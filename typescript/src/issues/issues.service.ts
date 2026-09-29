import {
  ConflictException,
  Injectable,
  NotFoundException,
  UnprocessableEntityException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import type { issue_status } from '../generated/prisma/enums.js';
import { ISSUE_INCLUDE, toIssue } from '../common/issue-shape.util.js';

interface UpdateIssueInput {
  title?: string;
  description?: string;
  status?: issue_status;
  label_ids?: string[];
}

const ISSUE_TRANSITIONS: Record<issue_status, issue_status[]> = {
  open: ['in_progress'],
  in_progress: ['closed'],
  closed: ['open'],
};

@Injectable()
export class IssuesService {
  constructor(private readonly prisma: PrismaService) {}

  async getIssue(issueId: string) {
    const issue = await this.prisma.issues.findUnique({
      where: { id: issueId },
      include: ISSUE_INCLUDE,
    });
    if (!issue) {
      throw new NotFoundException('Issue does not exist with this id');
    }
    return toIssue(issue);
  }

  async updateIssue(issueId: string, data: UpdateIssueInput) {
    const current = await this.prisma.issues.findUnique({
      where: { id: issueId },
    });
    if (!current) {
      throw new NotFoundException('Issue does not exist with this id');
    }

    if (
      data.status &&
      data.status !== current.status &&
      !ISSUE_TRANSITIONS[current.status].includes(data.status)
    ) {
      throw new ConflictException(
        `Cannot transition issue from ${current.status} to ${data.status}`,
      );
    }

    const { label_ids, ...issueData } = data;

    if (label_ids) {
      const uniqueLabelIds = [...new Set(label_ids)];
      const existingCount = await this.prisma.labels.count({
        where: { id: { in: uniqueLabelIds } },
      });
      if (existingCount !== uniqueLabelIds.length) {
        throw new UnprocessableEntityException(
          'One or more label_ids do not exist',
        );
      }
    }

    await this.prisma.$transaction(async (tx) => {
      if (label_ids) {
        await tx.issue_labels.deleteMany({ where: { issue_id: issueId } });
        if (label_ids.length > 0) {
          await tx.issue_labels.createMany({
            data: label_ids.map((label_id) => ({
              issue_id: issueId,
              label_id,
            })),
          });
        }
      }
      if (Object.keys(issueData).length > 0) {
        await tx.issues.update({ where: { id: issueId }, data: issueData });
      }
    });

    return this.getIssue(issueId);
  }

  async getIssueComments(
    issueId: string,
    params: { cursor?: string; limit: number },
  ) {
    await this.getIssue(issueId);

    const items = await this.prisma.comments.findMany({
      where: { issue_id: issueId },
      orderBy: { created_at: 'asc' },
      take: params.limit,
      ...(params.cursor && { cursor: { id: params.cursor }, skip: 1 }),
    });

    return {
      items,
      pagination: {
        next_cursor:
          items.length === params.limit ? items[items.length - 1].id : null,
        limit: params.limit,
      },
    };
  }

  async createIssueComment(
    issueId: string,
    data: { body: string; author_id: string },
  ) {
    await this.getIssue(issueId);

    const author = await this.prisma.users.findUnique({
      where: { id: data.author_id },
    });
    if (!author) {
      throw new UnprocessableEntityException(
        'author_id does not reference an existing user',
      );
    }

    return this.prisma.comments.create({
      data: { issue_id: issueId, author_id: data.author_id, body: data.body },
    });
  }

  async assignUser(issueId: string, userId: string) {
    await this.getIssue(issueId);

    const user = await this.prisma.users.findUnique({ where: { id: userId } });
    if (!user) {
      throw new NotFoundException('User does not exist with this id');
    }

    await this.prisma.issue_assignees.upsert({
      where: { issue_id_user_id: { issue_id: issueId, user_id: userId } },
      create: { issue_id: issueId, user_id: userId },
      update: {},
    });
  }

  async unassignUser(issueId: string, userId: string) {
    await this.getIssue(issueId);
    await this.prisma.issue_assignees.deleteMany({
      where: { issue_id: issueId, user_id: userId },
    });
  }
}

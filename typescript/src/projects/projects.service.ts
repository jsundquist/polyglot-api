import {
  ConflictException,
  Injectable,
  NotFoundException,
  UnprocessableEntityException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { Prisma } from '../generated/prisma/client.js';
import type {
  projectsCreateInput,
  projectsUpdateInput,
  webhook_subscriptionsUncheckedCreateInput,
} from '../generated/prisma/models.js';
import type { issue_status } from '../generated/prisma/enums.js';
import { ISSUE_INCLUDE, toIssue } from '../common/issue-shape.util.js';

const WEBHOOK_SELECT = {
  id: true,
  project_id: true,
  url: true,
  events: true,
  created_at: true,
} satisfies Prisma.webhook_subscriptionsSelect;

@Injectable()
export class ProjectsService {
  constructor(private readonly prismaService: PrismaService) {}

  async fetchProjects(cursor: string, limit: number = 50) {
    const items = await this.prismaService.projects.findMany({
      take: limit,
      orderBy: { id: 'asc' },
      ...(cursor && { cursor: { id: cursor }, skip: 1 }),
    });

    return {
      items,
      pagination: {
        next_cursor: items.length === limit ? items[items.length - 1].id : null,
        limit,
      },
    };
  }

  async createProject(data: projectsCreateInput) {
    try {
      return await this.prismaService.projects.create({ data });
    } catch (e) {
      if (
        e instanceof Prisma.PrismaClientKnownRequestError &&
        e.code === 'P2002'
      ) {
        throw new UnprocessableEntityException(
          `A project with the key of ${data.key} already exists`,
        );
      }
      throw e;
    }
  }

  async getProject(projectId: string) {
    const project = await this.prismaService.projects.findUnique({
      where: { id: projectId },
    });
    if (!project) {
      throw new NotFoundException(`Project does not exist with this id`);
    }
    return project;
  }

  async updateProject(id: string, data: projectsUpdateInput) {
    if (data.status) {
      const current = await this.getProject(id);
      if (current.status === 'archived') {
        throw new ConflictException(
          'Project is archived and cannot be updated further',
        );
      }
    }

    try {
      return await this.prismaService.projects.update({ where: { id }, data });
    } catch (e) {
      if (
        e instanceof Prisma.PrismaClientKnownRequestError &&
        e.code === 'P2025'
      ) {
        throw new NotFoundException(`Project does not exist with this id`);
      }
      throw e;
    }
  }

  async getProjectIssues(
    projectId: string,
    params: {
      cursor?: string;
      limit: number;
      status?: issue_status;
      label?: string;
      assignee?: string;
    },
  ) {
    await this.getProject(projectId);

    const items = await this.prismaService.issues.findMany({
      where: {
        project_id: projectId,
        ...(params.status && { status: params.status }),
        ...(params.label && {
          issue_labels: { some: { labels: { name: params.label } } },
        }),
        ...(params.assignee && {
          issue_assignees: { some: { user_id: params.assignee } },
        }),
      },
      include: ISSUE_INCLUDE,
      orderBy: { id: 'asc' },
      take: params.limit,
      ...(params.cursor && { cursor: { id: params.cursor }, skip: 1 }),
    });

    return {
      items: items.map(toIssue),
      pagination: {
        next_cursor:
          items.length === params.limit ? items[items.length - 1].id : null,
        limit: params.limit,
      },
    };
  }

  async createProjectIssue(
    projectId: string,
    data: {
      title: string;
      description?: string;
      status?: issue_status;
      label_ids?: string[];
      assignee_ids?: string[];
    },
  ) {
    await this.getProject(projectId);

    const { label_ids, assignee_ids, ...issueData } = data;

    if (label_ids && label_ids.length > 0) {
      const uniqueLabelIds = [...new Set(label_ids)];
      const existingCount = await this.prismaService.labels.count({
        where: { id: { in: uniqueLabelIds } },
      });
      if (existingCount !== uniqueLabelIds.length) {
        throw new UnprocessableEntityException(
          'One or more label_ids do not exist',
        );
      }
    }

    if (assignee_ids && assignee_ids.length > 0) {
      const uniqueAssigneeIds = [...new Set(assignee_ids)];
      const existingCount = await this.prismaService.users.count({
        where: { id: { in: uniqueAssigneeIds } },
      });
      if (existingCount !== uniqueAssigneeIds.length) {
        throw new UnprocessableEntityException(
          'One or more assignee_ids do not exist',
        );
      }
    }

    const created = await this.prismaService.issues.create({
      data: {
        ...issueData,
        project_id: projectId,
        issue_labels: label_ids
          ? { create: label_ids.map((label_id) => ({ label_id })) }
          : undefined,
        issue_assignees: assignee_ids
          ? { create: assignee_ids.map((user_id) => ({ user_id })) }
          : undefined,
      },
      include: ISSUE_INCLUDE,
    });

    return toIssue(created);
  }

  async getProjectWebhooks(projectId: string) {
    await this.getProject(projectId);
    return this.prismaService.webhook_subscriptions.findMany({
      where: { project_id: projectId },
      select: WEBHOOK_SELECT,
    });
  }

  async createProjectWebhooks(
    projectId: string,
    data: Omit<webhook_subscriptionsUncheckedCreateInput, 'project_id'>,
  ) {
    await this.getProject(projectId);
    return this.prismaService.webhook_subscriptions.create({
      data: { ...data, project_id: projectId },
      select: WEBHOOK_SELECT,
    });
  }
}

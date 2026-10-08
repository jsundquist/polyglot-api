import {
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  Param,
  Patch,
  Post,
  Put,
  Query,
} from '@nestjs/common';
import z from 'zod';
import { IssuesService } from './issues.service.js';
import type { issue_status } from '../generated/prisma/enums.js';
import { issueStatusSchema } from '../common/issue-status.util.js';
import {
  noNullBytes,
  optionalPositiveIntQuery,
  optionalUuidQuery,
} from '../common/zod.util.js';

@Controller('issues')
export class IssuesController {
  constructor(private readonly issuesService: IssuesService) {}

  @Get(':issueId')
  getIssue(@Param('issueId', { schema: z.uuidv4() }) issueId: string) {
    return this.issuesService.getIssue(issueId);
  }

  @Patch(':issueId')
  updateIssue(
    @Param('issueId', { schema: z.uuidv4() }) issueId: string,
    @Body({
      schema: z.object({
        title: noNullBytes(z.string().min(1)).optional(),
        description: noNullBytes(z.string()).optional(),
        status: issueStatusSchema.optional(),
        label_ids: z.array(z.uuidv4()).optional(),
      }),
    })
    data: {
      title?: string;
      description?: string;
      status?: issue_status;
      label_ids?: string[];
    },
  ) {
    return this.issuesService.updateIssue(issueId, data);
  }

  @Get(':issueId/comments')
  getIssueComments(
    @Param('issueId', { schema: z.uuidv4() }) issueId: string,
    @Query('cursor', { schema: optionalUuidQuery() }) cursor: string,
    @Query('limit', { schema: optionalPositiveIntQuery() })
    limit: number = 50,
  ) {
    return this.issuesService.getIssueComments(issueId, { cursor, limit });
  }

  @Post(':issueId/comments')
  createIssueComments(
    @Param('issueId', { schema: z.uuidv4() }) issueId: string,
    @Body({
      schema: z.object({
        body: noNullBytes(z.string().min(1)),
        author_id: z.uuidv4(),
      }),
    })
    data: { body: string; author_id: string },
  ) {
    return this.issuesService.createIssueComment(issueId, data);
  }

  @Put(':issueId/assignees/:userId')
  @HttpCode(204)
  updateIssueAssignees(
    @Param('issueId', { schema: z.uuidv4() }) issueId: string,
    @Param('userId', { schema: z.uuidv4() }) userId: string,
  ) {
    return this.issuesService.assignUser(issueId, userId);
  }

  @Delete(':issueId/assignees/:userId')
  @HttpCode(204)
  removeIssueAssignees(
    @Param('issueId', { schema: z.uuidv4() }) issueId: string,
    @Param('userId', { schema: z.uuidv4() }) userId: string,
  ) {
    return this.issuesService.unassignUser(issueId, userId);
  }
}

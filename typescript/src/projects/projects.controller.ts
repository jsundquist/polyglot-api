import {
  Body,
  Controller,
  Get,
  Param,
  Patch,
  Post,
  Query,
} from '@nestjs/common';
import z from 'zod';
import { ProjectsService } from './projects.service.js';
import {
  issue_status,
  Prisma,
  project_status,
} from '../generated/prisma/client.js';
import type { projectsUpdateInput } from '../generated/prisma/models.js';
import {
  noNullBytes,
  optionalPositiveIntQuery,
  optionalUuidQuery,
} from '../common/zod.util.js';

@Controller('projects')
export class ProjectsController {
  constructor(private readonly projectsService: ProjectsService) {}

  @Get()
  getProjects(
    @Query('cursor', { schema: optionalUuidQuery() }) cursor: string,
    @Query('limit', { schema: optionalPositiveIntQuery() })
    limit: number = 50,
  ) {
    return this.projectsService.fetchProjects(cursor, limit);
  }

  @Post()
  createProject(
    @Body({
      schema: z.object({
        name: noNullBytes(z.string().min(1)),
        key: noNullBytes(z.string().min(1)),
        description: noNullBytes(z.string()).optional(),
      }),
    })
    input: Prisma.projectsCreateInput,
  ) {
    return this.projectsService.createProject(input);
  }

  @Get(':projectId')
  getProject(@Param('projectId', { schema: z.uuidv4() }) projectId: string) {
    return this.projectsService.getProject(projectId);
  }

  @Patch(':projectId')
  updateProject(
    @Param('projectId', { schema: z.uuidv4() }) projectId: string,
    @Body({
      schema: z.object({
        name: noNullBytes(z.string().min(1)).optional(),
        key: noNullBytes(z.string().min(1)).optional(),
        description: noNullBytes(z.string()).optional(),
        status: z.enum(project_status).optional(),
      }),
    })
    data: projectsUpdateInput,
  ) {
    return this.projectsService.updateProject(projectId, data);
  }

  @Get(':projectId/issues')
  getProjectIssues(
    @Param('projectId', { schema: z.uuidv4() }) projectId: string,
    @Query('issueStatus', { schema: z.enum(issue_status).optional() })
    issueStatus: issue_status,
    @Query('label', { schema: z.string().optional() }) label: string,
    @Query('assignee', { schema: optionalUuidQuery() }) assignee: string,
    @Query('cursor', { schema: optionalUuidQuery() }) cursor: string,
    @Query('limit', { schema: optionalPositiveIntQuery() })
    limit: number = 50,
  ) {
    return this.projectsService.getProjectIssues(projectId, {
      cursor,
      limit,
      status: issueStatus,
      label,
      assignee,
    });
  }

  @Post(':projectId/issues')
  createIssue(
    @Param('projectId', { schema: z.uuidv4() }) projectId: string,
    @Body({
      schema: z.object({
        title: noNullBytes(z.string().min(1)),
        description: noNullBytes(z.string()).optional(),
        status: z.enum(issue_status).optional(),
        label_ids: z.array(z.uuidv4()).optional(),
        assignee_ids: z.array(z.uuidv4()).optional(),
      }),
    })
    body: {
      title: string;
      description?: string;
      status?: issue_status;
      label_ids?: string[];
      assignee_ids?: string[];
    },
  ) {
    return this.projectsService.createProjectIssue(projectId, body);
  }

  @Get(':projectId/webhooks')
  getProjectWebhooks(
    @Param('projectId', { schema: z.uuidv4() }) projectId: string,
  ) {
    return this.projectsService.getProjectWebhooks(projectId);
  }

  @Post(':projectId/webhooks')
  createWebhook(
    @Param('projectId', { schema: z.uuidv4() }) projectId: string,
    @Body({
      schema: z.object({
        url: noNullBytes(z.string().url()),
        events: z.array(noNullBytes(z.string().min(1))).min(1),
        secret: noNullBytes(z.string().min(1)),
      }),
    })
    body: Omit<Prisma.webhook_subscriptionsUncheckedCreateInput, 'project_id'>,
  ) {
    return this.projectsService.createProjectWebhooks(projectId, body);
  }
}

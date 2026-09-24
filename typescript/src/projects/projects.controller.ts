import { Controller, Get, NotImplementedException, Param, Patch, Post } from '@nestjs/common';
import z from 'zod';

@Controller('projects')
export class ProjectsController {
  @Get()
  getProjects() {
    throw new NotImplementedException();
  }

  @Post()
  createProject() {
    throw new NotImplementedException();
  }

  @Get(':projectId')
  getProject(@Param('projectId', { schema: z.string().min(1) }) projectId: string) {
    throw new NotImplementedException();
  }

  @Patch(':projectId')
  updateProject(@Param('projectId', { schema: z.string().min(1) }) projectId: string) {
    throw new NotImplementedException();
  }

  @Get(':projectId/issues')
  getProjectIssues(@Param('projectId', { schema: z.string().min(1) }) projectId: string) {
    throw new NotImplementedException();
  }

  @Post(':projectId/issues')
  createIssue(@Param('projectId', { schema: z.string().min(1) }) projectId: string) {
    throw new NotImplementedException();
  }

  @Get(':projectId/webhooks')
  getProjectWebhooks(@Param('projectId', { schema: z.string().min(1) }) projectId: string) {
    throw new NotImplementedException();
  }

  @Post(':projectId/webhooks')
  createWebhook(@Param('projectId', { schema: z.string().min(1) }) projectId: string) {
    throw new NotImplementedException();
  }
}

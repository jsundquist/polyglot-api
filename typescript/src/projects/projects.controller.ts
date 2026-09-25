import { Controller, Get, NotImplementedException, Patch, Post } from '@nestjs/common';

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
  getProject() {
    throw new NotImplementedException();
  }

  @Patch(':projectId')
  updateProject() {
    throw new NotImplementedException();
  }

  @Get(':projectId/issues')
  getProjectIssues() {
    throw new NotImplementedException();
  }

  @Post(':projectId/issues')
  createIssue() {
    throw new NotImplementedException();
  }

  @Get(':projectId/webhooks')
  getProjectWebhooks() {
    throw new NotImplementedException();
  }

  @Post(':projectId/webhooks')
  createWebhook() {
    throw new NotImplementedException();
  }
}

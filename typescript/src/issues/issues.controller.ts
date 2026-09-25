import { Controller, Delete, Get, NotImplementedException, Patch, Post, Put } from '@nestjs/common';

@Controller('issues')
export class IssuesController {
  @Get(':issueId')
  getIssue() {
    throw new NotImplementedException();
  }

  @Patch(':issueId')
  updateIssue() {
    throw new NotImplementedException();
  }

  @Get(':issueId/comments')
  getIssueComments() {
    throw new NotImplementedException();
  }

  @Post(':issueId/comments')
  createIssueComments() {
    throw new NotImplementedException();
  }

  @Put(':issueId/assignees/:userId')
  updateIssueAssignees() {
    throw new NotImplementedException();
  }

  @Delete(':issueId/assignees/:userId')
  removeIssueAssignees() {
    throw new NotImplementedException();
  }
}

import { Controller, Delete, Get, NotImplementedException, Param, Patch, Post, Put } from '@nestjs/common';
import z from 'zod';

@Controller('issues')
export class IssuesController {
  @Get(':issueId')
  getIssue(@Param('issueId', { schema: z.string().min(1) }) issueId: string) {
    throw new NotImplementedException();
  }

  @Patch(':issueId')
  updateIssue(@Param('issueId', { schema: z.string().min(1) }) issueId: string) {
    throw new NotImplementedException();
  }

  @Get(':issueId/comments')
  getIssueComments(@Param('issueId', { schema: z.string().min(1) }) issueId: string) {
    throw new NotImplementedException();
  }

  @Post(':issueId/comments')
  createIssueComments(@Param('issueId', { schema: z.string().min(1) }) issueId: string) {
    throw new NotImplementedException();
  }

  @Put(':issueId/assignees/:userId')
  updateIssueAssignees(@Param('issueId', { schema: z.string().min(1) }) issueId: string,
    @Param('userId', { schema: z.string().min(1) }) userId: string) {
    throw new NotImplementedException();
  }

  @Delete(':issueId/assignees/:userId')
  removeIssueAssignees(@Param('issueId', { schema: z.string().min(1) }) issueId: string,
    @Param('userId', { schema: z.string().min(1) }) userId: string) {
    throw new NotImplementedException();
  }
}

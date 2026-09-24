import { Controller, Delete, NotImplementedException, Param, Patch } from '@nestjs/common';
import z from 'zod';

@Controller('comments')
export class CommentsController {
  @Patch(':commentId')
  updateComment(@Param('commentId', {schema: z.string().min(1)}) commentId: string) {
    throw new NotImplementedException();
  }

  @Delete(':commentId')
  deleteComment(@Param('commentId', {schema: z.string().min(1)}) commentId: string) {
    throw new NotImplementedException();
  }
}

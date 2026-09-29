import {
  Body,
  Controller,
  Delete,
  HttpCode,
  Param,
  Patch,
} from '@nestjs/common';
import z from 'zod';
import { CommentsService } from './comments.service.js';
import { noNullBytes } from '../common/zod.util.js';

@Controller('comments')
export class CommentsController {
  constructor(private readonly commentsService: CommentsService) {}

  @Patch(':commentId')
  updateComment(
    @Param('commentId', { schema: z.uuidv4() }) commentId: string,
    @Body({ schema: z.object({ body: noNullBytes(z.string().min(1)) }) })
    data: { body: string },
  ) {
    return this.commentsService.updateComment(commentId, data);
  }

  @Delete(':commentId')
  @HttpCode(204)
  deleteComment(@Param('commentId', { schema: z.uuidv4() }) commentId: string) {
    return this.commentsService.deleteComment(commentId);
  }
}

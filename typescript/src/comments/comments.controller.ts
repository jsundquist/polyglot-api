import { Controller, Delete, NotImplementedException, Patch } from '@nestjs/common';

@Controller('comments')
export class CommentsController {
  @Patch(':commentId')
  updateComment() {
    throw new NotImplementedException();
  }

  @Delete(':commentId')
  deleteComment() {
    throw new NotImplementedException();
  }
}

import { Controller, Delete, Get, NotImplementedException, Param, Post } from '@nestjs/common';

@Controller('labels')
export class LabelsController {
  @Get()
  getLabels() {
    throw new NotImplementedException();
  }

  @Post()
  createLabel() {
    throw new NotImplementedException();
  }

  @Delete(':labelId')
  deleteLabel(@Param('labelId') labelId: string) {
    throw new NotImplementedException();
  }
}

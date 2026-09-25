import { Body, Controller, Delete, Get, HttpCode, Param, Post, Query } from '@nestjs/common';
import z from 'zod';

import { LabelsService } from './labels.service.js';
import { Prisma } from '../generated/prisma/client.js';

@Controller('labels')
export class LabelsController {
  constructor(private readonly labelsService: LabelsService) { }

  @Get()
  getLabels(@Query('cursor', { schema: z.string().optional() }) cursor: string, @Query('limit', { schema: z.coerce.number().optional() }) limit: number) {
    return this.labelsService.fetchLabels(cursor, limit);
  }

  @Post()
  createLabel(@Body({ schema: z.object({ name: z.string().min(1), color: z.string().min(1) }) }) labelData: Prisma.labelsCreateInput) {
    return this.labelsService.createLabel(labelData);
  }

  @Delete(':labelId')
  @HttpCode(204)
  deleteLabel(@Param('labelId', { schema: z.uuidv4() }) labelId: string) {
    return this.labelsService.deleteLabel(labelId);
  }
}

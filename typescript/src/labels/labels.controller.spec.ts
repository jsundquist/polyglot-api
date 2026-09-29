import { Test, TestingModule } from '@nestjs/testing';
import { LabelsController } from './labels.controller.js';
import { LabelsService } from './labels.service.js';
import { PrismaService } from '../prisma/prisma.service.js';

describe('LabelsController', () => {
  let controller: LabelsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [LabelsController],
      providers: [LabelsService, { provide: PrismaService, useValue: {} }],
    }).compile();

    controller = module.get<LabelsController>(LabelsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});

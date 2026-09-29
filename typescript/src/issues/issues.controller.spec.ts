import { Test, TestingModule } from '@nestjs/testing';
import { IssuesController } from './issues.controller.js';
import { IssuesService } from './issues.service.js';
import { PrismaService } from '../prisma/prisma.service.js';

describe('IssuesController', () => {
  let controller: IssuesController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [IssuesController],
      providers: [IssuesService, { provide: PrismaService, useValue: {} }],
    }).compile();

    controller = module.get<IssuesController>(IssuesController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});

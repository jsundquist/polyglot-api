import { Test, TestingModule } from '@nestjs/testing';
import { IssuesService } from './issues.service.js';
import { PrismaService } from '../prisma/prisma.service.js';

describe('IssuesService', () => {
  let service: IssuesService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [IssuesService, { provide: PrismaService, useValue: {} }],
    }).compile();

    service = module.get<IssuesService>(IssuesService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});

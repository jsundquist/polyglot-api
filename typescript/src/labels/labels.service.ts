import { Injectable, NotFoundException, UnprocessableEntityException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';

import { Prisma, labels } from '../generated/prisma/client.js';

@Injectable()
export class LabelsService {

  constructor(private readonly prisma: PrismaService) { }

  async fetchLabels(cursor: string, limit: number = 50): Promise<{ items: labels[], pagination: { next_cursor: string | null, limit: number } }> {
    const items = await this.prisma.labels.findMany({
      take: limit,
      orderBy: { id: 'asc' },
      ...(cursor && { cursor: { id: cursor }, skip: 1 }),
    });

    return {
      items,
      pagination: {
        next_cursor: items.length === limit ? items[items.length - 1].id : null,
        limit,
      },
    };
  }

  async createLabel(data: Prisma.labelsCreateInput): Promise<labels> {
    try {
      return await this.prisma.labels.create({ data });
    } catch (e) {
      if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2002') {
        throw new UnprocessableEntityException(`A label with the name of ${data.name} already exists`);
      }
      throw e;
    }
  }

  async deleteLabel(id: string): Promise<labels> {
    try {
      return await this.prisma.labels.delete({ where: { id } });
    } catch (e) {
      if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2025') {
        throw new NotFoundException(`Label does not exist with this id`);
      }
      throw e;
    }
  }
}

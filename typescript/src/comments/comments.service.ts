import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { Prisma } from '../generated/prisma/client.js';

@Injectable()
export class CommentsService {
  constructor(private readonly prisma: PrismaService) {}

  async updateComment(commentId: string, data: { body: string }) {
    try {
      return await this.prisma.comments.update({
        where: { id: commentId },
        data: { body: data.body, updated_at: new Date() },
      });
    } catch (e) {
      if (
        e instanceof Prisma.PrismaClientKnownRequestError &&
        e.code === 'P2025'
      ) {
        throw new NotFoundException('Comment does not exist with this id');
      }
      throw e;
    }
  }

  async deleteComment(commentId: string) {
    try {
      await this.prisma.comments.delete({ where: { id: commentId } });
    } catch (e) {
      if (
        e instanceof Prisma.PrismaClientKnownRequestError &&
        e.code === 'P2025'
      ) {
        throw new NotFoundException('Comment does not exist with this id');
      }
      throw e;
    }
  }
}

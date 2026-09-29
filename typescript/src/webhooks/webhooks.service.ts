import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service.js';
import { Prisma } from '../generated/prisma/client.js';

const WEBHOOK_SELECT = {
  id: true,
  project_id: true,
  url: true,
  events: true,
  created_at: true,
} satisfies Prisma.webhook_subscriptionsSelect;

@Injectable()
export class WebhooksService {
  constructor(private readonly prisma: PrismaService) {}

  async getWebhook(webhookId: string) {
    const webhook = await this.prisma.webhook_subscriptions.findUnique({
      where: { id: webhookId },
      select: WEBHOOK_SELECT,
    });
    if (!webhook) {
      throw new NotFoundException('Webhook does not exist with this id');
    }
    return webhook;
  }

  async deleteWebhook(webhookId: string) {
    try {
      await this.prisma.webhook_subscriptions.delete({
        where: { id: webhookId },
      });
    } catch (e) {
      if (
        e instanceof Prisma.PrismaClientKnownRequestError &&
        e.code === 'P2025'
      ) {
        throw new NotFoundException('Webhook does not exist with this id');
      }
      throw e;
    }
  }
}

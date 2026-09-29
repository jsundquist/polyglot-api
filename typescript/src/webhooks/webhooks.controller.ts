import { Controller, Delete, Get, HttpCode, Param } from '@nestjs/common';
import z from 'zod';
import { WebhooksService } from './webhooks.service.js';

@Controller('webhooks')
export class WebhooksController {
  constructor(private readonly webhooksService: WebhooksService) {}

  @Get(':webhookId')
  getWebhook(@Param('webhookId', { schema: z.uuidv4() }) webhookId: string) {
    return this.webhooksService.getWebhook(webhookId);
  }

  @Delete(':webhookId')
  @HttpCode(204)
  deleteWebhook(@Param('webhookId', { schema: z.uuidv4() }) webhookId: string) {
    return this.webhooksService.deleteWebhook(webhookId);
  }
}

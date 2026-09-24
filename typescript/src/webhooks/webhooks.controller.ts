import { Controller, Delete, Get, NotImplementedException, Param } from '@nestjs/common';

@Controller('webhooks')
export class WebhooksController {
  @Get(':webhookId')
  getWebhook(@Param('webhookId') webhookId: string){
    throw new NotImplementedException();
  }

  @Delete(':webhookId')
  deleteWebhook(@Param('webhookId') webhookId: string) {
    throw new NotImplementedException();
  }
}

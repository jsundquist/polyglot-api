import { Controller, Delete, Get, NotImplementedException } from '@nestjs/common';

@Controller('webhooks')
export class WebhooksController {
  @Get(':webhookId')
  getWebhook(){
    throw new NotImplementedException();
  }

  @Delete(':webhookId')
  deleteWebhook() {
    throw new NotImplementedException();
  }
}

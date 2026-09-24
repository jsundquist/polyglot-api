import { Module } from '@nestjs/common';
import { AppController } from './app.controller.js';
import { AppService } from './app.service.js';
import { IssuesModule } from './issues/issues.module.js';
import { ProjectsModule } from './projects/projects.module.js';
import { CommentsModule } from './comments/comments.module.js';
import { LabelsController } from './labels/labels.controller.js';
import { LabelsModule } from './labels/labels.module.js';
import { WebhooksController } from './webhooks/webhooks.controller.js';
import { WebhooksModule } from './webhooks/webhooks.module.js';

@Module({
  imports: [IssuesModule, ProjectsModule, CommentsModule, LabelsModule, WebhooksModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

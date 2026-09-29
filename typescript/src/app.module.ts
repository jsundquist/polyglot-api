import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { APP_GUARD } from '@nestjs/core';
import { AppController } from './app.controller.js';
import { AppService } from './app.service.js';
import { CommentsModule } from './comments/comments.module.js';
import { IssuesModule } from './issues/issues.module.js';
import { LabelsModule } from './labels/labels.module.js';
import { ProjectsModule } from './projects/projects.module.js';
import { WebhooksModule } from './webhooks/webhooks.module.js';
import { ApiKeyGuard } from './common/guards/api-key.guard.js';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    IssuesModule,
    ProjectsModule,
    CommentsModule,
    LabelsModule,
    WebhooksModule,
  ],
  controllers: [AppController],
  providers: [AppService, { provide: APP_GUARD, useClass: ApiKeyGuard }],
})
export class AppModule {}

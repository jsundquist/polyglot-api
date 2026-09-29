import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Reflector } from '@nestjs/core';
import type { Request } from 'express';
import { IS_PUBLIC_KEY } from '../decorators/public.decorator.js';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(
    private readonly configService: ConfigService,
    private readonly reflector: Reflector,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) {
      return true;
    }

    const request = context.switchToHttp().getRequest<Request>();
    const providedKey = this.extractKey(request);
    const validKeys = this.configService
      .getOrThrow<string>('API_KEY')
      .split(',')
      .map((key) => key.trim())
      .filter(Boolean);

    if (!providedKey || !validKeys.includes(providedKey)) {
      throw new UnauthorizedException('A valid API key is required');
    }

    return true;
  }

  private extractKey(request: Request): string | undefined {
    const headerKey = request.header('X-API-Key');
    if (headerKey) {
      return headerKey;
    }

    const authHeader = request.header('Authorization');
    if (authHeader?.startsWith('Bearer ')) {
      return authHeader.slice('Bearer '.length);
    }

    return undefined;
  }
}

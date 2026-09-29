import {
  ArgumentsHost,
  Catch,
  ExceptionFilter,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import type { Response } from 'express';

const STATUS_CODES: Record<number, string> = {
  401: 'unauthorized',
  404: 'not_found',
  409: 'conflict',
  422: 'validation_error',
};

/**
 * Global error shaping: known HttpExceptions map to the contract's
 * {code, message, details?} shape. Anything else - a Prisma/driver error, an
 * unhandled edge case - still comes back in that same shape as a generic 500
 * instead of leaking Nest's default error format or a stack trace.
 */
@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(HttpExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse<Response>();

    if (!(exception instanceof HttpException)) {
      this.logger.error(exception);
      response.status(HttpStatus.INTERNAL_SERVER_ERROR).json({
        code: 'internal_error',
        message: 'An unexpected error occurred',
      });
      return;
    }

    const status = exception.getStatus();
    const body = exception.getResponse();
    const message =
      typeof body === 'string'
        ? body
        : ((body as { message?: string }).message ?? exception.message);
    const details =
      typeof body === 'object'
        ? (body as { details?: unknown }).details
        : undefined;

    response.status(status).json({
      code:
        STATUS_CODES[status] ??
        exception.name.replace(/Exception$/, '').toLowerCase(),
      message,
      ...(details !== undefined && { details }),
    });
  }
}

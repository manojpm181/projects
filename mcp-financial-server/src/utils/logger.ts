import pino from 'pino';
import { env } from '@/config/env.js';

const createLogger = pino.default ?? pino;

export const logger = createLogger({
  level: env.NODE_ENV === 'production' ? 'info' : 'debug',

  transport: env.NODE_ENV === 'development'
    ? {
        target: 'pino-pretty',
        options: {
          colorize: true,
          translateTime: 'SYS:standard',
          ignore: 'pid,hostname',
        },
      }
    : undefined,
});

export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = 'AppError';
  }
}

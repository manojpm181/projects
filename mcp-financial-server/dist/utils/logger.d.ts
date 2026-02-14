import pino from 'pino';
export declare const logger: pino.Logger<never>;
export declare class AppError extends Error {
    readonly code: string;
    readonly statusCode: number;
    readonly details?: unknown | undefined;
    constructor(message: string, code: string, statusCode?: number, details?: unknown | undefined);
}
//# sourceMappingURL=logger.d.ts.map
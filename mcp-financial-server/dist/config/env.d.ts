import { z } from 'zod';
declare const envSchema: z.ZodObject<{
    NODE_ENV: z.ZodDefault<z.ZodEnum<["development", "production", "test"]>>;
    SUPABASE_URL: z.ZodString;
    SUPABASE_ANON_KEY: z.ZodString;
    SUPABASE_SERVICE_ROLE_KEY: z.ZodOptional<z.ZodString>;
    LOG_LEVEL: z.ZodDefault<z.ZodEnum<["fatal", "error", "warn", "info", "debug", "trace"]>>;
    PORT: z.ZodDefault<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    NODE_ENV: "development" | "production" | "test";
    SUPABASE_URL: string;
    SUPABASE_ANON_KEY: string;
    LOG_LEVEL: "fatal" | "error" | "warn" | "info" | "debug" | "trace";
    PORT: number;
    SUPABASE_SERVICE_ROLE_KEY?: string | undefined;
}, {
    SUPABASE_URL: string;
    SUPABASE_ANON_KEY: string;
    NODE_ENV?: "development" | "production" | "test" | undefined;
    SUPABASE_SERVICE_ROLE_KEY?: string | undefined;
    LOG_LEVEL?: "fatal" | "error" | "warn" | "info" | "debug" | "trace" | undefined;
    PORT?: number | undefined;
}>;
export type Env = z.infer<typeof envSchema>;
export declare const env: {
    NODE_ENV: "development" | "production" | "test";
    SUPABASE_URL: string;
    SUPABASE_ANON_KEY: string;
    LOG_LEVEL: "fatal" | "error" | "warn" | "info" | "debug" | "trace";
    PORT: number;
    SUPABASE_SERVICE_ROLE_KEY?: string | undefined;
};
export declare const isProduction: boolean;
export declare const isDevelopment: boolean;
export {};
//# sourceMappingURL=env.d.ts.map
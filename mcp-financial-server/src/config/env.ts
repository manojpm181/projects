import dotenv from 'dotenv';
import { z } from 'zod';
dotenv.config();
const envSchema = z.object({

  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),

  SUPABASE_URL: z.string().url(),

  SUPABASE_ANON_KEY: z.string().min(1),

  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1).optional(),

  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace']).default('info'),

  PORT: z.coerce.number().int().positive().default(3001),

});

export type Env = z.infer<typeof envSchema>;

export const env = envSchema.parse(process.env);

export const isProduction = env.NODE_ENV === 'production';

export const isDevelopment = env.NODE_ENV === 'development';

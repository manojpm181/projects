import { createClient } from '@supabase/supabase-js';

import { env } from '@/config/env.js';

import { logger } from '@/utils/logger.js';

export const supabase = createClient(env.SUPABASE_URL, env.SUPABASE_ANON_KEY, {

  auth: {

    persistSession: false,

  },

});

export async function testConnection() {

  try {

    const { error } = await supabase.from('companies').select('count').limit(1);

    if (error) throw error;

    logger.info('✅ Database connection successful');

    return true;

  } catch (error) {

    logger.error(`❌ Database connection failed: ${String(error)}`);

    return false;

  }

}
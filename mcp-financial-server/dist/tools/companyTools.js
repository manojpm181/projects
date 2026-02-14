import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { supabase } from '../db/client.js';
import { logger } from '../utils/logger.js';
export function registerCompanyTools(server) {
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        try {
            switch (request.params.name) {
                case 'get_company_profile': {
                    const { identifier } = request.params.arguments;
                    const { data, error } = await supabase
                        .from('companies')
                        .select('*')
                        .or(`ticker.ilike.%${identifier}%,name.ilike.%${identifier}%`)
                        .limit(1)
                        .single();
                    if (error) {
                        return {
                            content: [{
                                    type: 'text',
                                    text: JSON.stringify({
                                        success: false,
                                        error: 'Company not found',
                                        details: error.message,
                                    }, null, 2),
                                }],
                        };
                    }
                    return {
                        content: [{
                                type: 'text',
                                text: JSON.stringify({
                                    success: true,
                                    data,
                                    metadata: {
                                        source: 'Supabase',
                                        retrieved_at: new Date().toISOString(),
                                    },
                                }, null, 2),
                            }],
                    };
                }
                case 'search_companies': {
                    const args = request.params.arguments;
                    let query = supabase.from('companies').select('*');
                    if (args.sector)
                        query = query.eq('sector', args.sector);
                    if (args.industry)
                        query = query.eq('industry', args.industry);
                    if (args.min_market_cap)
                        query = query.gte('market_cap', args.min_market_cap);
                    if (args.max_market_cap)
                        query = query.lte('market_cap', args.max_market_cap);
                    if (args.country)
                        query = query.eq('country', args.country);
                    query = query.order('market_cap', { ascending: false });
                    const { data, error } = await query;
                    if (error) {
                        return {
                            content: [{
                                    type: 'text',
                                    text: JSON.stringify({
                                        success: false,
                                        error: 'Search failed',
                                        details: error.message,
                                    }, null, 2),
                                }],
                        };
                    }
                    return {
                        content: [{
                                type: 'text',
                                text: JSON.stringify({
                                    success: true,
                                    data: data || [],
                                    count: data?.length || 0,
                                    metadata: {
                                        filters_applied: Object.keys(args).filter(k => args[k] !== undefined),
                                        retrieved_at: new Date().toISOString(),
                                    },
                                }, null, 2),
                            }],
                    };
                }
                default:
                    return {
                        content: [{
                                type: 'text',
                                text: JSON.stringify({
                                    success: false,
                                    error: `Tool ${request.params.name} not found`,
                                }, null, 2),
                            }],
                    };
            }
        }
        catch (error) {
            logger.error('Tool error:', error);
            return {
                content: [{
                        type: 'text',
                        text: JSON.stringify({
                            success: false,
                            error: 'Internal server error',
                            details: error.message,
                        }, null, 2),
                    }],
            };
        }
    });
}
//# sourceMappingURL=companyTools.js.map
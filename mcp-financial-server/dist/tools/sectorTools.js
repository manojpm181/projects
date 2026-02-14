import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { supabase } from '../db/client.js';
import { logger } from '../utils/logger.js';
export function registerSectorTools(server) {
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        try {
            switch (request.params.name) {
                case 'get_sector_overview': {
                    const { sector } = request.params.arguments;
                    // Get companies in this sector
                    const { data: companies, error: companiesError } = await supabase
                        .from('companies')
                        .select('*')
                        .eq('sector', sector);
                    if (companiesError) {
                        return {
                            content: [{
                                    type: 'text',
                                    text: JSON.stringify({
                                        success: false,
                                        error: 'Failed to fetch sector data',
                                        details: companiesError.message,
                                    }, null, 2),
                                }],
                        };
                    }
                    if (!companies || companies.length === 0) {
                        return {
                            content: [{
                                    type: 'text',
                                    text: JSON.stringify({
                                        success: false,
                                        error: 'Sector not found or empty',
                                    }, null, 2),
                                }],
                        };
                    }
                    // Calculate sector statistics
                    const totalMarketCap = companies.reduce((sum, c) => sum + c.market_cap, 0);
                    const avgMarketCap = totalMarketCap / companies.length;
                    const largestCompany = companies.reduce((max, c) => c.market_cap > max.market_cap ? c : max);
                    // Get top 5 companies by market cap
                    const topCompanies = [...companies]
                        .sort((a, b) => b.market_cap - a.market_cap)
                        .slice(0, 5);
                    return {
                        content: [{
                                type: 'text',
                                text: JSON.stringify({
                                    success: true,
                                    data: {
                                        sector,
                                        company_count: companies.length,
                                        total_market_cap: totalMarketCap,
                                        average_market_cap: avgMarketCap,
                                        largest_company: {
                                            name: largestCompany.name,
                                            ticker: largestCompany.ticker,
                                            market_cap: largestCompany.market_cap,
                                        },
                                        top_companies: topCompanies.map(c => ({
                                            ticker: c.ticker,
                                            name: c.name,
                                            market_cap: c.market_cap,
                                            market_share: ((c.market_cap / totalMarketCap) * 100).toFixed(2) + '%',
                                        })),
                                    },
                                    metadata: {
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
            logger.error('Sector tool error:', error);
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
//# sourceMappingURL=sectorTools.js.map
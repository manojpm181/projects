import { Server } from '@modelcontextprotocol/sdk/server/index.js';

import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';


import { supabase } from '../db/client.js';
import { logger } from '../utils/logger.js';


export function registerStockTools(server: Server) {

  server.setRequestHandler(CallToolRequestSchema, async (request) => {


    try {

      switch (request.params.name) {

        case 'get_stock_price_history': {

          const { ticker, start_date, end_date, limit = 30 } = request.params.arguments as any;

          

          // Get company ID

          const { data: company, error: companyError } = await supabase

            .from('companies')

            .select('id')

            .eq('ticker', ticker.toUpperCase())

            .single();

          if (companyError || !company) {

            return {

              content: [{

                type: 'text',

                text: JSON.stringify({

                  success: false,

                  error: 'Company not found',

                }, null, 2),

              }],

            };

          }

          let query = supabase

            .from('stock_prices')

            .select('*')

            .eq('company_id', company.id)

            .order('date', { ascending: false })

            .limit(limit);

          if (start_date) query = query.gte('date', start_date);

          if (end_date) query = query.lte('date', end_date);

          const { data, error } = await query;

          if (error) {

            return {

              content: [{

                type: 'text',

                text: JSON.stringify({

                  success: false,

                  error: 'Failed to fetch stock prices',

                  details: error.message,

                }, null, 2),

              }],

            };

          }

          // Calculate statistics

          const prices = data || [];

          let totalReturn = 0;

          let high = -Infinity;

          let low = Infinity;

          let totalVolume = 0;

          if (prices.length > 0) {

            const firstPrice = prices[prices.length - 1].close;

            const lastPrice = prices[0].close;

            totalReturn = ((lastPrice - firstPrice) / firstPrice) * 100;

            prices.forEach(price => {

              if (price.high > high) high = price.high;

              if (price.low < low) low = price.low;

              totalVolume += price.volume;

            });

          }

          return {

            content: [{

              type: 'text',

              text: JSON.stringify({

                success: true,

                data: prices,

                statistics: {

                  period_return: totalReturn.toFixed(2) + '%',

                  highest_price: high !== -Infinity ? high : null,

                  lowest_price: low !== Infinity ? low : null,

                  avg_daily_volume: prices.length > 0 ? Math.round(totalVolume / prices.length) : 0,

                  data_points: prices.length,

                },

                metadata: {

                  ticker: ticker.toUpperCase(),

                  period: start_date && end_date ? `${start_date} to ${end_date}` : `Last ${limit} days`,

                  retrieved_at: new Date().toISOString(),

                },

              }, null, 2),

            }],

          };

        }

        case 'screen_stocks': {

          const args = request.params.arguments as any;

          

          // Get all companies with their latest financials

          const { data: companies, error: companiesError } = await supabase

            .from('companies')

            .select(`

              *,

              financial_reports!inner(*)

            `)

            .order('financial_reports.fiscal_year', { ascending: false })

            .order('financial_reports.fiscal_quarter', { ascending: false });

          if (companiesError) {

            return {

              content: [{

                type: 'text',

                text: JSON.stringify({

                  success: false,

                  error: 'Failed to fetch companies',

                  details: companiesError.message,

                }, null, 2),

              }],

            };

          }

          // Apply screening filters

          const screened = (companies || []).filter(company => {

            const latestReport = company.financial_reports?.[0];

            if (!latestReport) return false;

            if (args.min_revenue && latestReport.revenue < args.min_revenue) return false;

            if (args.min_eps && latestReport.eps && latestReport.eps < args.min_eps) return false;

            if (args.min_gross_margin && latestReport.gross_margin && latestReport.gross_margin < args.min_gross_margin) return false;

            if (args.max_debt_to_equity && latestReport.debt_to_equity && latestReport.debt_to_equity > args.max_debt_to_equity) return false;

            if (args.sector && company.sector !== args.sector) return false;

            if (args.min_market_cap && company.market_cap < args.min_market_cap) return false;

            if (args.max_market_cap && company.market_cap > args.max_market_cap) return false;

            return true;

          });

          return {

            content: [{

              type: 'text',

              text: JSON.stringify({

                success: true,

                data: screened,

                count: screened.length,

                metadata: {

                  filters_applied: Object.keys(args).filter(k => args[k] !== undefined),

                  screening_date: new Date().toISOString(),

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

    } catch (error: any) {

      logger.error('Stock tool error:', error);

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
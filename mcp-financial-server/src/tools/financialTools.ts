import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';

import { supabase } from '../db/client.js';
import { logger } from '../utils/logger.js';

export function registerFinancialTools(server: Server) {
  server.setRequestHandler(CallToolRequestSchema, async (request) => {

    try {
      switch (request.params.name) {
        case 'get_financial_report': {
          const { ticker, fiscal_year, fiscal_quarter } = request.params.arguments as any;
          
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
            .from('financial_reports')
            .select('*')
            .eq('company_id', company.id);

          if (fiscal_year) query = query.eq('fiscal_year', fiscal_year);
          if (fiscal_quarter) query = query.eq('fiscal_quarter', fiscal_quarter);

          query = query.order('fiscal_year', { ascending: false })
                      .order('fiscal_quarter', { ascending: false });

          const { data, error } = await query;

          if (error) {
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  success: false,
                  error: 'Failed to fetch financial reports',
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
                metadata: {
                  ticker: ticker.toUpperCase(),
                  report_count: data?.length || 0,
                  retrieved_at: new Date().toISOString(),
                },
              }, null, 2),
            }],
          };
        }

        case 'compare_companies': {
          const { tickers } = request.params.arguments as any;
          
          if (!tickers || !Array.isArray(tickers) || tickers.length < 2 || tickers.length > 5) {
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  success: false,
                  error: 'Must provide 2-5 tickers',
                }, null, 2),
              }],
            };
          }

          const { data: companies, error: companiesError } = await supabase
            .from('companies')
            .select('*')
            .in('ticker', tickers.map((t: string) => t.toUpperCase()));

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

          // Get latest financials for each company
          const comparisons = await Promise.all(
            companies.map(async (company) => {
              const { data: latestReport } = await supabase
                .from('financial_reports')
                .select('*')
                .eq('company_id', company.id)
                .order('fiscal_year', { ascending: false })
                .order('fiscal_quarter', { ascending: false })
                .limit(1)
                .single();

              return {
                company: {
                  ticker: company.ticker,
                  name: company.name,
                  sector: company.sector,
                  market_cap: company.market_cap,
                },
                latest_report: latestReport,
              };
            })
          );

          return {
            content: [{
              type: 'text',
              text: JSON.stringify({
                success: true,
                data: comparisons,
                metadata: {
                  companies_compared: tickers,
                  compared_at: new Date().toISOString(),
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
      logger.error('Financial tool error:', error);
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
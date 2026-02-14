import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js';

import { supabase } from '../db/client.js';
import { logger } from '../utils/logger.js';

export function registerAnalystTools(server: Server) {

  server.setRequestHandler(CallToolRequestSchema, async (request) => {

    try {

      switch (request.params.name) {

        case 'get_analyst_ratings': {

          const { ticker, firm, limit = 10 } = request.params.arguments as any;

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
            .from('analyst_ratings')
            .select('*')
            .eq('company_id', company.id)
            .order('rating_date', { ascending: false })
            .limit(limit);

          if (firm) {
            query = query.eq('analyst_firm', firm);
          }

          const { data, error } = await query;

          if (error) {
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  success: false,
                  error: 'Failed to fetch analyst ratings',
                  details: error.message,
                }, null, 2),
              }],
            };
          }

          // Calculate consensus
          const ratings = data || [];
          const ratingCounts: Record<string, number> = {};
          let totalTarget = 0;
          let targetCount = 0;

          ratings.forEach((rating: any) => {
            ratingCounts[rating.rating] =
              (ratingCounts[rating.rating] || 0) + 1;

            if (rating.target_price) {
              totalTarget += rating.target_price;
              targetCount++;
            }
          });

          const consensus = Object.entries(ratingCounts)
            .sort((a, b) => b[1] - a[1])
            .map(([rating, count]) => ({ rating, count }))[0];

          return {
            content: [{
              type: 'text',
              text: JSON.stringify({
                success: true,
                data: ratings,
                analysis: {
                  consensus: consensus ? consensus.rating : 'No consensus',
                  average_target_price:
                    targetCount > 0 ? totalTarget / targetCount : null,
                  total_ratings: ratings.length,
                  rating_distribution: ratingCounts,
                },
                metadata: {
                  ticker: ticker.toUpperCase(),
                  firm_filter: firm || 'All firms',
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

    } catch (error: any) {
      logger.error('Analyst tool error:', error);
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

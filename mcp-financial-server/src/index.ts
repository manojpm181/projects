#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';

import { createServer } from 'http';

import { env } from './config/env.js';
import { logger } from './utils/logger.js';
import { testConnection } from './db/client.js';

import { registerCompanyTools } from './tools/companyTools.js';
import { registerFinancialTools } from './tools/financialTools.js';
import { registerStockTools } from './tools/stockTools.js';
import { registerAnalystTools } from './tools/analystTools.js';
import { registerSectorTools } from './tools/sectorTools.js';

async function main() {
  const dbConnected = await testConnection();
  if (!dbConnected) process.exit(1);

  const server = new Server(
    { name: 'financial-data-server', version: '1.0.0' },
    { capabilities: { tools: {} } }
  );

  registerCompanyTools(server);
  registerFinancialTools(server);
  registerStockTools(server);
  registerAnalystTools(server);
  registerSectorTools(server);

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      { name: 'get_company_profile' },
      { name: 'search_companies' },
      { name: 'get_financial_report' },
      { name: 'compare_companies' },
      { name: 'get_stock_price_history' },
      { name: 'get_analyst_ratings' },
      { name: 'screen_stocks' },
      { name: 'get_sector_overview' },
    ],
  }));

  const mode = process.argv[2];

  if (mode === 'sse') {
    const port = Number(process.argv[3]) || env.PORT || 3000;

    const httpServer = createServer(async (req, res) => {
      if (req.url === '/message') {
        const transport = new SSEServerTransport('/message', res);
        await server.connect(transport);
      }
    });

    httpServer.listen(port, () =>
      logger.info(`SSE running on http://localhost:${port}/message`)
    );
  } else {
    await server.connect(new StdioServerTransport());
    logger.info('MCP running in stdio mode');
  }
}

main();

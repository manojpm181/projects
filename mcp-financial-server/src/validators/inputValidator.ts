import { z } from 'zod';

export const validateCompanyProfile = (input: unknown) => {
  const schema = z.object({
    identifier: z.string().min(1, 'Identifier is required'),
  });
  return schema.parse(input);
};

export const validateSearchCompanies = (input: unknown) => {
  const schema = z.object({
    sector: z.string().optional(),
    industry: z.string().optional(),
    min_market_cap: z.coerce.number().optional(),
    max_market_cap: z.coerce.number().optional(),
    country: z.string().optional(),
  });
  return schema.parse(input);
};

export const validateFinancialReport = (input: unknown) => {
  const schema = z.object({
    ticker: z.string().min(1, 'Ticker is required'),
    fiscal_year: z.coerce.number().int().min(1900).max(2100).optional(),
    fiscal_quarter: z.enum(['Q1', 'Q2', 'Q3', 'Q4']).optional(),
  });
  return schema.parse(input);
};

export const validateCompareCompanies = (input: unknown) => {
  const schema = z.object({
    tickers: z.array(z.string().min(1)).min(2).max(5),
  });
  return schema.parse(input);
};

export const validateStockPriceHistory = (input: unknown) => {
  const schema = z.object({
    ticker: z.string().min(1, 'Ticker is required'),
    start_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
    end_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
    limit: z.coerce.number().int().min(1).max(1000).default(30),
  });
  return schema.parse(input);
};

export const validateAnalystRatings = (input: unknown) => {
  const schema = z.object({
    ticker: z.string().min(1, 'Ticker is required'),
    firm: z.string().optional(),
  });
  return schema.parse(input);
};

export const validateScreenStocks = (input: unknown) => {
  const schema = z.object({
    min_revenue: z.coerce.number().optional(),
    min_eps: z.coerce.number().optional(),
    min_gross_margin: z.coerce.number().min(0).max(100).optional(),
    max_debt_to_equity: z.coerce.number().optional(),
    sector: z.string().optional(),
    min_market_cap: z.coerce.number().optional(),
    max_market_cap: z.coerce.number().optional(),
  });
  return schema.parse(input);
};

export const validateSectorOverview = (input: unknown) => {
  const schema = z.object({
    sector: z.string().min(1, 'Sector is required'),
  });
  return schema.parse(input);
};
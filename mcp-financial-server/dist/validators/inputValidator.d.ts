export declare const validateCompanyProfile: (input: unknown) => {
    identifier: string;
};
export declare const validateSearchCompanies: (input: unknown) => {
    sector?: string | undefined;
    industry?: string | undefined;
    country?: string | undefined;
    min_market_cap?: number | undefined;
    max_market_cap?: number | undefined;
};
export declare const validateFinancialReport: (input: unknown) => {
    ticker: string;
    fiscal_year?: number | undefined;
    fiscal_quarter?: "Q1" | "Q2" | "Q3" | "Q4" | undefined;
};
export declare const validateCompareCompanies: (input: unknown) => {
    tickers: string[];
};
export declare const validateStockPriceHistory: (input: unknown) => {
    ticker: string;
    limit: number;
    start_date?: string | undefined;
    end_date?: string | undefined;
};
export declare const validateAnalystRatings: (input: unknown) => {
    ticker: string;
    firm?: string | undefined;
};
export declare const validateScreenStocks: (input: unknown) => {
    sector?: string | undefined;
    min_market_cap?: number | undefined;
    max_market_cap?: number | undefined;
    min_revenue?: number | undefined;
    min_eps?: number | undefined;
    min_gross_margin?: number | undefined;
    max_debt_to_equity?: number | undefined;
};
export declare const validateSectorOverview: (input: unknown) => {
    sector: string;
};
//# sourceMappingURL=inputValidator.d.ts.map
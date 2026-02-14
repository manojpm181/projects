-- Enable UUID extension

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies table

CREATE TABLE companies (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    ticker VARCHAR(10) NOT NULL UNIQUE,

    name VARCHAR(255) NOT NULL,

    sector VARCHAR(100) NOT NULL,

    industry VARCHAR(100) NOT NULL,

    market_cap BIGINT NOT NULL,

    country VARCHAR(50) NOT NULL,

    founded_year INTEGER,

    ceo VARCHAR(255),

    employees INTEGER,

    description TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW()

);

-- Financial reports table

CREATE TABLE financial_reports (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,

    fiscal_year INTEGER NOT NULL,

    fiscal_quarter VARCHAR(5) NOT NULL CHECK (fiscal_quarter IN ('Q1', 'Q2', 'Q3', 'Q4', 'FY')),

    revenue NUMERIC(15,2) NOT NULL,

    net_income NUMERIC(15,2) NOT NULL,

    eps NUMERIC(8,4),

    gross_margin NUMERIC(5,2),

    operating_margin NUMERIC(5,2),

    debt_to_equity NUMERIC(6,3),

    free_cash_flow NUMERIC(15,2),

    report_date DATE NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(company_id, fiscal_year, fiscal_quarter)

);

-- Stock prices table

CREATE TABLE stock_prices (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,

    date DATE NOT NULL,

    open NUMERIC(10,2) NOT NULL,

    high NUMERIC(10,2) NOT NULL,

    low NUMERIC(10,2) NOT NULL,

    close NUMERIC(10,2) NOT NULL,

    volume BIGINT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(company_id, date)

);

-- Analyst ratings table

CREATE TABLE analyst_ratings (

    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,

    analyst_firm VARCHAR(255) NOT NULL,

    rating VARCHAR(20) NOT NULL CHECK (rating IN ('Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell', 'Overweight', 'Underweight')),

    target_price NUMERIC(10,2),

    previous_rating VARCHAR(20),

    rating_date DATE NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- Create indexes

CREATE INDEX idx_companies_ticker ON companies(ticker);

CREATE INDEX idx_companies_sector ON companies(sector);

CREATE INDEX idx_financial_reports_company_id ON financial_reports(company_id);

CREATE INDEX idx_stock_prices_company_date ON stock_prices(company_id, date DESC);

CREATE INDEX idx_analyst_ratings_company_date ON analyst_ratings(company_id, rating_date DESC);

-- Enable RLS

ALTER TABLE companies ENABLE ROW LEVEL SECURITY;

ALTER TABLE financial_reports ENABLE ROW LEVEL SECURITY;

ALTER TABLE stock_prices ENABLE ROW LEVEL SECURITY;

ALTER TABLE analyst_ratings ENABLE ROW LEVEL SECURITY;

-- Create public read policies

CREATE POLICY "Allow public read access" ON companies FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON financial_reports FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON stock_prices FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON analyst_ratings FOR SELECT USING (true);
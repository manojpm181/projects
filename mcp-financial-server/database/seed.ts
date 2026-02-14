import { createClient } from '@supabase/supabase-js';

import { faker } from '@faker-js/faker';

import dotenv from 'dotenv';

dotenv.config();

const supabase = createClient(

  process.env.SUPABASE_URL!,

  process.env.SUPABASE_SERVICE_ROLE_KEY!

);

async function seedDatabase() {

  console.log('🚀 Starting database seeding...');

  

  // Insert 25 real companies

  const companies = [

    { ticker: 'AAPL', name: 'Apple Inc.', sector: 'Technology', industry: 'Consumer Electronics', country: 'US' },

    { ticker: 'MSFT', name: 'Microsoft Corporation', sector: 'Technology', industry: 'Software', country: 'US' },

    { ticker: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology', industry: 'Internet Services', country: 'US' },

    { ticker: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer', industry: 'E-Commerce', country: 'US' },

    { ticker: 'NVDA', name: 'NVIDIA Corporation', sector: 'Technology', industry: 'Semiconductors', country: 'US' },

    { ticker: 'META', name: 'Meta Platforms Inc.', sector: 'Technology', industry: 'Social Media', country: 'US' },

    { ticker: 'TSLA', name: 'Tesla Inc.', sector: 'Automotive', industry: 'Electric Vehicles', country: 'US' },

    { ticker: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Financial', industry: 'Banking', country: 'US' },

    { ticker: 'V', name: 'Visa Inc.', sector: 'Financial', industry: 'Financial Services', country: 'US' },

    { ticker: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare', industry: 'Pharmaceuticals', country: 'US' },

    { ticker: 'WMT', name: 'Walmart Inc.', sector: 'Consumer', industry: 'Retail', country: 'US' },

    { ticker: 'PG', name: 'Procter & Gamble Co.', sector: 'Consumer', industry: 'Consumer Goods', country: 'US' },

    { ticker: 'MA', name: 'Mastercard Incorporated', sector: 'Financial', industry: 'Financial Services', country: 'US' },

    { ticker: 'HD', name: 'Home Depot Inc.', sector: 'Consumer', industry: 'Retail', country: 'US' },

    { ticker: 'DIS', name: 'Walt Disney Company', sector: 'Entertainment', industry: 'Media', country: 'US' },

    { ticker: 'BAC', name: 'Bank of America Corp', sector: 'Financial', industry: 'Banking', country: 'US' },

    { ticker: 'ADBE', name: 'Adobe Inc.', sector: 'Technology', industry: 'Software', country: 'US' },

    { ticker: 'NFLX', name: 'Netflix Inc.', sector: 'Entertainment', industry: 'Streaming', country: 'US' },

    { ticker: 'CRM', name: 'Salesforce Inc.', sector: 'Technology', industry: 'Software', country: 'US' },

    { ticker: 'PEP', name: 'PepsiCo Inc.', sector: 'Consumer', industry: 'Beverages', country: 'US' },

    { ticker: 'KO', name: 'Coca-Cola Company', sector: 'Consumer', industry: 'Beverages', country: 'US' },

    { ticker: 'XOM', name: 'Exxon Mobil Corp', sector: 'Energy', industry: 'Oil & Gas', country: 'US' },

    { ticker: 'TMO', name: 'Thermo Fisher Scientific', sector: 'Healthcare', industry: 'Medical Devices', country: 'US' },

    { ticker: 'ABBV', name: 'AbbVie Inc.', sector: 'Healthcare', industry: 'Pharmaceuticals', country: 'US' },

    { ticker: 'AVGO', name: 'Broadcom Inc.', sector: 'Technology', industry: 'Semiconductors', country: 'US' },

  ];

  // Insert companies

  const companyData = companies.map(company => ({

    ...company,

    market_cap: faker.number.int({ min: 50_000_000_000, max: 3_000_000_000_000 }),

    founded_year: faker.number.int({ min: 1800, max: 2000 }),

    ceo: faker.person.fullName(),

    employees: faker.number.int({ min: 1000, max: 500000 }),

    description: faker.company.buzzPhrase()

  }));

  const { data: insertedCompanies, error } = await supabase
    .from('companies')
    .upsert(companyData, { onConflict: 'ticker' })
    .select();


  if (error) {

    console.error('Error inserting companies:', error);

    return;

  }

  console.log(`✅ Inserted ${insertedCompanies?.length} companies`);

  // Generate financial reports

  for (const company of insertedCompanies!) {

    const reports = [];

    for (let year = 2021; year <= 2023; year++) {

      for (const quarter of ['Q1', 'Q2', 'Q3', 'Q4']) {

        reports.push({

          company_id: company.id,

          fiscal_year: year,

          fiscal_quarter: quarter,

          revenue: faker.number.float({ min: 1000, max: 100000, fractionDigits:2 }),

          net_income: faker.number.float({ min: 100, max: 20000, fractionDigits:2 }),

          eps: faker.number.float({ min: 0.5, max: 15, fractionDigits:2 }),

          gross_margin: faker.number.float({ min: 30, max: 80, fractionDigits:2 }),

          operating_margin: faker.number.float({ min: 15, max: 40, fractionDigits:2 }),

          debt_to_equity: faker.number.float({ min: 0.1, max: 2.0, fractionDigits: 3 }),

          free_cash_flow: faker.number.float({ min: 500, max: 15000, fractionDigits:2 }),

          report_date: `${year}-${quarter === 'Q1' ? '03-31' : quarter === 'Q2' ? '06-30' : quarter === 'Q3' ? '09-30' : '12-31'}`

        });

      }

    }

    

    await supabase.from('financial_reports').insert(reports);

  }

  

  console.log('✅ Generated financial reports');

  // Generate stock prices

  for (const company of insertedCompanies!) {

    const prices = [];

    const startDate = new Date('2023-01-01');

    

    for (let i = 0; i < 90; i++) {

      const date = new Date(startDate);

      date.setDate(startDate.getDate() + i);

      if (date.getDay() === 0 || date.getDay() === 6) continue; // Skip weekends

      

      prices.push({

        company_id: company.id,

        date: date.toISOString().split('T')[0],

        open: faker.number.float({ min: 50, max: 500, fractionDigits:2 }),

        high: faker.number.float({ min: 50, max: 500, fractionDigits:2 }),

        low: faker.number.float({ min: 50, max: 500, fractionDigits:2 }),

        close: faker.number.float({ min: 50, max: 500, fractionDigits:2 }),

        volume: faker.number.int({ min: 1000000, max: 100000000 })

      });

    }

    

    await supabase.from('stock_prices').insert(prices);

  }

  

  console.log('✅ Generated stock prices');

  // Generate analyst ratings

  const firms = ['Morgan Stanley', 'Goldman Sachs', 'JP Morgan', 'Bank of America', 'Citigroup'];

  for (const company of insertedCompanies!) {

    const ratings = [];

    

    for (let i = 0; i < 5; i++) {

      ratings.push({

        company_id: company.id,

        analyst_firm: firms[i],

        rating: faker.helpers.arrayElement(['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']),

        target_price: faker.number.float({ min: 50, max: 500, fractionDigits:2 }),

        rating_date: faker.date.between({ from: '2023-01-01', to: '2024-01-01' }).toISOString().split('T')[0]

      });

    }

    

    await supabase.from('analyst_ratings').insert(ratings);

  }

  

  console.log('✅ Generated analyst ratings');

  console.log('🎉 Database seeding completed!');

}
void seedDatabase().catch((err) => {
  console.error('Seeding failed:', err);
});


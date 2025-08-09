"""
Data Generator for Confectionery Sales Analysis
Generates realistic sample sales data for Orion Food Vina, Kido, and Kinh Do brands (2010-2020)
"""

import pandas as pd
import numpy as np
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

class ConfectionerySalesDataGenerator:
    def __init__(self, start_year=2010, end_year=2020):
        self.start_year = start_year
        self.end_year = end_year
        self.brands = {
            1: {'name': 'Orion Food Vina', 'code': 'OFV', 'base_growth': 0.12},
            2: {'name': 'Kido', 'code': 'KDO', 'base_growth': 0.08}, 
            3: {'name': 'Kinh Do', 'code': 'KDD', 'base_growth': 0.06}
        }
        self.products = {
            # Orion Food Vina products
            1: {'name': 'Choco Pie Original', 'brand_id': 1, 'category_id': 4, 'base_price': 15000, 'seasonality': 1.0},
            2: {'name': 'O-Star Chocolate', 'brand_id': 1, 'category_id': 1, 'base_price': 8000, 'seasonality': 1.2},
            3: {'name': 'Potato Snack', 'brand_id': 1, 'category_id': 5, 'base_price': 12000, 'seasonality': 0.9},
            4: {'name': 'Marine Boy Gum', 'brand_id': 1, 'category_id': 2, 'base_price': 3000, 'seasonality': 1.0},
            
            # Kido products  
            5: {'name': 'Richeese Crackers', 'brand_id': 2, 'category_id': 5, 'base_price': 18000, 'seasonality': 0.8},
            6: {'name': 'Solite Cake', 'brand_id': 2, 'category_id': 4, 'base_price': 25000, 'seasonality': 1.1},
            7: {'name': 'Soft Candy Mix', 'brand_id': 2, 'category_id': 2, 'base_price': 10000, 'seasonality': 1.0},
            8: {'name': 'Butter Cookies', 'brand_id': 2, 'category_id': 3, 'base_price': 35000, 'seasonality': 1.3},
            
            # Kinh Do products
            9: {'name': 'Moon Cake Traditional', 'brand_id': 3, 'category_id': 6, 'base_price': 120000, 'seasonality': 2.5},
            10: {'name': 'Coconut Cookies', 'brand_id': 3, 'category_id': 3, 'base_price': 45000, 'seasonality': 1.2},
            11: {'name': 'Royal Jelly Candy', 'brand_id': 3, 'category_id': 2, 'base_price': 15000, 'seasonality': 1.0},
            12: {'name': 'Green Bean Cake', 'brand_id': 3, 'category_id': 6, 'base_price': 80000, 'seasonality': 1.8},
        }
        self.regions = ['North', 'Central', 'South']
        self.sales_channels = ['Supermarket', 'Convenience Store', 'Traditional Market', 'Online']
        
    def generate_sales_data(self, num_records=50000):
        """Generate sales data for the specified period"""
        sales_data = []
        
        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13):
                for product_id, product_info in self.products.items():
                    brand_info = self.brands[product_info['brand_id']]
                    
                    # Calculate number of sales transactions for this product/month
                    base_transactions = random.randint(50, 200)
                    
                    # Apply growth trend
                    years_from_start = year - self.start_year
                    growth_factor = (1 + brand_info['base_growth']) ** years_from_start
                    
                    # Apply seasonality (higher sales in Q4 for most products)
                    seasonal_factor = product_info['seasonality']
                    if month in [10, 11, 12]:  # Q4 seasonal boost
                        seasonal_factor *= 1.4
                    elif month in [1, 2]:  # Post-holiday decline
                        seasonal_factor *= 0.7
                        
                    transactions = int(base_transactions * growth_factor * seasonal_factor)
                    
                    for _ in range(transactions):
                        # Generate random sale date within the month
                        days_in_month = 28 if month == 2 else 30 if month in [4,6,9,11] else 31
                        day = random.randint(1, days_in_month)
                        sale_date = f"{year}-{month:02d}-{day:02d}"
                        
                        # Generate units sold (varying by transaction)
                        units_sold = random.randint(1, 10)
                        
                        # Calculate price with some variation
                        unit_price = product_info['base_price'] * random.uniform(0.9, 1.1)
                        revenue = units_sold * unit_price
                        
                        # Calculate costs and profit
                        cost_percentage = random.uniform(0.6, 0.75)
                        cost_of_goods = revenue * cost_percentage
                        profit = revenue - cost_of_goods
                        
                        # Assign random region and sales channel
                        region = random.choice(self.regions)
                        sales_channel = random.choice(self.sales_channels)
                        
                        quarter = (month - 1) // 3 + 1
                        
                        sales_data.append({
                            'product_id': product_id,
                            'sale_date': sale_date,
                            'year': year,
                            'month': month,
                            'quarter': quarter,
                            'units_sold': units_sold,
                            'revenue': round(revenue, 2),
                            'cost_of_goods': round(cost_of_goods, 2),
                            'profit': round(profit, 2),
                            'region': region,
                            'sales_channel': sales_channel
                        })
        
        return pd.DataFrame(sales_data)
    
    def generate_market_share_data(self):
        """Generate market share data for each brand by year"""
        market_share_data = []
        
        # Base market shares (approximated)
        base_shares = {1: 35, 2: 30, 3: 25}  # Remaining 10% for other brands
        
        for year in range(self.start_year, self.end_year + 1):
            total_market_size = 1000000000 * (1.08 ** (year - self.start_year))  # 8% annual market growth
            
            for brand_id, base_share in base_shares.items():
                # Add some variation to market share over time
                share_variation = random.uniform(-2, 2)
                market_share = base_share + share_variation
                brand_revenue = total_market_size * (market_share / 100)
                
                for quarter in range(1, 5):
                    quarterly_variation = random.uniform(0.8, 1.2)
                    quarterly_share = market_share * quarterly_variation
                    quarterly_revenue = brand_revenue / 4 * quarterly_variation
                    
                    market_share_data.append({
                        'brand_id': brand_id,
                        'year': year,
                        'quarter': quarter,
                        'market_share_percentage': round(quarterly_share, 2),
                        'total_market_size': round(total_market_size, 2),
                        'brand_revenue': round(quarterly_revenue, 2)
                    })
        
        return pd.DataFrame(market_share_data)
    
    def save_to_csv(self, sales_df, market_share_df):
        """Save generated data to CSV files"""
        data_dir = Path('data/sample_data')
        data_dir.mkdir(parents=True, exist_ok=True)
        
        sales_df.to_csv(data_dir / 'sales_data.csv', index=False)
        market_share_df.to_csv(data_dir / 'market_share_data.csv', index=False)
        
        print(f"Sales data saved: {len(sales_df)} records")
        print(f"Market share data saved: {len(market_share_df)} records")
    
    def save_to_database(self, sales_df, market_share_df, db_path='data/confectionery_sales.db'):
        """Save generated data to SQLite database"""
        conn = sqlite3.connect(db_path)
        
        # Load and execute schema
        with open('sql/create_tables.sql', 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        
        # Load and execute data insertion
        with open('sql/data_insertion.sql', 'r') as f:
            data_sql = f.read()
        conn.executescript(data_sql)
        
        # Insert generated data
        sales_df.to_sql('sales', conn, if_exists='append', index=False)
        market_share_df.to_sql('market_share', conn, if_exists='append', index=False)
        
        conn.close()
        print(f"Data saved to database: {db_path}")

def main():
    """Main function to generate and save data"""
    print("Generating confectionery sales data (2010-2020)...")
    
    generator = ConfectionerySalesDataGenerator()
    
    # Generate data
    sales_data = generator.generate_sales_data()
    market_share_data = generator.generate_market_share_data()
    
    # Save to files
    generator.save_to_csv(sales_data, market_share_data)
    generator.save_to_database(sales_data, market_share_data)
    
    print("Data generation completed successfully!")
    print(f"Generated {len(sales_data)} sales records and {len(market_share_data)} market share records")

if __name__ == "__main__":
    main()

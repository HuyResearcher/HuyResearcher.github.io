"""
Database Manager for Confectionery Sales Analysis
Handles database connections, queries, and data operations
"""

import sqlite3
import pandas as pd
from pathlib import Path
import logging

class DatabaseManager:
    def __init__(self, db_path='data/confectionery_sales.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            logging.info(f"Connected to database: {self.db_path}")
            return self.connection
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            return None
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SQL query and return results as DataFrame"""
        try:
            if not self.connection:
                self.connect()
            
            if params:
                df = pd.read_sql_query(query, self.connection, params=params)
            else:
                df = pd.read_sql_query(query, self.connection)
            
            return df
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            return None
    
    def execute_script(self, script_path):
        """Execute SQL script from file"""
        try:
            if not self.connection:
                self.connect()
            
            with open(script_path, 'r') as f:
                script = f.read()
            
            self.connection.executescript(script)
            self.connection.commit()
            logging.info(f"Script executed successfully: {script_path}")
            return True
        except Exception as e:
            logging.error(f"Error executing script: {e}")
            return False
    
    def get_annual_revenue_by_brand(self, start_year=2010, end_year=2020):
        """Get annual revenue data by brand"""
        query = """
        SELECT 
            b.brand_name,
            s.year,
            SUM(s.revenue) as total_revenue,
            COUNT(DISTINCT s.product_id) as products_sold,
            SUM(s.units_sold) as total_units
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE s.year BETWEEN ? AND ?
        GROUP BY b.brand_name, s.year
        ORDER BY b.brand_name, s.year
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_market_share_data(self, start_year=2010, end_year=2020):
        """Get market share data by brand"""
        query = """
        SELECT 
            b.brand_name,
            ms.year,
            AVG(ms.market_share_percentage) as avg_market_share,
            SUM(ms.brand_revenue) as total_brand_revenue,
            AVG(ms.total_market_size) as avg_market_size
        FROM market_share ms
        JOIN brands b ON ms.brand_id = b.brand_id
        WHERE ms.year BETWEEN ? AND ?
        GROUP BY b.brand_name, ms.year
        ORDER BY ms.year, avg_market_share DESC
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_product_performance(self, start_year=2010, end_year=2020):
        """Get product performance data"""
        query = """
        SELECT 
            b.brand_name,
            p.product_name,
            pc.category_name,
            SUM(s.revenue) as total_revenue,
            SUM(s.units_sold) as total_units,
            AVG(s.revenue/s.units_sold) as avg_price_per_unit,
            SUM(s.profit) as total_profit,
            ROUND((SUM(s.profit) / SUM(s.revenue)) * 100, 2) as profit_margin
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN product_categories pc ON p.category_id = pc.category_id
        WHERE s.year BETWEEN ? AND ?
        GROUP BY b.brand_name, p.product_name, pc.category_name
        ORDER BY total_revenue DESC
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_seasonal_analysis(self, start_year=2010, end_year=2020):
        """Get seasonal sales pattern analysis"""
        query = """
        SELECT 
            b.brand_name,
            s.quarter,
            AVG(s.revenue) as avg_quarterly_revenue,
            SUM(s.revenue) as total_revenue,
            COUNT(*) as sales_transactions
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE s.year BETWEEN ? AND ?
        GROUP BY b.brand_name, s.quarter
        ORDER BY b.brand_name, s.quarter
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_yoy_growth(self, start_year=2010, end_year=2020):
        """Get year-over-year growth analysis"""
        query = """
        WITH yearly_revenue AS (
            SELECT 
                b.brand_name,
                s.year,
                SUM(s.revenue) as revenue
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            JOIN brands b ON p.brand_id = b.brand_id
            WHERE s.year BETWEEN ? AND ?
            GROUP BY b.brand_name, s.year
        )
        SELECT 
            brand_name,
            year,
            revenue,
            LAG(revenue) OVER (PARTITION BY brand_name ORDER BY year) as prev_year_revenue,
            CASE 
                WHEN LAG(revenue) OVER (PARTITION BY brand_name ORDER BY year) IS NOT NULL
                THEN ROUND(((revenue - LAG(revenue) OVER (PARTITION BY brand_name ORDER BY year)) / 
                            LAG(revenue) OVER (PARTITION BY brand_name ORDER BY year)) * 100, 2)
                ELSE NULL 
            END as yoy_growth_rate
        FROM yearly_revenue
        ORDER BY brand_name, year
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_category_analysis(self, start_year=2010, end_year=2020):
        """Get product category performance analysis"""
        query = """
        SELECT 
            b.brand_name,
            pc.category_name,
            SUM(s.revenue) as total_revenue,
            ROUND(SUM(s.revenue) * 100.0 / SUM(SUM(s.revenue)) OVER (PARTITION BY b.brand_name), 2) as revenue_percentage,
            SUM(s.units_sold) as total_units
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN product_categories pc ON p.category_id = pc.category_id
        WHERE s.year BETWEEN ? AND ?
        GROUP BY b.brand_name, pc.category_name
        ORDER BY b.brand_name, total_revenue DESC
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_regional_performance(self, start_year=2010, end_year=2020):
        """Get regional sales performance"""
        query = """
        SELECT 
            b.brand_name,
            s.region,
            SUM(s.revenue) as total_revenue,
            SUM(s.units_sold) as total_units,
            COUNT(DISTINCT s.product_id) as unique_products,
            ROUND(AVG(s.revenue), 2) as avg_transaction_value
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE s.year BETWEEN ? AND ?
        GROUP BY b.brand_name, s.region
        ORDER BY b.brand_name, total_revenue DESC
        """
        return self.execute_query(query, (start_year, end_year))
    
    def get_brand_comparison(self, start_year=2010, end_year=2020):
        """Get comprehensive brand comparison"""
        query = """
        SELECT 
            b.brand_name,
            SUM(s.revenue) as total_revenue,
            SUM(s.units_sold) as total_units,
            COUNT(DISTINCT p.product_id) as product_portfolio_size,
            ROUND(AVG(s.revenue/s.units_sold), 2) as avg_unit_price,
            SUM(s.profit) as total_profit,
            ROUND((SUM(s.profit) / SUM(s.revenue)) * 100, 2) as profit_margin,
            RANK() OVER (ORDER BY SUM(s.revenue) DESC) as revenue_rank,
            RANK() OVER (ORDER BY SUM(s.units_sold) DESC) as volume_rank
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE s.year BETWEEN ? AND ?
        GROUP BY b.brand_name
        ORDER BY total_revenue DESC
        """
        return self.execute_query(query, (start_year, end_year))
    
    def create_summary_statistics(self):
        """Generate summary statistics for the dataset"""
        stats = {}
        
        # Basic counts
        stats['total_sales_records'] = self.execute_query("SELECT COUNT(*) as count FROM sales").iloc[0]['count']
        stats['total_products'] = self.execute_query("SELECT COUNT(*) as count FROM products").iloc[0]['count']
        stats['total_brands'] = self.execute_query("SELECT COUNT(*) as count FROM brands").iloc[0]['count']
        
        # Date range
        date_range = self.execute_query("SELECT MIN(year) as min_year, MAX(year) as max_year FROM sales")
        stats['date_range'] = f"{date_range.iloc[0]['min_year']}-{date_range.iloc[0]['max_year']}"
        
        # Revenue totals
        revenue_total = self.execute_query("SELECT SUM(revenue) as total FROM sales")
        stats['total_revenue'] = revenue_total.iloc[0]['total']
        
        return stats

# Usage example and testing
def main():
    """Test database operations"""
    db = DatabaseManager()
    
    # Test connection
    if db.connect():
        print("Database connection successful")
        
        # Get summary statistics
        stats = db.create_summary_statistics()
        print("\nDataset Summary:")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Test some queries
        print("\nTesting queries...")
        revenue_data = db.get_annual_revenue_by_brand()
        print(f"Annual revenue data shape: {revenue_data.shape if revenue_data is not None else 'None'}")
        
        db.disconnect()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    main()

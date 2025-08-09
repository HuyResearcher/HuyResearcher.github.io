-- Database Schema for Confectionery Sales Analysis
-- Creates tables for sales data analysis of Orion Food Vina, Kido, and Kinh Do

-- Create brands table
CREATE TABLE IF NOT EXISTS brands (
    brand_id INTEGER PRIMARY KEY,
    brand_name VARCHAR(50) NOT NULL,
    brand_code VARCHAR(10) NOT NULL,
    founded_year INTEGER,
    headquarters VARCHAR(100),
    description TEXT
);

-- Create product categories table
CREATE TABLE IF NOT EXISTS product_categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    category_description TEXT
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    brand_id INTEGER,
    category_id INTEGER,
    launch_date DATE,
    unit_price DECIMAL(10,2),
    package_size VARCHAR(50),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES product_categories(category_id)
);

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sale_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    units_sold INTEGER NOT NULL,
    revenue DECIMAL(15,2) NOT NULL,
    cost_of_goods DECIMAL(15,2),
    profit DECIMAL(15,2),
    region VARCHAR(50),
    sales_channel VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create market share table
CREATE TABLE IF NOT EXISTS market_share (
    market_share_id INTEGER PRIMARY KEY,
    brand_id INTEGER,
    year INTEGER NOT NULL,
    quarter INTEGER,
    market_share_percentage DECIMAL(5,2),
    total_market_size DECIMAL(15,2),
    brand_revenue DECIMAL(15,2),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_year ON sales(year);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_id);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand_id);
CREATE INDEX IF NOT EXISTS idx_market_share_brand_year ON market_share(brand_id, year);

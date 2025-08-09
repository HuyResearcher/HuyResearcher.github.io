-- Comprehensive SQL Analysis Queries for Confectionery Sales Performance

-- 1. REVENUE TREND ANALYSIS
-- Annual revenue by brand
SELECT 
    b.brand_name,
    s.year,
    SUM(s.revenue) as total_revenue,
    COUNT(DISTINCT s.product_id) as products_sold,
    SUM(s.units_sold) as total_units
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, s.year
ORDER BY b.brand_name, s.year;

-- 2. MARKET SHARE ANALYSIS
-- Market share percentage by brand over years
SELECT 
    b.brand_name,
    ms.year,
    ms.market_share_percentage,
    ms.brand_revenue,
    ms.total_market_size
FROM market_share ms
JOIN brands b ON ms.brand_id = b.brand_id
WHERE ms.year BETWEEN 2010 AND 2020
ORDER BY ms.year, ms.market_share_percentage DESC;

-- 3. PRODUCT PERFORMANCE ANALYSIS
-- Top performing products by revenue
SELECT 
    b.brand_name,
    p.product_name,
    pc.category_name,
    SUM(s.revenue) as total_revenue,
    SUM(s.units_sold) as total_units,
    AVG(s.revenue/s.units_sold) as avg_price_per_unit
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
JOIN product_categories pc ON p.category_id = pc.category_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, p.product_name, pc.category_name
ORDER BY total_revenue DESC;

-- 4. SEASONAL ANALYSIS
-- Quarterly sales patterns
SELECT 
    b.brand_name,
    s.quarter,
    AVG(s.revenue) as avg_quarterly_revenue,
    SUM(s.revenue) as total_revenue,
    COUNT(*) as sales_transactions
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, s.quarter
ORDER BY b.brand_name, s.quarter;

-- 5. YEAR-OVER-YEAR GROWTH ANALYSIS
-- YoY growth rate calculation
WITH yearly_revenue AS (
    SELECT 
        b.brand_name,
        s.year,
        SUM(s.revenue) as revenue
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    JOIN brands b ON p.brand_id = b.brand_id
    WHERE s.year BETWEEN 2010 AND 2020
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
ORDER BY brand_name, year;

-- 6. CATEGORY ANALYSIS
-- Revenue distribution by product category
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
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, pc.category_name
ORDER BY b.brand_name, total_revenue DESC;

-- 7. PROFITABILITY ANALYSIS
-- Profit margins by brand and year
SELECT 
    b.brand_name,
    s.year,
    SUM(s.revenue) as total_revenue,
    SUM(s.cost_of_goods) as total_cogs,
    SUM(s.profit) as total_profit,
    ROUND((SUM(s.profit) / SUM(s.revenue)) * 100, 2) as profit_margin_percentage
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, s.year
ORDER BY b.brand_name, s.year;

-- 8. REGIONAL PERFORMANCE
-- Sales performance by region
SELECT 
    b.brand_name,
    s.region,
    SUM(s.revenue) as total_revenue,
    SUM(s.units_sold) as total_units,
    COUNT(DISTINCT s.product_id) as unique_products
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, s.region
ORDER BY b.brand_name, total_revenue DESC;

-- 9. SALES CHANNEL ANALYSIS
-- Performance across different sales channels
SELECT 
    b.brand_name,
    s.sales_channel,
    SUM(s.revenue) as total_revenue,
    ROUND(AVG(s.revenue), 2) as avg_transaction_value,
    COUNT(*) as transaction_count
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name, s.sales_channel
ORDER BY b.brand_name, total_revenue DESC;

-- 10. COMPETITIVE ANALYSIS
-- Brand ranking by key metrics
SELECT 
    b.brand_name,
    SUM(s.revenue) as total_revenue,
    SUM(s.units_sold) as total_units,
    COUNT(DISTINCT p.product_id) as product_portfolio_size,
    ROUND(AVG(s.revenue/s.units_sold), 2) as avg_unit_price,
    RANK() OVER (ORDER BY SUM(s.revenue) DESC) as revenue_rank,
    RANK() OVER (ORDER BY SUM(s.units_sold) DESC) as volume_rank
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN brands b ON p.brand_id = b.brand_id
WHERE s.year BETWEEN 2010 AND 2020
GROUP BY b.brand_name
ORDER BY total_revenue DESC;

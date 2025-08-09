-- Sample data insertion for confectionery brands analysis

-- Insert brand data
INSERT INTO brands (brand_id, brand_name, brand_code, founded_year, headquarters, description) VALUES
(1, 'Orion Food Vina', 'OFV', 1999, 'Ho Chi Minh City, Vietnam', 'Vietnamese subsidiary of Korean Orion Corporation, specializing in confectionery and snacks'),
(2, 'Kido', 'KDO', 1993, 'Ho Chi Minh City, Vietnam', 'Leading Vietnamese food and confectionery company known for cakes and candies'),
(3, 'Kinh Do', 'KDD', 1993, 'Ho Chi Minh City, Vietnam', 'Premier Vietnamese confectionery brand famous for moon cakes and traditional sweets');

-- Insert product categories
INSERT INTO product_categories (category_id, category_name, category_description) VALUES
(1, 'Chocolates', 'Chocolate bars, pralines, and chocolate confections'),
(2, 'Candies', 'Hard candies, gummies, and chewy confections'),
(3, 'Cookies & Biscuits', 'Various types of cookies and biscuits'),
(4, 'Cakes', 'Fresh cakes, moon cakes, and packaged cake products'),
(5, 'Snacks', 'Crackers, chips, and other savory snacks'),
(6, 'Traditional Sweets', 'Vietnamese traditional confectionery items');

-- Insert sample products for each brand
INSERT INTO products (product_id, product_name, brand_id, category_id, launch_date, unit_price, package_size) VALUES
-- Orion Food Vina products
(1, 'Choco Pie Original', 1, 4, '2000-01-15', 15000, '12 pieces'),
(2, 'O-Star Chocolate', 1, 1, '2001-03-20', 8000, '50g'),
(3, 'Potato Snack', 1, 5, '2002-06-10', 12000, '60g'),
(4, 'Marine Boy Gum', 1, 2, '2003-09-05', 3000, '10 pieces'),

-- Kido products  
(5, 'Richeese Crackers', 2, 5, '1995-05-12', 18000, '135g'),
(6, 'Solite Cake', 2, 4, '1998-11-20', 25000, '240g'),
(7, 'Soft Candy Mix', 2, 2, '2000-07-15', 10000, '100g'),
(8, 'Butter Cookies', 2, 3, '2001-12-01', 35000, '200g'),

-- Kinh Do products
(9, 'Moon Cake Traditional', 3, 6, '1995-08-20', 120000, '4 pieces'),
(10, 'Coconut Cookies', 3, 3, '1996-02-14', 45000, '300g'),
(11, 'Royal Jelly Candy', 3, 2, '1999-04-10', 15000, '150g'),
(12, 'Green Bean Cake', 3, 6, '2000-09-25', 80000, '6 pieces');

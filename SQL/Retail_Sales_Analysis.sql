
-- RETAIL SALES & BUSINESS PERFORMANCE ANALYTICS
-- Database: retail_analytics
-- Table: superstore

USE retail_analytics;

-- 1. Total Sales, Profit and Orders
SELECT
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(DISTINCT `Order ID`) AS Total_Orders
FROM superstore;

-- 2. Sales by Category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC;

-- 3. Profit by Category
SELECT
    Category,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY Category
ORDER BY Total_Profit DESC;

-- 4. Sales by Region
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC;

-- 5. Top 10 Customers by Sales
SELECT
    `Customer Name`,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore
GROUP BY `Customer Name`
ORDER BY Total_Sales DESC
LIMIT 10;

-- 6. Profit by Sub-Category
SELECT
    `Sub-Category`,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY `Sub-Category`
ORDER BY Total_Profit DESC;

-- 7. Monthly Sales Trend
SELECT
    DATE_FORMAT(`Order Date`, '%Y-%m') AS Sales_Month,
    ROUND(SUM(Sales), 2) AS Monthly_Sales
FROM superstore
GROUP BY Sales_Month
ORDER BY Sales_Month;

-- 8. Sales by Customer Segment
SELECT
    Segment,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore
GROUP BY Segment
ORDER BY Total_Sales DESC;

-- 9. Sales by Shipping Mode
SELECT
    `Ship Mode`,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore
GROUP BY `Ship Mode`
ORDER BY Total_Sales DESC;

-- 10. Overall Profit Margin
SELECT
    ROUND(
        (SUM(Profit) / NULLIF(SUM(Sales), 0)) * 100,
        2
    ) AS Profit_Margin_Percentage
FROM superstore;

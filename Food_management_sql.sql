# creatinng database 

create database food_waste_management;
use food_waste_management;

SELECT COUNT(*) FROM claims_data_cleaned;
SELECT COUNT(*) FROM food_listings_data;

CREATE TABLE providers_data (
    Provider_ID INT,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address VARCHAR(255),
    City VARCHAR(100),
    Contact VARCHAR(100)
);

CREATE TABLE receivers_data (
    Receiver_ID INT,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(100)
);

SHOW VARIABLES LIKE 'local_infile';


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/providers_data.csv'
INTO TABLE providers_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/receivers_data.csv'
INTO TABLE receivers_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

SHOW VARIABLES LIKE 'secure_file_priv';

SELECT COUNT(*) FROM providers_data;
SELECT COUNT(*) FROM receivers_data;


USE food_waste_management;

# Query 1: Total Records 

SELECT COUNT(*) AS Total_Providers
FROM providers_data;
SELECT COUNT(*) AS Total_Receivers
FROM receivers_data;
SELECT COUNT(*) AS Total_Food_Listings
FROM food_listings_data;
SELECT COUNT(*) AS Total_Claims
FROM claims_data_cleaned;


# Query 2: Provider Type Distribution

SELECT Type,
COUNT(*) AS Total_Providers
FROM Providers_data
GROUP BY Type
ORDER BY Total_Providers DESC ;

# Query 3: Receiver Type Distribution

SELECT Type,
COUNT(*) AS Total_Receivers
FROM receivers_data
GROUP BY Type
ORDER BY Total_Receivers DESC;

# Query 4: Food Type Distribution

SELECT Food_Type,
COUNT(*) AS Total_Food
FROM food_listings_data
GROUP BY Food_Type
ORDER BY Total_Food DESC;

# Query 5: Meal Type Distribution

SELECT Meal_Type,
COUNT(*) AS Total_Meal
FROM food_listings_data
GROUP BY Meal_Type
ORDER BY Total_Meal DESC;

# Query 6: Top 10 Cities by Food Listings

SELECT Location,
COUNT(*) AS Total_listings
FROM food_listings_data
GROUP BY Location
ORDER BY Total_listings DESC 
LIMIT 10 ;

# Query 7: Total Quantity Available

SELECT SUM(Quantity) AS Total_Quantity
FROM food_listings_data;


# Query 8: Claim Status Distribution

SELECT Status,
COUNT(*) AS Total_Claims
FROM claims_data_cleaned
GROUP BY Status;

# Query 9: Top 10 Most Claimed Food Items

SELECT Food_ID,
COUNT(*) AS Total_Claims
FROM claims_data_cleaned
GROUP BY Food_ID
ORDER BY Total_Claims DESC
LIMIT 10;

# Query 10: Top 10 Receivers by Claims

SELECT Receiver_ID,
COUNT(*) AS Total_Claims
FROM claims_data_cleaned
GROUP BY Receiver_ID
ORDER BY Total_Claims DESC
LIMIT 10;

# Query 11: Provider Type vs Quantity - JOIN QUERY

SELECT
Provider_Type,
SUM(Quantity) AS Total_Quantity
FROM food_listings_data
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;

# Query 12: Food Type vs Quantity

SELECT
Food_Type,
SUM(Quantity) AS Total_Quantity
FROM food_listings_data
GROUP BY Food_Type
ORDER BY Total_Quantity DESC;

# Query 13: Meal Type vs Quantity

SELECT
Meal_Type,
SUM(Quantity) AS Total_Quantity
FROM food_listings_data
GROUP BY Meal_Type
ORDER BY Total_Quantity DESC;

# Query 14: Top Providers by Quantity Donated

SELECT
Provider_ID,
SUM(Quantity) AS Total_Donated
FROM food_listings_data
GROUP BY Provider_ID
ORDER BY Total_Donated DESC
LIMIT 10;

# Query 15: Top Receivers by Quantity Claimed

SELECT
c.Receiver_ID,
SUM(f.Quantity) AS Total_Claimed
FROM claims_data_cleaned c
JOIN food_listings_data f
ON c.Food_ID = f.Food_ID
GROUP BY c.Receiver_ID
ORDER BY Total_Claimed DESC
LIMIT 10;
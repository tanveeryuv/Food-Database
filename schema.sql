
DROP TABLE IF EXISTS foods;

CREATE TABLE foods (
id SERIAL PRIMARY KEY,
barcode TEXT UNIQUE, -- Open Food Facts product code
product_name TEXT,
brand TEXT,
category TEXT,
calories DECIMAL,
fat DECIMAL,
sugar DECIMAL,
protein DECIMAL,
salt DECIMAL,
fiber DECIMAL,
nutriscore_grade TEXT,
ecoscore_grade TEXT,
ingredients TEXT,
country TEXT,
image_url TEXT,
insights TEXT,
imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_food_category ON foods using HASH (category);
CREATE INDEX idx_food_country ON foods using HASH (country);

CREATE INDEX idx_foods_calories ON foods (calories);
CREATE INDEX idx_foods_fat ON foods (fat);
CREATE INDEX idx_foods_sugar ON foods (sugar);
CREATE INDEX idx_foods_protein ON foods (protein);
CREATE INDEX idx_foods_salt ON foods (salt);
CREATE INDEX idx_foods_fiber ON foods (fiber);

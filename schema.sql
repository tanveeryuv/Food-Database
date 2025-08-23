-- Enable extensions (optional but nice to have)
-- CREATE EXTENSION IF NOT EXISTS pg_trgm; -- enables fast ILIKE searches (optional)
-- CREATE EXTENSION IF NOT EXISTS unaccent; -- better text search (optional)


CREATE TABLE IF NOT EXISTS foods (
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


-- Speed up common filters
CREATE INDEX IF NOT EXISTS idx_foods_calories ON foods (calories);
CREATE INDEX IF NOT EXISTS idx_foods_protein ON foods (protein);
CREATE INDEX IF NOT EXISTS idx_foods_sugar ON foods (sugar);
CREATE INDEX IF NOT EXISTS idx_foods_nutriscore ON foods (nutriscore_grade);


-- Full‑text search on ingredients (works without extensions)
CREATE INDEX IF NOT EXISTS idx_foods_ingredients_fts
ON foods USING GIN (to_tsvector('english', ingredients));


-- Optional: faster ILIKE on ingredients if pg_trgm enabled
-- CREATE INDEX IF NOT EXISTS idx_foods_ingredients_trgm
-- ON foods USING GIN (ingredients gin_trgm_ops);
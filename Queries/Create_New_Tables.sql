---------------------------------- Create New Tabels ------------------------------------------------
-- Create the Category_table
CREATE TABLE category_table (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE
);

-- Populate the Category_table with unique categories from google_play_apps
INSERT INTO category_table (category_name)
SELECT DISTINCT category
FROM google_play_apps
WHERE category IS NOT NULL;

-- Create the developers_table
CREATE TABLE developers_table (
    developer_id SERIAL PRIMARY KEY,
    developer_name VARCHAR(255) NOT NULL UNIQUE,
    developer_website VARCHAR(255),
    developer_email VARCHAR(255)
);

-- Populate the developers_table with unique developers from google_play_apps
INSERT INTO developers_table (developer_name, developer_website, developer_email)
SELECT DISTINCT developer_id, developer_website, developer_email
FROM google_play_apps
WHERE developer_id IS NOT NULL
ON CONFLICT (developer_name) DO NOTHING;

---------------------------------- Modify Existing Tabels ------------------------------------------------
-- Update the google_play_apps table to reference the new tables
ALTER TABLE google_play_apps
ADD COLUMN category_id INT,
ADD COLUMN developer_id_new INT;

-- Update the google_play_apps table to set category_id based on category_table
UPDATE google_play_apps
SET category_id = (
    SELECT category_id
    FROM category_table
    WHERE google_play_apps.category = category_table.category_name
);

-- Update the google_play_apps table to set developer_id_new based on developers_table
UPDATE google_play_apps
SET developer_id_new = (
    SELECT developer_id
    FROM developers_table
    WHERE google_play_apps.developer_id = developers_table.developer_name
);

-- Remove the old developer_id column
ALTER TABLE google_play_apps
DROP COLUMN developer_id;

-- Rename the new developer_id_new column
ALTER TABLE google_play_apps
RENAME COLUMN developer_id_new TO developer_id;


USE forkast;

CREATE TABLE IF NOT EXISTS recipes (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    ingredients TEXT,
    directions TEXT,
    link VARCHAR(255),
    source VARCHAR(100),
    NER TEXT
);

LOAD DATA INFILE '/var/lib/mysql-files/recipe.csv'
INTO TABLE recipes
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, title, ingredients, directions, link, source, NER); 
#!/bin/bash

# Copy recipe.csv to MySQL container
docker cp recipe.csv mysql:/var/lib/mysql-files/

# Execute SQL script to create table and import data
docker exec -i mysql mysql -u root -proot < spark-scripts/setup_database.sql

# Create HDFS directory
docker exec namenode hdfs dfs -mkdir -p /recipes

# Restart data transfer service
docker-compose restart data-transfer 
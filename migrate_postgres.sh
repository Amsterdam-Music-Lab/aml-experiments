#!/bin/bash

# Backup existing data
docker-compose exec db pg_dumpall -c -U ${SQL_USER} > db_backup.sql

# Remove existing volumes
docker-compose down -v

# Restore data
docker-compose up -d db
sleep 10 # Wait for the database to be ready
cat db_backup.sql | docker-compose exec -T db psql -U ${SQL_USER}

docker-compose up -d
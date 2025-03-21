#!/bin/bash
set -e

export PGUSER="$POSTGRES_USER"

echo "Loading pg_sphere extensions into $POSTGRES_DB"
psql --dbname="$POSTGRES_DB" <<-'EOSQL'
    CREATE EXTENSION IF NOT EXISTS pg_sphere;
EOSQL


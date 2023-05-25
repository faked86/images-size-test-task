#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z $PG_HOST $PG_PORT; do
    sleep 3
done

echo "PostgreSQL started"

echo "Waiting for Redis..."

while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 3
done

echo "Redis started"

exec "$@"
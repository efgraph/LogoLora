#!/bin/sh
./wait-for-it.sh postgres:5432 -t 10 -- echo "postgres is up"
alembic upgrade head
python3 -m bot

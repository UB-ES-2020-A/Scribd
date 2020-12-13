#!/bin/sh

if [[ -f "db.sqlite3" ]]; then
  echo "Eliminando 'db.sqlite3'"
  rm "db.sqlite3"
fi

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata fixtures/data.json

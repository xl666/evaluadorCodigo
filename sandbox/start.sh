#!/bin/bash

#Este script inicia el todos los sistemas locales de forma adecuada

# Reiniciar BD sandboxer
rm sandboxer/app/db.sqlite3 2> /dev/null
python sandboxer/app/manage.py migrate

# Quitar contenedores ttyd
docker stop $(docker ps | grep cplus | egrep -o "^[a-zA-Z0-9]{12}") 2> /dev/null

# Lanzar monitor
python monitor/monitor.py & 

# Lanzar sandboxer

python sandboxer/app/manage.py runserver 0.0.0.0:8181

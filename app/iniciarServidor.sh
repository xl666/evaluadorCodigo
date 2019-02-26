#!/bin/bash

#Pasar todas la variables a un archivo env
echo SECRET_KEY_DEVELOPMENT=$SECRET_KEY_DEVELOPMENT > .env
echo SECRET_KEY_PRODUCTION=$SECRET_KEY_PRODUCTION >> .env
echo DATABASE_NAME=$DATABASE_NAME >> .env
echo DATABASE_USER=$DATABASE_USER >> .env
echo DATABASE_PASSWORD=$DATABASE_PASSWORD >> .env
echo DATABASE_HOST=$DATABASE_HOST >> .env
echo DATABASE_PORT=$DATABASE_PORT >> .env

# lanzar servicio de inyeccion con usuario limitado
su -c 'python -u api/servicioInyeccion.py 9030' limitado &

echo "Esperando a iniciar servidor"

sleep 15

echo "Espera terminada, ahora si iniciando..."




python -u manage.py makemigrations --settings sistema_evaluacion_codigo.production
python -u manage.py migrate --settings sistema_evaluacion_codigo.production
#python -u manage.py runserver --settings sistema_evaluacion_codigo.production 0.0.0.0:8000
gunicorn --bind :8000 sistema_evaluacion_codigo.wsgi:application --reload

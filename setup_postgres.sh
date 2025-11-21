#!/bin/bash

# Variables
DB_NAME="proyecto_desercion"
DB_USER="proyecto_user"
DB_PASS="12345"

echo "Configurando postgres"

sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"

sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

echo "Usuario y base de datos creados:"

sudo -u postgres psql -c "\du $DB_USER"
sudo -u postgres psql -c "\l $DB_NAME"

echo "Configuración completa."
echo "Usa estos valores en tu settings.py de Django:"
echo "
Configurado:
'NAME': '$DB_NAME',
'USER': '$DB_USER',
'PASSWORD': '$DB_PASS',
'HOST': 'localhost',
'PORT': '5432',
"

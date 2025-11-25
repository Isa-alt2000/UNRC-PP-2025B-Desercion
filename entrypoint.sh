#!/bin/bash

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Creando superusuario..."

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="Admin").exists():
    User.objects.create_superuser("Admin", "admin@example.com", "admin123")
    print("Superusuario creado.")
else:
    print("Superusuario ya existe.")
EOF
echo "Superusuario listo. Usuario: Admin, Contraseña: admin123"
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000

#!/usr/bin/env python
import os
import sys
import time
#import socket
import subprocess
import psycopg2


# def wait_for_db():
#     """Espera a que PostgreSQL esté listo"""
#     print("Esperando a que PostgreSQL esté listo...")
#     while True:
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.connect(('db', 5432))
#             sock.close()
#             print("PostgreSQL está listo!")
#             break
#         except socket.error:
#             time.sleep(0.1)


def wait_for_db():
    """Espera a que PostgreSQL esté listo"""
    print("Esperando a que PostgreSQL esté listo...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                connect_timeout=3
            )
            conn.close()
            print("PostgreSQL está listo!")
            return True
        except psycopg2.OperationalError as e:
            retry_count += 1
            print(f"Intento {retry_count}/{max_retries}: PostgreSQL no está listo aún...")
            time.sleep(1)
    
    print("ERROR: No se pudo conectar a PostgreSQL")
    return False


def run_command(command):
    """Ejecuta un comando y muestra el output"""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    wait_for_db()

    print("Aplicando migraciones...")
    run_command("python manage.py makemigrations --noinput")
    run_command("python manage.py migrate --noinput")

    print("Creando superusuario...")
    run_command("""python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='Admin').exists():
    User.objects.create_superuser('Admin', 'admin@example.com', 'admin123')
    print('Superusuario creado.')
else:
    print('Superusuario ya existe.')
"
""")

    print("Superusuario listo. Usuario: Admin, Contraseña: admin123")
    print("Iniciando servidor...")
    run_command("python manage.py runserver 0.0.0.0:8000")
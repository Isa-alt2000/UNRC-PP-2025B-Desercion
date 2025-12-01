# Proyecto Prototípico de Deserción estudiantil
Este pequeño proyecto forma parte de la evidencia para el Proyecto Prototípico "Deserción escolar" realizado por alumnos de tercer semestre de la Universidad Nacional Rosaio Castellanos.

Para la realización de este proyecto, se optó por utilizar django debido a su modularidad y manejo más ordenado de los archivos e información.

## Tareas
- [x] Sistema de login simple que NO requiere correo dada la simplicidad del proyecto.
- [x] App calculadora de balance personal (login necesario).
- [x] Visualización de predicción financiera integrando cálculo.
- [ ] ~~Formulario de deserciones y posterior desglose de estadísticas en un dashboard.~~
- [ ] Dashboard de resultados de investigación extraido creado en base a formularios de google.
- [x] PDF de presentación con reporte ejecutivo anexado.

## Herramientas utilizadas
 - Django (Framework Python para desarrollo web)
 - Postgres (Motor de base de datos)
 - Docker (Para configuración rápida)

## Prerequisitos
 - **Python:** Instalar Python 3.10+ si se va a ejecutar el proyecto localmente.

 - **pip:** Administrador de paquetes para Python (`pip` se instala normalmente con Python).

 - **Docker (opcional):** Para levantar el proyecto con contenedores, instalar Docker Engine y Docker Compose (Linux) ó Docker Desktop(Windows).

 - **PostgreSQL (opcional):** Si no se opta por instalación Docker, instala Postgres o configura una DB externa.

## Instalación
Se cuenta con dos métodos; el método docker o con contenedores, y el método local. El método con contenedores es el más recomendado para un despliegue sencillo. EL método local es recomendable para un mayor control.  

### Configuración global  
1. **Configuración de variables de entorno**  

   Las variables de entorno sirven para no exponer datos que podrían ser sensibles como son endpoints de APIs, credenciales de bases de datos, tokens, etc. Para este proyecto, no se usan datos sensibles y el .evn.example tiene variables genericas que funcionarán bien al armar los contenedores sin requerir mayor configuración.

   Para configurar las variables de entorno genéricas:  

    **Windows**  

   - Copiar el archivo `.env.example` y renombrar la copia a `.env`  

    **Linux:**  

    ```bash
    cp .env.example .env
    ```

## Guia de instalación docker  
**Windows**  
1. Instalación de docker desktop 
   1. Descargar de sitio oficial [Aquí](https://www.docker.com/products/docker-desktop/).

   2. Instalar dependencias necesarias (pendiente).

2. Levantar los contenedores

   Una vez instalado docker desktop con todas sus dependencias, ejecutar el Powershell como administrador y desde la raíz del proyecto.

    ```powershell
    docker compose up
    ```

**Linux**
1. **Instalación de Docker**
   1. Docker Engine: https://docs.docker.com/engine/install/
   2. Docker Compose: https://docs.docker.com/compose/install/

2. Levantar los contenedores.  

   Una vez instaladas las herramientas de contenedores necesarias, ejecutar el siguiente comando en la raíz del proyecto:

   ```bash
   docker compose up
   ```

Siguiendo estos pasos, se puede acceder al proyecto por medio de `http://127.0.0.1:8000/` ó `http://localhost/`

## Instalación local (sin Docker)

1. Crear un entorno virtual

   ### **Linux**  
   Creación y ejecución

   ```bash
   python3 -m venv ppvenv
   source ppvenv/bin/activate
   ```

   ### **Windows**  
   Dar permisos:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

   Creación:

      ```powershell
   python3 -m venv ppvenv
   ```
   Activar:
   ```powershell
   .\ppvenv\Scripts\activate
   ```

2. Instalar dependencias (Dentro del entrono virtual)

   ```bash
   pip install -r requirements.txt
   ```

- **Configurar variables de entorno:**

   ```bash
   cp .env.example .env
   ```

- **Aplicar migraciones y crear superusuario:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   python manage.py runserver
   ```

## Uso
La apliación cuenta con apartados de:
 1. Sistema de login
 2. Manejo de cuentas
 3. Visualización del PDF final del reporte ejecutivo.
 4. Acceso al forms de google
 5. Dashboard de resultados del forms

## Extras
Para este proyecto se buscó seguir las mejores prácticas posibles de python y de desarrollo web indicadas a continuación.
 - Versionado git
 - PEP8 (Haciendo uso de Flake8)
 - Manejo de variables de entorno

**Sin embargo no se implementaron prácticas REST debido a la naturaleza pequeña del proyecto.**  

**La funcionalidad de usuarios fue reciclada de un proyecto anterior y adaptada a este proyecto por lo cual puede haber ligeras discrepancias que serán removidas poco a poco.**  

**El proyecto utiliza postgres como motor de base de datos, ~~será migrado a mysql en la posterioridad.~~**

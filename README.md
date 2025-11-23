# Proyecto Prototípico de Deserción estudiantil
Este pequeño proyecto forma parte de la evidencia para el Proyecto Prototípico "Deserción escolar" realizado por alumnos de tercer semestre de la Universidad Nacional Rosaio Castellanos.

Para la realización de este proyecto, se optó por utilizar django debido a su modularidad y manejo más ordenado de los archivos e información.

## Tareas
- [x] Sistema de login simple que NO requiere correo dada la simplicidad del proyecto.
- [x] App calculadora de balance personal (login necesario).
- [ ] Visualización de predicción financiera integrando cálculo.
- [ ] ~~Formulario de deserciones y posterior desglose de estadísticas en un dashboard.~~
- [ ] Dashboard de resultados de investigación extraido creado en base a formularios de google.
- [ ] PDF de presentación con reporte ejecutivo anexado.

## Herramientas utilizadas
 - Django
 - Postgres

## Guia de instalación
1. Configuración de motor de base de datos (postgres por el momento)  
    Configuración automática para despliegue con script. **UNICAMENTE SI NO EXISTE USUARIO O DB PREVIOS CON LOS MISMOS NOMBRES. EN TODO CASO, SERÁ NECESARIO HACERLO MANUALMENTE**
    - **script NO incluye la instalación de postgres por lo que deberá hacerse manualmente**  

    **Linux**
    ```bash
    chmod +x setup_postgres.sh
    ```

    ```bash
    ./setup_postgres.sh
    ```

2. Creación de entorno virtual  

   Para correr el proyecto de forma más eficiente, es recomendable crear un entorno virtual para instalar todas las dependencias. Para esto, ejecutar:

   **Linux:**

    ```bash
    python3 -m venv ppvenv
    ```

   Posteriormente para activarlo, ejecutar:  

   **Linux:**

    ```bash
    source ppvenv/bin/activate
    ```

    Para instalar librerías, ejecutar en la raíz del proyecto:  

    **Linux:**

    ```bash
    pip install -r requirements.txt
    ```

3. Configuración de variables de entorno  

   Las variables de entorno sirven para no exponer datos que podrían ser sensibles como son endpoints de APIs, credenciales de bases de datos, etc. Para este proyecto, no se usan datos sensibles y el .evn.example tiene variables genericas que funcionarán bien si se hace la instalación de postgres como se hizo previamente en pasos anteriores.

   Para settear las variables de entorno genéricas, ejecutar:

    **Linux:**

    ```bash
    cp .env.example .env
    ```

4. Migraciones django  

   Para que el proyecto funcione, hay que realizar las migraciones de django, las cuales se encargarán de las configuraciones de las bases de datos.

   **Linux:**

   ```bash
   python3 manage.py makemigrations
   ```
   ```bash
   python3 manage.py migrate
   ```

5. Levantar el proyecto  

   Finalmente, para levantar el proyecto, ejecutar:

   **Linux:**

   ```bash
   python3 manage.py runserver
   ```

Siguiendo estos pasos, se puede acceder al proyecto por medio de `http://127.0.0.1:8000/` ó `http://localhost/`

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

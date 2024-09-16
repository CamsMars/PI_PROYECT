# MIUW Project



Este repositorio contiene una página web con integraciones de IA y Spotyfy API



## Tabla de Contenidos

- [Características](#características)

- [Requisitos](#requisitos)

- [Instalación](#instalación)

- [Uso](#uso)

- [Estructura del Proyecto](#estructura-del-proyecto)

- [Contribuir](#contribuir)

- [Licencia](#licencia)



## Características

- Integración de música a través de API (ejemplo: Spotify, YouTube, etc.)

- Chatbot con IA que interactúa con los usuarios.

- Generecion automatica de  plailist con base a interaccion con la IA

- Sistema de gestión de base de datos basado en Django.

- Interfaz de usuario intuitiva y fácil de usar.



## Requisitos

Asegúrate de tener instalados los siguientes requisitos antes de continuar con la instalación:



- Python 3.x

- Django

- Otros paquetes que están especificados en el archivo [requirements.txt](https://github.com/CamsMars/PI_PROYECT/blob/658996757dcec066805a6d46c2f2522af779eb6c/MIUW/requirements.txt)



## Instalación



Sigue estos pasos para clonar e instalar el proyecto en tu máquina local.



1. Clonar el repositorio:



    ```bash

    git clone [[https://github.com/usuario/repo.git](https://github.com/CamsMars/PI_PROYECT.git)](https://github.com/CamsMars/PI_PROYECT.git)

    cd PI_PROYECT/

    ```



2. Crear un entorno virtual e instalar las dependencias:



    ```bash

    python -m venv env

    source env/bin/activate  # Para sistemas Unix

    env\\Scripts\\activate  # Para Windows

    pip install -r requirements.txt

    ```



3. Configurar la base de datos:



    ```bash

    python manage.py migrate

    ```



## Uso



1. Para iniciar el servidor local:



    ```bash

    python manage.py runserver

    ```



2. Abre tu navegador y ve a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.



### Comandos Adicionales

- Crear un superusuario para acceder al panel de administración de Django:



    ```bash

    python manage.py createsuperuser

    ```



- Recoger archivos estáticos para producción:



    ```bash

    python manage.py collectstatic

    ```

## Licencia

Este proyecto está bajo la Licencia EAFIT?.

"""

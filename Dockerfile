FROM docker.io/python:3.11.5

RUN apt-get update && apt-get upgrade -y

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app

EXPOSE 80

RUN rm -r /var/cache/apt/archives

RUN useradd accountancpy -s /bin/bash

USER accountancpy:accountancpy

ENTRYPOINT [ "python", "-Wa", "manage.py", "runserver", "0.0.0.0:80" ]

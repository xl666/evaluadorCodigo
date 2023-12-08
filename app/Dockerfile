# start from an official image
FROM python:3.9

RUN apt-get -y update \  
    && apt-get install -y swi-prolog openjdk-17-jdk sbcl\
    && apt-get -y clean

RUN mkdir -p /code
RUN mkdir "/system"
COPY requirements.txt "/system"
RUN pip install -r /system/requirements.txt

WORKDIR /code

# 8000 es el puerto por defecto de django
EXPOSE 8000

ENV SECRET_KEY_DEVELOPMENT=""
ENV SECRET_KEY_PRODUCTION=""
ENV DATABASE_NAME=""
ENV DATABASE_USER=""
ENV DATABASE_PASSWORD=""
ENV DATABASE_HOST=""
ENV DATABASE_PORT=3306

COPY iniciarServidor.sh "/system"
RUN chmod 755 "/system/iniciarServidor.sh"


RUN useradd -s /bin/bash principal
RUN useradd -s /bin/bash limitado

CMD /bin/bash -c '/system/iniciarServidor.sh'

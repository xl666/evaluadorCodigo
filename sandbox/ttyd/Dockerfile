FROM tsl0922/ttyd

RUN apt-get -y update \  
    && apt-get install -y g++ emacs \
    && apt-get -y clean

RUN mkdir -p /code
WORKDIR /code

EXPOSE 7681

ENV TOKEN=""

COPY ./run.sh /
RUN chmod 700 /run.sh
RUN useradd -s /bin/bash alumno
RUN chown  alumno /code


CMD /run.sh





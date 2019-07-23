FROM tsl0922/ttyd

RUN apt-get -y update \  
    && apt-get install -y g++ emacs \
    && apt-get -y clean

RUN mkdir -p /code
WORKDIR /code

EXPOSE 7681

ENV TOKEN=""

CMD ["ttyd", "-m", "1", "bash"]





FROM selenium/standalone-chrome

USER root

RUN apt-get update -y
RUN apt-get install -y vim git python3-pip
RUN mkdir /app
WORKDIR /app
COPY . .
RUN chmod 777 /app

RUN sudo apt-get install -y python3-pip
RUN sudo pip3 install virtualenv
RUN cd /app && virtualenv env && \ 
    /app/env/bin/pip3 install -r requirements.txt && \
    mkdir /app/downloads && \
    fallocate -l 25MB img25mb.png

USER seluser

ENTRYPOINT ["tail", "-f", "/dev/null"]
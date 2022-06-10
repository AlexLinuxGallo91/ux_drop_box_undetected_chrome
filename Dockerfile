FROM selenium/standalone-chrome

USER root

RUN apt-get update -y
RUN apt-get install -y vim git python3-pip
RUN mkdir -p /app/downloads
WORKDIR /app
COPY . .
RUN chmod 777 -R /app
RUN chmod 777 -R /app/downloads

RUN sudo apt-get install -y python3-pip
RUN sudo pip3 install virtualenv
RUN cd /app && virtualenv env && \ 
    /app/env/bin/pip3 install -r requirements.txt && \
    fallocate -l 25MB img25mb.png

USER seluser

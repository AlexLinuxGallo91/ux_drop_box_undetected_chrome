FROM selenium/standalone-chrome:103.0

USER root

RUN apt-get update -y
RUN apt-get install -y vim git python3-pip
RUN apt install -y python3-xlib python3-tk python3-dev
RUN apt install -y xvfb xserver-xephyr

WORKDIR /app
COPY . .
RUN chmod 777 -R /app
RUN mkdir -p /downloads
RUN chmod 777 -R /downloads

RUN sudo apt-get install -y python3-pip
RUN sudo pip3 install virtualenv
RUN cd /app && virtualenv /env && /env/bin/pip3 install -r requirements.txt && \
    fallocate -l 25MB /img25mb.png
    
RUN chmod 777 -R /img25mb.png

USER seluser
RUN touch /home/seluser/.Xauthority

FROM ubuntu:latest
MAINTAINER big_J

ENV NAME=reverseroski

WORKDIR /${NAME}
COPY . /${NAME}

RUN apt-get update
#RUN apt-get install -y apt-utils
RUN apt-get install -y python3 python3-pip
RUN /${NAME}/setup.sh

EXPOSE 80 5000 5001 5002 5003 5004 5005 5006 5007 5008 5009

CMD ./run.sh

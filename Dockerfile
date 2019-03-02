FROM jmc1283/flasq-base

RUN apk add --update gcc g++ make libffi-dev openssl-dev && rm -rf /var/cache/apk/
COPY ./requirements.txt /flasq/
RUN  pip3 install -r requirements.txt

COPY . /flasq

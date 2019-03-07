FROM jmc1283/flasq-base

RUN apk add --update gcc g++ make libffi-dev openssl-dev mysql-client && rm -rf /var/cache/apk/
COPY ./requirements.txt /flasq/
RUN pip3 install -r requirements.txt

COPY . /flasq
RUN rm requirements.txt

RUN chmod +x docker-entrypoint.sh
CMD ./docker-entrypoint.sh

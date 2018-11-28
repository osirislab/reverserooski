#!/bin/bash

openssl dhparam -dsaparam -out /etc/ssl/private/dhparam.pem 4096
openssl req -newkey rsa:4096 -nodes -keyout cert.pem -x509 -days 365 -out cert.pem

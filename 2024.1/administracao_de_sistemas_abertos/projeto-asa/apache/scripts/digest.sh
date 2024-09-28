#!/bin/bash

EMAIL="${1}"
DOMINIO="${2}"

STRING=$(mysql -p"1F(986934)" -u container20 -h 192.168.102.100 BD20 -N -B -e "select SHA1(senha) from projeto_users where email = '${EMAIL}' and dominio = '${DOMINIO}';" | base64)

echo "{SHA}${STRING}"

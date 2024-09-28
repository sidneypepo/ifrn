#!/bin/bash


SENHA="1F(986934)"

MYSQL="mysql -h 192.168.102.100 -u container20 -p"$SENHA" -D BD20 -e"
LISTA_DOMINIOS="$($MYSQL 'SELECT domain FROM domains;')"
ARQUIVOS='/var/projeto-asa/dns/arquivos_de_zona'
IFS=' '

for ARQUIVO_ZONE in "$ARQUIVOS"/*; do

ARQUIVO=$(echo "$ARQUIVO_ZONE" | sed 's/\.[^.]*$//')
ARQUIVO=$(basename $ARQUIVO)
unset IFS

if ! echo "$LISTA_DOMINIOS" | grep -q "$ARQUIVO"; then

DOMINIO=$ARQUIVO

### ADICIONANDO UM PONTO (.) CASO NÃO TENHA --------------------------------
if [[ ! $DOMINIO =~ \.$ ]]; then
    DOMINIO="$DOMINIO."
fi


### APAGANDO ARQUIVO DE ZONA

CAMINHO_ARQUIVOS_ZONA='/var/projeto-asa/dns/arquivos_de_zona/'
rm "$CAMINHO_ARQUIVOS_ZONA$DOMINIO"zone


### APAGANDO CONFIGURACOES DE ZONA

LINHA_INICIAL=$(grep -n "$DOMINIO" /var/projeto-asa/dns/named.conf.projeto  | awk -F':' '{print $1}' | head -n 1)
LINHA_FINAL=$(( LINHA_INICIAL + 5 ))
LINHAS="$LINHA_INICIAL,$LINHA_FINAL"d
sed "$LINHAS" /var/projeto-asa/dns/named.conf.projeto > temp && mv temp /var/projeto-asa/dns/named.conf.projeto
chgrp apache /var/projeto-asa/dns/named.conf.projeto
chown apache /var/projeto-asa/dns/named.conf.projeto

fi
done


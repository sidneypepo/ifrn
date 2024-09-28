#!/bin/bash


### VERIFICANDO DOMINIOS NO BANCO DE DADOS

SENHA="1F(986934)"

MYSQL="mysql -h 192.168.102.100 -u container20 -p"$SENHA" -D BD20 -e"
LISTA_DOMINIOS="$($MYSQL 'SELECT domain FROM domains;')"

for DOMINIO in $LISTA_DOMINIOS; do
if [[ $DOMINIO != domain && $DOMINIO != f.mail20.local && $DOMINIO != mail20.local ]]; then
if [[ ! -e "/var/projeto-asa/dns/arquivos_de_zona/$DOMINIO.zone" ]]; then

### ADICIONANDO UM PONTO (.) CASO NÃO TENHA
if [[ ! $DOMINIO =~ \.$ ]]; then
    DOMINIO="$DOMINIO."
fi


IP='192.168.102.120'

ARQUIVO_DOMINIO="$DOMINIO"zone
CAMINHO_NAMED='/var/projeto-asa/dns/named.conf.projeto'
CAMINHO_ARQUIVOS="/var/projeto-asa/dns/arquivos_de_zona/$ARQUIVO_DOMINIO"


### CRIACAO DO ARQUIVO DE ZONA ---------------------------------

SERIAL=$(date +"%Y%m%d")00
WWW="www.$DOMINIO"
MAIL="mail.$DOMINIO"
FTP="ftp.$DOMINIO"


echo -e '$TTL 30\n'\
"\$ORIGIN $DOMINIO\n"\
"@      IN      SOA     $DOMINIO                admin   (\n"\
"               $SERIAL\n"\
'               2M\n'\
'               1M\n'\
'               5M\n'\
"               30      )\n"\
'\n'\
"               IN      A       $IP\n"\
"               IN      NS      $DOMINIO\n"\
"               IN      MX  5   $MAIL\n"\
'\n'\
"$WWW			IN	CNAME	@\n"\
"$MAIL          	IN      A       $IP\n"\
"$FTP           	IN      A	$IP" > $CAMINHO_ARQUIVOS



### CRIACAO DAS CONFIGURACOES DE ZONA --------------------------


if ! test -f /var/projeto-asa/dns/named.conf.projeto; then
touch $CAMINHO_NAMED
chgrp apache $CAMINHO_NAMED
chown apache $CAMINHO_NAMED
fi

echo -e "zone \"$DOMINIO\" IN {\n"\
'       type master;\n'\
"       file \"/var/projeto-asa/dns/arquivos_de_zona/$ARQUIVO_DOMINIO\";\n"\
'       allow-query { any; };\n'\
'};\n' >> $CAMINHO_NAMED



fi
fi
done


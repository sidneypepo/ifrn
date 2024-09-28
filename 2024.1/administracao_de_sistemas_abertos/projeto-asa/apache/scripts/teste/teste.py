#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
import subprocess
import os

def check_ipv4_address():
    saida = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True)
    ip = saida.decode('utf-8').strip()

    if ip.startswith('192.168.'):
        return ip
    else:
        print('Erro ao obter endereço IPv4.')
        raise SystemExit

def mysql_check():

    connection = mysql.connector.connect(
        host='192.168.102.100',  
        database='BD20',  
        user='container20',  
        password='1F(986934)',  
        charset='utf8'
        )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM domains;")
            
            # Obter todos os registros
        records = cursor.fetchall()

            # Converter para uma lista única
        lista_unica = [item for sublist in records for item in sublist]
        return lista_unica

 
def atualizar_namedconf(domains_array):
    os.chdir("/var/projeto-asa/apache/scripts/teste")
    ipv4 = check_ipv4_address()

    if len(domains_array) > 0:
        with open('named.conf.projeto', 'w') as named_conf:
            for domain in domains_array:
                zone_config = """zone "{domain}" IN {{
    type master;
    file "/var/projeto-asa/apache/scripts/teste/{domain}.zone";
    allow-query {{ any; }};
}};\n\n""".format(domain=domain)
                named_conf.write(zone_config)

        for domain in domains_array:
            zone_file_content = """; {domain} zone file
$TTL 2M
$ORIGIN {domain}.
@       IN  SOA     {domain}. admin.{domain}. (
                202406100   ; Serial
                2M          ; Refresh
                5M          ; Retry
                30M         ; Expire
                1D)         ; Minimum TTL
        IN  A       {ipv4}
        IN  NS      {domain}.
        IN  MX 10   mail.{domain}.

mail    IN  A       {ipv4}
ftp     IN  CNAME   @
www     IN  CNAME   @
""".format(domain=domain, ipv4=ipv4)
            with open('{domain}.zone'.format(domain=domain), 'w') as zone_file:
                zone_file.write(zone_file_content)

def checagem(domains_array):
    os.chdir("/var/projeto-asa/apache/scripts/teste/arquivoszona")
    for i in os.listdir():
        if i not in domains_array:
            try:
                os.remove(i)
            except:
                os.system('rm -f {0}'.format(i))

def main():
    dominios = mysql_check()
    atualizar_namedconf(domains_array=dominios)
    checagem(domains_array=dominios)

if __name__ == "__main__":
    main()


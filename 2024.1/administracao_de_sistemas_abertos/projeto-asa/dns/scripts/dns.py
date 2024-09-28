#!/usr/bin/env python3
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
    try:
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
            
            records = cursor.fetchall()
            domains_list = [item for sublist in records for item in sublist]
            return domains_list
    except Error as e:
        print("Erro ao conectar ao MySQL: {0}".format(e))
        raise SystemExit
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def atualizar_namedconf(domains_array):
    os.chdir("/var/projeto-asa/dns")
    ipv4 = check_ipv4_address()

    if len(domains_array) > 0:
        with open('named.conf.projeto', 'w') as named_conf:
            for domain in domains_array:
                zone_config = """zone "{domain}" IN {{
    type master;
    file "/var/projeto-asa/dns/arquivos_de_zona/{domain}.zone";
    allow-query {{ any; }};
}};\n\n""".format(domain=domain)
                named_conf.write(zone_config)
        
        os.chdir('/var/projeto-asa/dns/arquivos_de_zona')
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
            with open('{0}.zone'.format(domain), 'w') as zone_file:
                zone_file.write(zone_file_content)

def checagem(domains_array):
    os.chdir("/var/projeto-asa/dns/arquivos_de_zona")
    for filename in os.listdir():
        if filename.split('.')[0] not in domains_array:
            try:
                os.remove(filename)
            except:
                os.system('rm -f {0}'.format(filename))

def main():
    dominios = mysql_check()
    atualizar_namedconf(domains_array=dominios)
    checagem(domains_array=dominios)

if __name__ == "__main__":
    main()


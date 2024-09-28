#!/usr/bin/env python3
import subprocess
import os
import mysql.connector
from mysql.connector import Error

# Aqui obtemos o endereço Ipv4 do container
def check_ipv4_address():
    saida = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True)
    ip = saida.decode('utf-8').strip()

    if ip.startswith('192.168.'):
        return ip

    else:
        print('Erro ao obter endereço Ipv4.')
        raise SystemExit

# Atualizar o arquivo httpd.conf.projeto
def atualizar_httpdconf(domains_array):
    os.chdir('/var/projeto-asa/apache')
    ipv4 = check_ipv4_address()

    with open('httpd.conf.projeto', 'w') as arquivo:
        header = """<Directory /var/projeto-asa/dominios>
    AllowOverride All
    Require all granted
</Directory>\n"""
        arquivo.write(header)

    if domains_array[1:] != 0:
        with open('httpd.conf.projeto', 'a') as arquivo:
            for domain_name in domains_array[1:]:
                body = """\n<VirtualHost {0}:80>
    <Directory /var/projeto-asa/dominios/{1}/www/adm>
        AuthType Basic
        AuthName "Login"
        AuthBasicProvider socache dbd
        AuthnCacheProvideFor dbd
        AuthnCacheContext '{1}'
        Require valid-user
        AuthDBDUserPWQuery "SELECT senha_apache FROM projeto_users WHERE email = %s AND dominio = '{1}'"
        Options Indexes
    </Directory>
    ServerName www.{1}
    ServerAlias {1}
    DocumentRoot "/var/projeto-asa/dominios/{1}/www"
    ErrorLog "/var/projeto-asa/dominios/{1}/logs/error.log"
    CustomLog "/var/projeto-asa/dominios/{1}/logs/access.log" common
</VirtualHost>\n""".format(ipv4, domain_name)

                arquivo.write(body)

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

        # Exibir os registros
   
        lista_unica = [item for sublist in records for item in sublist]
        return lista_unica

# Atualiza a estrutura de arquivo dos domínios
def update_virtualdomains(domains_array):
    os.chdir('/var/projeto-asa/dominios')
    for i in os.listdir():
        if i not in domains_array:
            try:
                os.removedirs(i)
            except NotADirectoryError:
                os.remove(i)
            except OSError:
                os.system('rm -rf {0}'.format(i))

    for i in domains_array:
        os.chdir('/var/projeto-asa/dominios')
        # Verificia se o diretório existe
        if i not in os.listdir():
            # Cria os arquivos do domínio
            os.makedirs('{0}'.format(i))
            os.makedirs('{0}/www/adm'.format(i))
            os.makedirs('{0}/logs'.format(i))
            #os.system("chown apache * & chgrp apache *")

            os.chdir('{0}/logs'.format(i))
            with open('error.log', 'w') as arquivo:
                pass
            with open('access.log', 'w') as arquivo:
                pass

            os.chdir('../www')
            os.system("cp /var/projeto-asa/apache/interface_grafica/* .")
            #os.system('chown apache * & chgrp apache *')				
# Chama um script que reinicia o apache e o bind
def apache_reload():
    caminho_script = '/var/projeto-asa/apache/scripts/reiniciar_services.sh'
    processo = subprocess.Popen([caminho_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = processo.communicate()

    if processo.returncode == 0:
        print(stdout.decode('utf-8'))

    else:
        print(stderr.decode('utf-8'))

def main():
    dominios = mysql_check()
    atualizar_httpdconf(domains_array=dominios)
    update_virtualdomains(domains_array=dominios)
    #apache_reload()

if __name__ == "__main__":
    main()

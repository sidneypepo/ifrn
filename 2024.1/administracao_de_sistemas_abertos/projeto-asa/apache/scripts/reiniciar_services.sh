#!/bin/bash

#/sbin/service named restart
(/var/projeto-asa/dns/scripts/bind.sh && /usr/sbin/rndc reload)&
(/var/projeto-asa/email/postconf.sh && /sbin/service postfix restart && /sbin/service dovecot restart)&
(/var/projeto-asa/ftp/ftpconfig.sh && /var/projeto-asa/ftp/atualizar_ftpgroups.sh && chmod -R 777 /var/projeto-asa/dominios/)&
(/var/projeto-asa/apache/scripts/atualizar_apache.py && sleep 10 && /opt/rh/httpd24/root/usr/sbin/apachectl restart)&
disown

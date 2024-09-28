#!/bin/bash

# Dados da conexão
USER="container20"
SENHA="1F(986934)"
HOST="192.168.102.100"
BD="BD20"
DOMINIOS=""

# Conectar ao MySQL e executar a consulta para obter os emails dos admins
for dominio in $(mysql -u$USER -p$SENHA -h$HOST $BD -N -B -e "SELECT * FROM domains;"); do
	DOMINIOS="mail.${dominio}, ${DOMINIOS}"
done

# Adiciona os domínios do banco de dados à configuração do Postfix
postconf -e "mydestination = ${DOMINIOS}\$myhostname, localhost.\$mydomain, localhost, localhost.localdomain"

echo "Postfix atualizado com sucesso!"

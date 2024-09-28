#!/bin/bash

# Dados da conexão
USER="container20"
SENHA="1F(986934)"
HOST="192.168.102.100"
BD="BD20"

# Conectar ao MySQL e executar a consulta para obter os emails dos admins
EMAILS=$(mysql -u$USER -p$SENHA -h$HOST $BD -N -B -e "SELECT email FROM projeto_users WHERE gid = '0' AND tipo LIKE 'adm%' AND tipo <> 'admgeral.php'")


for EMAIL in $EMAILS; do
  # Obter o domínio correspondente ao email
  DOMINIO=$(mysql -u$USER -p$SENHA -h$HOST $BD -N -B -e "SELECT dominio FROM projeto_users WHERE email = '$EMAIL';")

  if [ -n "$DOMINIO" ]; then
    # Atualizar a tabela projeto_users
    PROJETO_USERS_UPDATE="UPDATE projeto_users SET gid = '70000', ativo = 'Y', dir = '/var/projeto-asa/dominios/$DOMINIO', shell = '/bin/bash' WHERE email = '$EMAIL';"
    echo "Executando query para projeto_users: $PROJETO_USERS_UPDATE"
    mysql -u$USER -p$SENHA -h$HOST $BD -e "$PROJETO_USERS_UPDATE"

    # Atualizar a tabela ftpgroups
    FTPGROUPS_UPDATE="UPDATE ftpgroups SET members = CASE WHEN members IS NULL OR members = '' THEN '$EMAIL' ELSE CONCAT(members, ', ', '$EMAIL') END WHERE groupname = 'projeto-asa';"
    mysql -u$USER -p$SENHA -h$HOST $BD -e "$FTPGROUPS_UPDATE"
  fi
done

echo "Atualizações concluídas com sucesso!"

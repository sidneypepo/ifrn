#!/bin/bash

# Função para consultar o banco de dados e retornar resultado
execute_query() {
    QUERY="$1"
    mysql -u container20 -p'1F(986934)' -h 192.168.102.100 -D BD20 -N -s -e "$QUERY"
}

# Consulta para obter os membros atuais do grupo projeto-asa
CONSULTAR_MEMBROS="SELECT members FROM ftpgroups WHERE groupname = 'projeto-asa';"
MEMBROS_ATUAIS=$(execute_query "$CONSULTAR_MEMBROS")

# Lista de membros atuais do grupo projeto-asa
IFS=', ' read -r -a MEMBERS_ARRAY <<< "$MEMBROS_ATUAIS"

NEW_MEMBERS=""

# Iterar sobre cada membro
for MEMBER in "${MEMBERS_ARRAY[@]}"; do
    # Verificar se o membro está na tabela projeto_users
    EXISTS=$(execute_query "SELECT COUNT(*) FROM projeto_users WHERE email = '$MEMBER';")

 
    if [ "$EXISTS" -eq 1 ]; then
        if [ -z "$NEW_MEMBERS" ]; then
            NEW_MEMBERS="$MEMBER"
        else
            NEW_MEMBERS="$NEW_MEMBERS, $MEMBER"
        fi
    fi
done

# Atualizar a tabela ftpgroups com a nova lista de membros
if [ -n "$NEW_MEMBERS" ]; then
    UPDATE_QUERY="UPDATE ftpgroups SET members = '$NEW_MEMBERS' WHERE groupname = 'projeto-asa';"
    execute_query "$UPDATE_QUERY"
fi

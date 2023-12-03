#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/cliente.py
# Copyright (C) 2023  Sidney Pedro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# Importando bibliotecas
from constantes import *
import socket

# Criando socket TCP
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando socket
status_conexao = server_sock.connect_ex(SOCKET_SERVIDOR)
if (status_conexao != 0):
    print("Erro: não foi possível se conectar ao servidor!")
    exit()
print("Conexão estabelecida com o servidor!")

while (True):
    # Recebendo e apresentando mensagem do servidor
    try:
        mensagem_recebida = server_sock.recv(TAMANHO_BUFFER).decode(CHARSET)
    except:
        print()
        break
    if (len(mensagem_recebida) == 0):
        print("Conexão perdida com o servidor!")
        break
    print(f"Mensagem recebida: {mensagem_recebida}")

    # Devolvendo mensagem ao servidor
    mensagem_retorno = ("Devolvendo mensagem: " + mensagem_recebida).encode(CHARSET)
    server_sock.send(mensagem_retorno)

# Finalizando socket
server_sock.close()

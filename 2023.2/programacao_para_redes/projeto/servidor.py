#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/servidor.py
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

# Criando socket TCP e desabilitando TIME_WAIT
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Habilitando socket
server_sock.bind(SOCKET_SERVIDOR)

# Escutando até o máximo de conexões simultaneas permitidas
server_sock.listen(CONEXOES_MAXIMAS)

parar = False
while (not parar):
    # Recebendo conexão do cliente e o apresentando
    try:
        client_sock, SOCKET_CLIENTE = server_sock.accept()
    except:
        print()
        break
    print(f"Cliente {SOCKET_CLIENTE} conectado!")

    while (True):
        # Obtendo mensagem do usuário
        try:
            mensagem = input("Digite uma mensagem: ").encode(CHARSET)
        except:
            parar = True
            print()
            break
        if (len(mensagem) == 0):
            continue

        # Enviando mensagem obtida ao cliente
        client_sock.send(mensagem)

        # Recebendo mensagem do cliente
        mensagem_recebida = client_sock.recv(TAMANHO_BUFFER).decode(CHARSET)
        if (len(mensagem_recebida) == 0):
            print(f"Cliente {SOCKET_CLIENTE} desconectado!")
            break

        print(f"{SOCKET_CLIENTE}> {mensagem_recebida}")

    client_sock.close()

server_sock.close()

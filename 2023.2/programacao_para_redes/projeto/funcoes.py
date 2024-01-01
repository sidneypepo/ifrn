#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/funcoes.py
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
import os, socket

# Armazenando caminho completo do diretório desse programa para
# funções que leem ou escrevem arquivos
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Função para remover um arquivo no diretório local do programa
def remover_arquivo(nome_arquivo: str):
    os.remove(f"{DIRETORIO_ATUAL}/{nome_arquivo}")
    return

# Função para testar se uma string é um número natural
def ehnatural(numero: str):
    # Se a string for vazia, retorna-se False
    if (len(numero) < 1):
        return False

    # Navegando em cada caractere da string e, se algum deles não for
    # um caractere numérico, retorna-se False
    for index in range(len(numero)):
        if (numero[index] < '0' or numero[index] > '9'):
            return False

    # Retorna True, caso a string seja um número natural
    return True

# Função para testar se uma string é um número inteiro
def ehinteiro(numero: str):
    # Se a string for vazia, retorna-se False
    if (len(numero) < 1):
        return False

    # Se a string for um número natural retorna-se True. Se não,
    # se o primeiro caractere for um hífem e o resto da string
    # for um número natural, retorna-se True
    if (ehnatural(numero)):
            return True
    elif (numero[0] == '-' and ehnatural(numero[1:])):
        return True

    # Retorna False, casoa string não seja um número inteiro
    return False

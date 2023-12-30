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
# funções que leem ou escrevem arquivos e tamanho de buffer padrão
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
TAMANHO_BUFFER = 1024

# Função para remover um arquivo no diretório local do programa
def remover_arquivo(nome_arquivo: str):
    os.remove(f"{DIRETORIO_ATUAL}/{nome_arquivo}")
    return
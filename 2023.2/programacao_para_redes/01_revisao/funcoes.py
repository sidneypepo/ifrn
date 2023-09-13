#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/01_revisao/funcoes.py
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

import os, random

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

def ehnatural(numero: str):
    if (len(numero) < 1):
        return False
    for index in range(len(numero)):
        if (numero[index] < '0' or numero[index] > '9'):
            return False

    return True

def ehinteiro(numero: str):
    if (ehnatural(numero)):
            return True
    elif (len(numero) > 1):
        if (numero[0] == '-' and ehnatural(numero[1:])):
            return True
        else:
            return False

    return False

def ehfloat(numero: str):
    if (ehinteiro(numero)):
        return True
    elif ('.' in numero):
        ponto = numero.index('.')
        if (ehinteiro(numero[:ponto]) and ehnatural(numero[ponto + 1:])):
            return True
        else:
            return False

    return False

def mostrar_erro(ativar: bool, mensagem: str):
    if (not ativar):
        print(mensagem)

def entrada_usuario(tipo: str, mensagem: str):
    valor = ""

    if (tipo.lower() == "nat"):
        while (not ehnatural(valor)):
            valor = input(mensagem)
            mostrar_erro(ehnatural(valor), "Erro: Digite um número natural!\n")
        valor = int(valor)
    elif (tipo.lower() == "int"):
        while (not ehinteiro(valor)):
            valor = input(mensagem)
            mostrar_erro(ehinteiro(valor), "Erro: Digite um número inteiro!\n")
        valor = int(valor)
    elif (tipo.lower() == "float"):
        while (not ehfloat(valor)):
            valor = input(mensagem)
            mostrar_erro(ehfloat(valor), "Erro: Digite um número fracionário!\n")
        valor = float(valor)
    elif (tipo.lower() == "str"):
        while (len(valor) == 0):
            valor = input(mensagem)
            mostrar_erro((len(valor) > 0), "Erro: Digite uma string válida!\n")
    else:
        valor = None

    return valor

def gerar_lista(quantidade: int, valor_minimo: int = 1, valor_maximo: int = 1000000):
    if (valor_minimo < 0):
        return False, None
    if (valor_maximo < valor_minimo):
        return False, None

    lista = []

    for item in range(quantidade):
        lista.append(random.randint(valor_minimo, valor_maximo))

    return True, lista

def salvar_lista(nome_lista: list, nome_arquivo: str = "valores_nao_ordenados.txt"):
    try:
        arquivo = open(diretorio_atual + '/' + nome_arquivo, 'w')
    except:
        return False

    for item in range(len(nome_lista)):
        arquivo.write(f"{nome_lista[item]}\n")

    arquivo.close()
    return True

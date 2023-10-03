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

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

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
        while (not len(valor) > 0):
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

    for index in range(quantidade):
        lista.append(random.randint(valor_minimo, valor_maximo))

    return True, lista

def salvar_lista(nome_lista: list, nome_arquivo: str = "valores_nao_ordenados.txt"):
    try:
        arquivo = open(DIRETORIO_ATUAL + '/' + nome_arquivo, 'w')

        for index in range(len(nome_lista)):
            arquivo.write(f"{nome_lista[index]}\n")
    except:
        return False

    arquivo.close()
    return True

def ler_arquivo(nome_arquivo: str, ignorar_strings: bool = True, encode: str = "utf-8"):
    try:
        arquivo = open(DIRETORIO_ATUAL + '/' + nome_arquivo, 'r', encoding=encode)
    except:
        return False, None

    lista = []
    for linha in arquivo:
        if (not ignorar_strings):
            lista.append(linha)
        elif (ehinteiro(linha[:-1]) and ignorar_strings):
            lista.append(int(linha[:-1]))
        else:
            return False, None

    arquivo.close()
    return True, lista

def ordena_bubble(nome_lista: list):
    if (len(nome_lista) == 0):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    invercao = False

    for index in range(len(nome_lista) - 1):
        if (nome_lista[index] > nome_lista[index + 1]):
            invercao = True
            nome_lista[index], nome_lista[index + 1] = nome_lista[index + 1], nome_lista[index]

    if (invercao):
        ordena_bubble(nome_lista)

    return True, nome_lista

def ordena_insertion(nome_lista: list):
    if (len(nome_lista) == 0):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    for index in range(1, len(nome_lista)):
        valor_temp = nome_lista[index]

        novo_index = index
        while (novo_index > 0 and valor_temp < nome_lista[novo_index - 1]):
            nome_lista[novo_index] = nome_lista[novo_index - 1]
            novo_index -= 1

        nome_lista[novo_index] = valor_temp

    return True, nome_lista

def ordena_selection(nome_lista: list):
    if (len(nome_lista) == 0):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    for index in range(len(nome_lista)):
        index_temp = index

        for outro_index in range(index + 1, len(nome_lista)):
            if (nome_lista[outro_index] < nome_lista[index_temp]):
                index_temp = outro_index

        nome_lista[index], nome_lista[index_temp] = nome_lista[index_temp], nome_lista[index]

    return True, nome_lista

def particionar(nome_lista: list, index_inicio: int, index_fim: int):
    valor_pivo = nome_lista[index_fim]
    index_pivo = index_inicio

    for index in range(index_inicio, index_fim):
        if (nome_lista[index] <= valor_pivo):
            nome_lista[index_pivo], nome_lista[index] = nome_lista[index], nome_lista[index_pivo]
            index_pivo += 1

    nome_lista[index_pivo], nome_lista[index_fim] = nome_lista[index_fim], nome_lista[index_pivo]

    return index_pivo

def ordena_quick(nome_lista: list, index_inicio: int = 0, index_fim: int = -1):
    if (len(nome_lista) == 0):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    if (index_fim == -1):
        index_fim = len(nome_lista) - 1

    if (index_inicio < index_fim):
        index_pivo = particionar(nome_lista, index_inicio, index_fim)

        ordena_quick(nome_lista, index_inicio, index_pivo - 1)
        ordena_quick(nome_lista, index_pivo + 1, index_fim)

    return True, nome_lista

def ordena_lista(nome_lista: list, metodo_ordena: str):
    try:
        if (metodo_ordena.upper() == "BUBBLE"):
            return ordena_bubble(nome_lista)
        elif (metodo_ordena.upper() == "INSERTION"):
            return ordena_insertion(nome_lista)
        elif (metodo_ordena.upper() == "SELECTION"):
            return ordena_selection(nome_lista)
        elif (metodo_ordena.upper() == "QUICK"):
            return ordena_quick(nome_lista)
    except:
        return False, None

    return False, None

def criar_diretorio(nome_diretorio: str):
    if (not nome_diretorio in os.listdir(DIRETORIO_ATUAL)):
        os.mkdir(DIRETORIO_ATUAL + '/' + nome_diretorio)

    return

def ler_diretorio(nome_diretorio: str):
    try:
        conteudo = os.listdir(DIRETORIO_ATUAL + "/" + nome_diretorio)
        return conteudo
    except:
        return []

    return []

def dividir_linha(linha: str, divisor: str = ';'):
    if (not '"' in linha):
        return linha.split(divisor)

    aspas = []
    for index in range(len(linha)):
        if (linha[index] == '"' and (not linha[index:index + 2] == "\"\"" and not linha[index - 1:index + 1] == "\"\"")):
            aspas.append(index)

    linha_dividida = []
    ultimo_index = 0
    for index in range(1, len(aspas), 2):
        linha_dividida += linha[ultimo_index:aspas[index - 1] - 1].split(divisor)
        linha_dividida.append(linha[aspas[index - 1]:aspas[index] + 1])
        ultimo_index = aspas[index] + 2
    linha_dividida += linha[ultimo_index:].split(divisor)

    return linha_dividida

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
    except:
        return False

    for index in range(len(nome_lista)):
        arquivo.write(f"{nome_lista[index]}\n")

    arquivo.close()
    return True

def ler_arquivo(nome_arquivo: str):
    try:
        arquivo = open(DIRETORIO_ATUAL + '/' + nome_arquivo, 'r')
    except:
        return False, None

    lista = []
    for linha in arquivo:
        if (not ehinteiro(linha[:-1])):
            return False, None
        lista.append(int(linha[:-1]))

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

def parser_pcap_header(dados: bytes):
    header = {}

    header["magic_number"] = int.from_bytes(dados[0:4], "little")
    if (header["magic_number"] == 2712847316):
        endianness = "little"
        precision = "micro"
    elif (header["magic_number"] == 2712812621):
        endianness = "little"
        precision = "nano"
    elif (header["magic_number"] == 3569595041):
        endianness = "big"
        precision = "micro"
    elif (header["magic_number"] == 1295823521):
        endianness = "big"
        precision = "nano"
    else:
        return None

    header["major_version"] = int.from_bytes(dados[4:6], endianness)
    header["minor_version"] = int.from_bytes(dados[6:8], endianness)
    if (header["major_version"] != 2 or header["minor_version"] != 4):
        return None

    header["snap_len"] = int.from_bytes(dados[16:20], endianness)
    header["link_type"] = int.from_bytes(dados[20:24], endianness)
    if (endianness == "little"):
        header["fcs"] = int.from_bytes(dados[23:24], endianness) >> 5
    else:
        header["fcs"] = int.from_bytes(dados[20:21], endianness) >> 5

    return endianness, precision, header

def parser_pacote_header(dados: bytes, endianness: str):
    header = {}
    header["timestamp"] = int.from_bytes(dados[0:4], endianness)
    header["precision"] = int.from_bytes(dados[4:8], endianness)
    header["captured_length"] = int.from_bytes(dados[8:12], endianness)
    header["original_length"] = int.from_bytes(dados[12:16], endianness)
    return header

def ler_pcap():
    nome_arquivo = entrada_usuario("str", "Digite o nome do arquivo: ")
    try:
        arquivo = open(DIRETORIO_ATUAL + '/' + nome_arquivo, "rb")
    except:
        print("Erro: não foi possível abrir o arquivo!")
        return None

    pcap_info = parser_pcap_header(arquivo.read(24))
    if (pcap_info == None):
        print("Erro: arquivo corrompido!")
        arquivo.close()
        return None

    endianness = pcap_info[0]
    precision = pcap_info[1]
    pcap_header = pcap_info[2]
    pacotes = []
    pacote = arquivo.read(16)

    try:
        while (len(pacote) != 0):
            pacote = parser_pacote_header(pacote, endianness)
            pacote["data"] = arquivo.read(pacote["captured_length"])
            pacotes.append(pacote)
            pacote = arquivo.read(16)
    except:
        print("Erro: não foi possível ler o arquivo!")
        return None

    arquivo.close()
    return endianness, precision, pcap_header, pacotes

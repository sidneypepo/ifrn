#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/03_tcpdump/funcoes.py
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

# Importando funções
import os

# Armazenando caminho completo do diretório desse programa para
# funções que leem ou escrevem arquivos
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

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

# Função para mostrar erro se o booleano informado for False
def mostrar_erro(ativar: bool, mensagem: str):
    if (not ativar):
        print(mensagem)

    return

# Função para receber e tratar dados informados pelo usuário
def entrada_usuario(tipo: str, mensagem: str):
    # Incializando dado
    dado = ""

    # Solitando dado com tipo informado, usando mensagem também
    # informada, enquanto não for digitado um dado válido e mostrando
    # erro em caso de dado inválido
    if (tipo.lower() == "nat"):
        while (not ehnatural(dado)):
            dado = input(mensagem)
            mostrar_erro(ehnatural(dado), "Erro: Digite um número natural!\n")
        dado = int(dado)
    elif (tipo.lower() == "int"):
        while (not ehinteiro(dado)):
            dado = input(mensagem)
            mostrar_erro(ehinteiro(dado), "Erro: Digite um número inteiro!\n")
        dado = int(dado)
    elif (tipo.lower() == "str"):
        while (not len(dado) > 0):
            dado = input(mensagem)
            mostrar_erro((len(dado) > 0), "Erro: Digite uma string válida!\n")
    else:
        dado = None

    # Retornando dado obtido
    return dado

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
    header["link_type"] = int.from_bytes(dados[20:24], endianness) & 268435455
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
        try:
            arquivo = open(DIRETORIO_ATUAL + "/tcp_dump/" + nome_arquivo, "rb")
        except:
            mostrar_erro(False, "Erro: não foi possível abrir o arquivo!")
            return None

    pcap_info = parser_pcap_header(arquivo.read(24))
    if (pcap_info == None):
        mostrar_erro(False, "Erro: arquivo corrompido!")
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
        mostrar_erro(False, "Erro: não foi possível ler o arquivo!")
        return None

    arquivo.close()
    return endianness, precision, pcap_header, pacotes

def ehbissexto(ano: int):
    if (not ehinteiro(str(ano))):
        return False

    if (ano % 400 == 0 or (ano % 4 == 0 and ano % 100 != 0)):
        return True

    return False

def segundos_data(timestamp: int, precision: int, tipo_precision: str, gmt: int = 0):
    if (tipo_precision == "micro" and ehinteiro(str(precision))):
        precision = f"{precision / 1000000:.6f}"[2:]
    elif (tipo_precision == "nano" and ehinteiro(str(precision))):
        precision = f"{precision / 1000000000:.9f}"[2:]
    else:
        mostrar_erro(False, "Erro: precisão inválida!")
        return None

    if (ehinteiro(str(timestamp)) and ehinteiro(str(gmt))):
        timestamp += 60 * 60 * gmt
    else:
        mostrar_erro(False, "Erro: timestamp inválida!")
        return None

    dias = timestamp // (60 * 60 * 24)
    segundos = timestamp % (60 * 60 * 24)

    ano = 1970
    mes = 1
    dia = 1
    for index in (range(1, dias + 1)):
        dia += 1
        if (not ehbissexto(ano) and mes == 2 and dia == 29):
            dia = 1
            mes = 3
        elif (ehbissexto(ano) and mes == 2 and dia == 30):
            dia = 1
            mes = 3
        elif (mes == 12 and dia == 32):
            ano += 1
            mes = 1
            dia = 1
        elif ((mes == 4 or mes == 6 or mes == 9 or mes == 11) and dia == 31):
            mes += 1
            dia = 1
        elif ((mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10) and dia == 32):
            mes += 1
            dia = 1

    hora = segundos // (60 * 60)
    minuto = (segundos % (60 * 60)) // 60
    segundo = segundos % 60

    return f"{ano:04d}-{mes:02d}-{dia:02d}_{hora:02d}:{minuto:02d}:{segundo:02d}.{precision}"
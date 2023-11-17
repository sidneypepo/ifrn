#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/10_universal_http_downloader/funcoes.py
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
import os, socket

# Armazenando caminho completo do diretório desse programa para
# funções que leem ou escrevem arquivos e codificação de
# caracteres
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CHARSET = "utf-8"
TAMANHO_BUFFER = 512
TAMANHO_CONTENT_LENGTH = len("Content-Length: ")

# Função para dividir cada parte de um endereço
def dividir_endereco(endereco: str):
    inicio_endereco = 0
    if ("http://" in endereco):
        inicio_endereco = len("http://")
    elif ("https://" in endereco):
        inicio_endereco = len("https://")

    protocolo = endereco[:inicio_endereco]
    endereco = endereco[inicio_endereco:]
    barra = endereco.find('/')
    if (barra == -1):
        return ''

    host = endereco[:barra]
    caminho = endereco[barra:]
    if (len(caminho) == 1 or not '.' in caminho[caminho.rfind('/'):]):
        return ''

    return protocolo, host, caminho

# Função para mostrar erro se o booleano informado for False
def mostrar_erro(ativar: bool, mensagem: str):
    if (not ativar):
        print(mensagem)

    return

# Função para receber e tratar dados informados pelo usuário
def entrada_usuario(tipo: str, mensagem: str):
    # Incializando dado
    dado = ''

    # Solitando dado com tipo informado, usando mensagem também
    # informada, enquanto não for digitado um dado válido e mostrando
    # erro em caso de dado inválido
    if (tipo.lower() == "addr"):
        while (not len(dado) > 0):
            dado = dividir_endereco(input(mensagem))
            mostrar_erro((len(dado) > 0), "Erro: digite um endereço válido!\n")
    else:
        dado = None

    # Retornando dado obtido
    return dado

def tamanho_resposta(resposta: bytes):
    if (b"Transfer-Encoding: chunked" in resposta):
        return "chunked"
    elif (not b"Content-Length: " in resposta):
        return ''

    cl_posicao = resposta.index(b"Content-Length: ") + TAMANHO_CONTENT_LENGTH
    if (not b"\r\n" in resposta[cl_posicao:]):
        return ''
    cl_posicao_fim = cl_posicao + resposta[cl_posicao:].index(b"\r\n")

    return str(resposta[cl_posicao:cl_posicao_fim])[2:-1]

def resposta_recebida(resposta: bytes):
    inicio_resposta = resposta.index(b"\r\n\r\n") + 4
    return len(resposta[inicio_resposta:])

def obter_arquivo(host: str, porta: int, caminho: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = sock.connect_ex((host, porta))
    if (status != 0):
        return ''

    requisicao = f"GET {caminho} HTTP/1.1\r\nHOST: {host}\r\n\r\n"
    sock.sendall(requisicao.encode(CHARSET))

    resposta = b''
    tipo_tamanho = ''
    bytes_recebidos = 0
    total_bytes = 1
    while ((tipo_tamanho != "chunked" or resposta[-5:] != b"0\r\n\r\n") and bytes_recebidos != total_bytes):
        resposta += sock.recv(TAMANHO_BUFFER)

        if (tipo_tamanho.isdecimal() and total_bytes > 1):
            bytes_recebidos = resposta_recebida(resposta)
        elif (tipo_tamanho.isdecimal()):
            total_bytes = int(tipo_tamanho)
        elif (tipo_tamanho == ''):
            tipo_tamanho = tamanho_resposta(resposta)

    sock.close()

    if (resposta[:12] != b"HTTP/1.1 200"):
        return ''

    return resposta[-total_bytes:]

def salvar_arquivo(dados: bytes, nome_arquivo: str):
    try:
        arquivo = open(f"{DIRETORIO_ATUAL}/{nome_arquivo}", "wb")
        arquivo.write(dados)
        arquivo.close()
        print("Arquivo salvo com sucesso!")
    except:
        mostrar_erro(False, "Erro: não foi possível salvar o arquivo!")

    return

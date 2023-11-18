#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/10_universal_image_downloader/funcoes.py
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
# funções que leem ou escrevem arquivos, a codificação de
# caracteres, tamanho de buffer padrão e quantidade de caracteres
# em "Content-Lenght: "
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CHARSET = "utf-8"
TAMANHO_BUFFER = 1024
TAMANHO_CONTENT_LENGTH = len("Content-Length: ")

# Função para dividir cada parte de um endereço
def dividir_endereco(endereco: str):
    # Separando protocolo do endereço total e armazenando-o
    inicio_endereco = 0
    if ("http://" in endereco):
        inicio_endereco = len("http://")
    elif ("https://" in endereco):
        inicio_endereco = len("https://")
    protocolo = endereco[:inicio_endereco]
    endereco = endereco[inicio_endereco:]

    # Obtendo posição da barra de caminho e, se não houver, retorna-se
    # uma string vazia
    barra = endereco.find('/')
    if (barra == -1):
        return ''

    # Armazenando host e caminho do arquivo e, se o caminho só possuir
    # um caractere ou não houver um ponto após a última barra presente
    # no caminho do arquivo, retorna-se uma string vazia
    host = endereco[:barra]
    caminho = endereco[barra:]
    if (len(caminho) == 1 or not '.' in caminho[caminho.rfind('/'):]):
        return ''

    # Retornando protocolo, host e caminho do arquivo
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

# Função para obter tipo ou tamanho da resposta HTTP
def tipo_tamanho_resposta(resposta: bytes):
    # Se a resposta possuir tipo de transferência chunked, retorna-se
    # a string "chunked", senão, se não possuir a string
    # "Content-Lenght: ", retorna-se uma string vazia
    if (b"Transfer-Encoding: chunked" in resposta):
        return "chunked"
    elif (not b"Content-Length: " in resposta):
        return ''

    # Obtendo posição do final da string "Content-Length: " e, se não
    # houver uma quebra de linha posteriormente a ela, retorna-se uma
    # string vazia
    content_length_posicao = resposta.index(b"Content-Length: ") + TAMANHO_CONTENT_LENGTH
    if (not b"\r\n" in resposta[content_length_posicao:]):
        return ''

    # Obtendo posição do final da linha do Content-Length
    content_length_posicao_fim = content_length_posicao + resposta[content_length_posicao:].index(b"\r\n")

    # Retornando caracteres presentes entre o final da string
    # "Content-Length: " e final da linha
    return str(resposta[content_length_posicao:content_length_posicao_fim])[2:-1]

# Função para contar quantos bytes foram recebidos em uma resposta
# HTTP
def tamanho_resposta_recebida(resposta: bytes):
    if (b"\r\n\r\n" in resposta):
        inicio_resposta = resposta.index(b"\r\n\r\n") + 4
        return len(resposta[inicio_resposta:])

    return 0

# Função para obter um arquivo via HTTP
def obter_arquivo(host: str, porta: int, caminho: str):
    # Montando socket, estabelecendo conexão e, se o status da mesma
    # for diferente de zero, retorna-se uma string vazia
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = sock.connect_ex((host, porta))
    if (status != 0):
        return ''

    # Montando e enviando requisição HTTP do tipo GET para o arquivo
    # especificado do host
    requisicao = f"GET {caminho} HTTP/1.1\r\nHOST: {host}\r\n\r\n"
    sock.sendall(requisicao.encode(CHARSET))

    # Definindo variáveis para armazenar resposta temporária, resposta
    # completa, tipo ou tamanho da resposta, quantidade de bytes já
    # recebidos e total de bytes a serem recebidos
    temp_resposta = b'\n'
    resposta = b''
    tipo_tamanho = ''
    bytes_recebidos = 0
    total_bytes = 1

    # Recebendo bytes enquanto o tipo da resposta não for chunked ou
    # os últimos bytes da resposta completa não forem um zero e duas
    # quebras de linha, e enquanto a quantidade de bytes recebidos for
    # menor que o total a ser recebido, e enquanto o tamanho da
    # resposta recebida for maior que zero e o socket é finalizado,
    # após receber todos os bytes
    while ((tipo_tamanho != "chunked" or resposta[-5:] != b"0\r\n\r\n") and bytes_recebidos < total_bytes and len(temp_resposta) > 0):
        # Armazenando resposta temporária e adicionando-a à resposta
        # completa
        temp_resposta = sock.recv(TAMANHO_BUFFER)
        resposta += temp_resposta

        # Se a string do tipo ou tamanho da resposta for numérico e o
        # total de bytes a serem recebidos for maior que um, obtem-se a
        # quantidade total de bytes recebidos até o momento, senão, se o
        # tipo ou tamanho da resposta for numérico, armazena-se o total
        # de bytes a serem recebidos a partir da conversão da string da
        # variável de tipo ou tamanho para inteiro, senão, se a variável
        # de tipo ou tamanho for uma string vazia, obtem-se o tipo ou
        # tamanho da resposta e o armazena na variável de tipo ou tamanho
        if (tipo_tamanho.isdecimal() and total_bytes > 1):
            bytes_recebidos = tamanho_resposta_recebida(resposta)
        elif (tipo_tamanho.isdecimal()):
            total_bytes = int(tipo_tamanho)
        elif (tipo_tamanho == ''):
            tipo_tamanho = tipo_tamanho_resposta(resposta)
    sock.close()

    # Se os 12 primeiros bytes indicarem um status de resposta
    # diferente de "Ok" (código 200), retorna-se uma string vazia
    if (resposta[:12] != b"HTTP/1.1 200"):
        return ''

    # Retornando bytes úteis
    if (tipo_tamanho == "chunked"):
        return resposta[resposta.index(b"\r\n\r\n") + 4:-5]
    else:
        return resposta[-total_bytes:]

# Função para salvar um arquivo
def salvar_arquivo(dados: bytes, nome_arquivo: str):
    # Abrindo e gravando dados no arquivo especificado e apresentando
    # mensagem de sucesso e, em caso de exceção, um erro é apresentado
    try:
        arquivo = open(f"{DIRETORIO_ATUAL}/{nome_arquivo}", "wb")
        arquivo.write(dados)
        arquivo.close()
        print("Arquivo salvo com sucesso!")
    except:
        mostrar_erro(False, "Erro: não foi possível salvar o arquivo!")

    return

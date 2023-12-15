#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/11_bot_telegram/funcoes.py
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
# funções que leem ou escrevem arquivos, a codificação de
# caracteres, tamanho de buffer padrão e quantidade de caracteres
# em "Content-Lenght: "
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CHARSET = "utf-8"
TAMANHO_BUFFER = 1024
TAMANHO_CONTENT_LENGTH = len("Content-Length: ")

# Função para obter o IP de um host
def obter_ip(host: str):
    try:
        ip = socket.gethostbyname(host)
    except:
        return ''

    return ip

# Função para testar a conectividade de um host
def testar_conectividade(ip: str):
    if (os.name == "nt"):
        os.system(f"ping {ip} | findstr /i ttl= > {DIRETORIO_ATUAL}/active.txt")
    elif (os.name == "posix"):
        os.system(f"ping -nc 4 {ip} | grep -i ttl= > {DIRETORIO_ATUAL}/active.txt")

    return

# Função para remover um arquivo no diretório local do programa
def remover_arquivo(nome_arquivo: str):
    os.remove(f"{DIRETORIO_ATUAL}/{nome_arquivo}")
    return

# Função para testar se uma porta está aberta ou fechada
def testar_porta(ip: str, porta: int):
    # Definindo lista de resultados e timeout para meio segundo
    resultados = []
    timeout = 0.5

    # Montando socket, estabelecendo timeout, conectando e, se o
    # retorno da conexão for zero, significa que a conexão foi
    # estabelecida e a porta está aberta
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    conexao = sock.connect_ex((ip, porta))
    if (conexao == 0):
        status_conexao = True
    else:
        status_conexao = False

    # Armazenando informações e status da porta para o protocolo TCP
    # e fechando socket
    resultados.append(status_conexao)
    sock.close()

    # Montando socket, estabelecendo timeout, conectando, enviando
    # bytes e tentando receber um retorno
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.connect_ex((ip, porta))
    sock.sendall("AAAA".encode(CHARSET))
    try:
        teste_udp = sock.recv(1)
    except:
        teste_udp = b''

    # Se houve retorno dos bytes enviados, significa que a porta está
    # aberta
    if (teste_udp == b''):
        status_conexao = False
    else:
        status_conexao = True

    # Armazenando informações e status da porta para o protocolo UDP
    # e fechando socket
    resultados.append(status_conexao)
    sock.close()

    return resultados

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

# Função para extrair bytes úteis de chunks
def extrair_chunks(resposta: bytes):
    # Removendo cabeçalho da resposta HTTP
    inicio_resposta = resposta.index(b"\r\n\r\n") + 4
    resposta = resposta[inicio_resposta:]

    # Definindo uma variável para armazenar o tamanho de cada chunk e
    # uma para armazenar a resposta final extraída
    tamanho_chunk = -1
    resposta_final = b''

    # Enquanto o tamanho da última chunk for diferente de zero,
    # obtem-se a posição da quebra de linha pós tamanho da chunk,
    # então a string que contém o tamanho da chunk é lida e convertida
    # para valor inteiro, então a quantidade de bytes da chunk,
    # especificados pelo tamanho da mesma, são armazenados na variável
    # de resposta final e a resposta original remove os bytes da chunk
    # anterior
    while (tamanho_chunk != 0):
        fim_tamanho_chunk = resposta.index(b"\r\n")
        tamanho_chunk = int(resposta[:fim_tamanho_chunk], 16)
        inicio_chunk = fim_tamanho_chunk + 2
        fim_chunk = inicio_chunk + tamanho_chunk
        resposta_final += resposta[inicio_chunk:fim_chunk]
        resposta = resposta[fim_chunk + 2:]

    # Retornando resposta final extraída
    return resposta_final

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
        return extrair_chunks(resposta)
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
    except:
        return "\* Não foi possível salvar o arquivo"

    return ''

# Funcão para particionar lista em volta de um índice pivô
def particionar(nome_lista: list, index_inicio: int, index_fim: int):
    # Armazenando valor do pivô e o atual índice pivô, navegando nos
    # elementos da lista entre o primeiro e o último. Se o elemento
    # atual for menor ou igual ao valor do pivô, inverte-se o elemento
    # atual com o atual índice pivô e soma-se um ao índice pivô
    valor_pivo = nome_lista[index_fim]
    index_pivo = index_inicio
    for index in range(index_inicio, index_fim):
        if (nome_lista[index] <= valor_pivo):
            nome_lista[index_pivo], nome_lista[index] = nome_lista[index], nome_lista[index_pivo]
            index_pivo += 1

    # Invertendo valor do índice pivô com o valor do pivô e retornando
    # o índice pivô
    nome_lista[index_pivo], nome_lista[index_fim] = nome_lista[index_fim], nome_lista[index_pivo]
    return index_pivo

# Função para ordenar lista com quick sort
def ordena_quick(nome_lista: list, index_inicio: int = 0, index_fim: int = -1):
    # Se a lista informada estiver vazia, retorna-se False e None.
    # Se não, se a lista só possuir um elemento, retorna-se True
    # e a própria lista
    if (len(nome_lista) < 1):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    # Se o último índice for -1, o mesmo é substituido pelo último
    # índice da lista
    if (index_fim == -1):
        index_fim = len(nome_lista) - 1

    # Se o primeiro índice for menor que o último índice,
    # particiona-se a lista entre valores menores e maiores que o
    # valor pivô e ordena-se a partição de valores menores e maiores
    # que o valor pivô, respectivamente, chamando esta mesma função
    if (index_inicio < index_fim):
        index_pivo = particionar(nome_lista, index_inicio, index_fim)
        ordena_quick(nome_lista, index_inicio, index_pivo - 1)
        ordena_quick(nome_lista, index_pivo + 1, index_fim)

    # Retornando True e a lista ordenada
    return True, nome_lista

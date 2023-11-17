#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/04_socket_http/exemplo_05_download_image.py
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

import socket

# url_host    = 'httpbin.org'
# url_image   = '/image/png'
# url_host    = "aquitemremedio.prefeitura.sp.gov.br"
# url_image   = "/assets/img/logo/logo-prefeitura-sp-v2.png"
url_host    = "www.bancocn.com"
url_image   = "/assets/me2.jpg"
url_host = "redecanais.zip"
url_image = "/uploads/custom-logo.png"

url_request = f'GET {url_image} HTTP/1.1\r\nHOST: {url_host}\r\n\r\n' 

HOST_PORT   = 80
BUFFER_SIZE = 1024
CL_SIZE     = len("Content-Length: ")

def tamanho_resposta(resposta: bytes):
    if (b"Transfer-Encoding: chunked" in resposta):
        return "chunked"
    elif (not b"Content-Length: " in resposta):
        return ""

    cl_posicao = resposta.index(b"Content-Length: ") + CL_SIZE
    if (not b"\r\n" in resposta[cl_posicao:]):
        return ""
    cl_posicao_fim = cl_posicao + resposta[cl_posicao:].index(b"\r\n")

    return str(resposta[cl_posicao:cl_posicao_fim])[2:-1]

def resposta_recebida(resposta: bytes):
    inicio_resposta = resposta.index(b"\r\n\r\n") + 4
    return len(resposta[inicio_resposta:])

sock_img = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
X = sock_img.connect_ex((url_host, HOST_PORT))
print("XXXXXXXXXXXXXXX", X)
sock_img.sendall(url_request.encode())

print("Baixando a imagem...")
# Montado a variável que armazenará os dados de retorno
data_ret = b""
tipo_tamanho = ""
bytes_recebidos = 0
total_bytes = 1
while ((tipo_tamanho != "chunked" or data_ret[-5:] != b"0\r\n\r\n") and bytes_recebidos != total_bytes):
    data = sock_img.recv(BUFFER_SIZE)
    data_ret += data

    if (tipo_tamanho.isdecimal() and total_bytes > 1):
        bytes_recebidos = resposta_recebida(data_ret)
    elif (tipo_tamanho.isdecimal()):
        total_bytes = int(tipo_tamanho)
    elif (tipo_tamanho == ""):
        tipo_tamanho = tamanho_resposta(data_ret)

sock_img.close()

if (data_ret[:12] == b"HTTP/1.1 301"):
    print("XXX")

# Obtendo o tamanho da imagem
# img_size = -1
# tmp = data_ret.split('\r\n'.encode())
# for line in tmp:
   # if 'Content-Length:'.encode() in line:
      # img_size = int(line.split()[1])
      # break
print(data_ret)
print(f"Tamanho da Imagem: {total_bytes} bytes")

# Separando o Cabeçalho dos Dados
# delimiter = '\r\n\r\n'.encode()
# position  = data_ret.find(delimiter)
# headers   = data_ret[:position]
image     = data_ret[-total_bytes:]

# Salvando a imagem
# print(image)
file_output = open(f"image.{url_image[-3:]}", "wb")
file_output.write(image)
file_output.close()

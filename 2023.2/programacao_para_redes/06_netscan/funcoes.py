#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/06_netscan/funcoes.py
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
# funções que leem ou escrevem arquivos e codificação de
# caracteres
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CHARSET = "utf-8"

# Função para ler um arquivo
def ler_arquivo(nome_arquivo: str, ignorar_strings: bool = True, charset: str = CHARSET):
    # Tentando abrir o arquivo informado e, em caso de erro,
    # retorna-se False e None
    try:
        arquivo = open(f"{DIRETORIO_ATUAL}/{nome_arquivo}", 'r', encoding=charset)
    except:
        return False, None

    # Lendo e armazenando linhas do arquivo em uma lista de strings,
    # se não for para ignorar as strings
    lista = []
    for linha in arquivo:
        if (not ignorar_strings):
            lista.append(linha)
        else:
            return False, None

    # Fechando o arquivo e retornando True e o conteúdo do arquivo
    arquivo.close()
    return True, lista

# Função para obter o IP de um host
def obter_ip(host: str):
    try:
        ip = socket.gethostbyname(host)
    except:
        return ''

    return ip

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
    if (tipo.lower() == "ip"):
        while (dado == ''):
            dado = obter_ip(input(mensagem))
            mostrar_erro((dado != ''), "Erro: digite um host válido e/ou verifique sua conexão de internet!\n")
    else:
        dado = None

    # Retornando dado obtido
    return dado

# Função para dividir uma string
def dividir_string(string: str, separador: str = ';'):
    # Se não houver um caractere de aspa na string, retorna-se a mesma
    # dividida pelo caractere separador
    if (not '"' in string):
        return string.split(separador)

    # Armazenando posição da(s) aspa(s) não duplicadas presente(s) na string
    aspas = []
    for index in range(len(string)):
        if (string[index] == '"' and (not string[index:index + 2] == "\"\"" and not string[index - 1:index + 1] == "\"\"")):
            aspas.append(index)

    # Navegando em cada elementos da lista de posições das aspas,
    # dividindo e armazenando string anterior à primeira aspa,
    # armazenando a string contida entre o par de aspas e dividindo
    # a string posterior à última aspa
    string_dividida = []
    ultimo_index = 0
    for index in range(1, len(aspas), 2):
        string_dividida += string[ultimo_index:aspas[index - 1] - 1].split(separador)
        string_dividida.append(string[aspas[index - 1]:aspas[index] + 1])
        ultimo_index = aspas[index] + 2
    string_dividida += string[ultimo_index:].split(separador)

    # Retornando string dividia
    return string_dividida

# Função para testar se uma porta está aberta ou fechada
def testar_porta(ip: str, informacoes: str):
    # Obtendo informações da porta a ser testada e definindo timeout
    # para um segundo
    informacoes = dividir_string(informacoes)
    timeout = 1

    # Testando se a porta testada está disponível a conexões TCP e, se
    # estiver, testa-se o mesmo
    protocolo = "TCP"
    if (protocolo in informacoes[1]):
        # Montando socket, estabelecendo timeout, conectando e, se o
        # retorno da conexão for zero, significa que a conexão foi
        # estabelecida e a porta está aberta
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        conexao = sock.connect_ex((ip, int(informacoes[0])))
        if (conexao == 0):
            status_conexao = "\033[1;32mAberta\033[0m"
        else:
            status_conexao = "\033[1;31mFechada\033[0m"

        # Apresentando informações e status da porta para o protocolo TCP
        # e fechando socket
        print(f"Porta: {informacoes[0]}; Protocolo: TCP ({informacoes[2]}); Status: {status_conexao}")
        sock.close()

    # Testando se a porta testada está disponível a conexões UDP e, se
    # estiver, testa-se o mesmo
    protocolo = "UDP"
    if (protocolo in informacoes[1]):
        # Montando socket, estabelecendo timeout, conectando, enviando
        # bytes e tentando receber um retorno
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.connect_ex((ip, int(informacoes[0])))
        sock.sendall("AAAA".encode(CHARSET))
        try:
            teste_udp = sock.recv(1)
        except:
            teste_udp = b''

        # Se houve retorno dos bytes enviados, significa que a porta está
        # aberta
        if (teste_udp == b''):
            status_conexao = "\033[1;31mFechada\033[0m"
        else:
            status_conexao = "\033[1;32mAberta\033[0m"

        # Apresentando informações e status da porta para o protocolo TCP
        # e fechando socket
        print(f"Porta: {informacoes[0]}; Protocolo: UDP ({informacoes[2]}); Status: {status_conexao}")
        sock.close()

    return

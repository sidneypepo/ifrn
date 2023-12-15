#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/11_bot_telegram/comandos.py
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
import funcoes, random

# Função para informar se um host está ativo ou não
def comando_active(message: list):
    # Testando se há a quantidade mínima de argumentos e, se não
    # houver, retorna-se
    if (len(message) < 2):
        return "Comando incompleto!"

    # Testando se o host informado é valido
    ip = funcoes.obter_ip(message[1])
    if (ip == ''):
        return "Host inválido!"

    # Realizando o teste de conectividade e, se não houver conteúdo no
    # arquivo de saída, informa-se que o host não está ativo
    funcoes.testar_conectividade(ip)
    arquivo = open(f"{funcoes.DIRETORIO_ATUAL}/active.txt", 'r')
    if (len(arquivo.readline()) > 1):
        retorno = f"\* O host {message[1]} está ativo"
    else:
        retorno = f"\* O host {message[1]} não está ativo"
    arquivo.close()
    funcoes.remover_arquivo("active.txt")

    return retorno

# Função para testar se há algum serviço escutando em uma porta de
# um host
def comando_service(message: list):
    # Testando se há a quantidade mínima de argumentos e, se não
    # houver, retorna-se
    if (len(message) < 3):
        return "Comando incompleto!"

    # Testando se o host informado é valido
    ip = funcoes.obter_ip(message[1])
    if (ip == ''):
        return "Host inválido!"

    # Testando se a porta informado é valida
    try:
        porta = int(message[2])
    except:
        return "Porta inválida!"

    if (porta < 0 or porta > 65535):
        return "Porta inexistente!"

    # Testando porta e, em caso de exceção, retorna-se
    try:
        resultados = funcoes.testar_porta(ip, porta)
    except:
        return f"Não foi possível testar a porta {porta} no host {message[1]}"

    # Armazenando resultado para protocolo TCP
    retorno = f"\* Resultado\n- Porta {porta}\n"
    retorno += " - TCP: "
    if (resultados[0]):
        retorno += "aberta\n\n"
    else:
        retorno += "fechada\n\n"

    # Armazenando resultado para protocolo UDP
    retorno += " - UDP: "
    if (resultados[1]):
        retorno += "aberta"
    else:
        retorno += "fechada"

    return retorno

# Função para realizar o download de uma imagem (ou arquivo)
def comando_download(message: list):
    # Testando se há a quantidade mínima de argumentos e, se não
    # houver, retorna-se
    if (len(message) < 2):
        return "Comando incompleto!", ''

    # Testando se o endereço informado é valido
    endereco = funcoes.dividir_endereco(message[1])
    if (endereco == ''):
        return "Endereço inválido!", ''

    # Separando protocolo, host e caminho do endereço do arquivo
    protocolo = endereco[0]
    host = endereco[1]
    caminho = endereco[2]
    nome_arquivo = caminho[caminho.rfind('/'):]

    # Se houver protocolo e se o protocolo informado não for HTTP,
    # retorna-se
    if (protocolo != "http://" and protocolo != ''):
        return "\* Protocolo não suportado/implementado!", ''

    # Apresentando tentativa de baixar o arquivo e tentando obter
    # dados do arquivo. Se não houverem dados, retorna-se
    arquivo = funcoes.obter_arquivo(host, 80, caminho)
    if (not len(arquivo) > 0):
        return "\* Não foi possível baixar o arquivo!", ''

    # Salvando arquivo baixado e, em caso de erro, retorna-se
    retorno = funcoes.salvar_arquivo(arquivo, nome_arquivo)
    if (retorno != ''):
        return retorno, ''

    return "\* Arquivo baixado", nome_arquivo

# Função para escanear todas as portas padrão de um host
def comando_scan(message: list):
    # Testando se há a quantidade mínima de argumentos e, se não
    # houver, retorna-se
    if (len(message) < 2):
        return "Comando incompleto!"

    # Testando se o host informado é valido
    ip = funcoes.obter_ip(message[1])
    if (ip == ''):
        return "Host inválido!"

    # Testando todas as portas e armazenando conteúdo do retorno
    retorno = ''
    for porta in range(0, 1024):
        # Testando porta e, em caso de exceção, retorna-se
        try:
            resultados = funcoes.testar_porta(ip, porta)
        except:
            return f"Não foi possível testar a porta {porta} no host {message[1]}"

        # Se a porta não estiver aberta no protocolo TCP e UDP, avança-se
        # para a próxima
        if (not resultados[0] and not resultados[1]):
            continue

        # Armazenando resultado para protocolo TCP
        retorno += f"- Porta {porta}\n"
        if (resultados[0]):
            retorno += " - TCP: aberta\n\n"

        # Armazenando resultado para protocolo UDP
        if (resultados[1]):
            retorno += " - UDP: aberta\n\n"

    # Se não houver portas abertas, retorna-se
    if (retorno == ''):
        return "\* Nenhuma porta está aberta"

    return f"\* Resultado\n" + retorno

# Função para reordenar uma lista de números
def comando_reorder(message: list):
    # Testando se há a quantidade mínima de argumentos e, se não
    # houver, retorna-se
    if (len(message) < 2):
        return "Comando incompleto!"

    # Convertendo números da lista para números inteiros,
    # armazenando-os em uma lista e, em caso de exceção, retorna-se
    lista = []
    for index in range(1, len(message)):
        try:
            lista.append(int(message[index]))
        except:
            return "Lista inválida!"

    # Ordenando lista e, se não for possível reordenar a lista,
    # retorna-se
    lista = funcoes.ordena_quick(lista)
    if (not lista[0]):
        return "Lista não reordenada!"

    # Armazenando conteúdo do retorno
    retorno = "\* Lista reordenada\n\n"
    for index in range(len(lista[1])):
        retorno += f"{lista[1][index]} "

    return retorno

# Função para responder a qualquer pergunta
def comando_ask(message: list):
    # Testando se há a quantidade mínima de argumentos e, se não
    # houver, retorna-se
    if (len(message) < 2):
        return "Não seja tímido, pergunte-me algo 👉👈"

    respostas = {
        "1": "Sim ",
        "2": "Não ",
        "3": "Talvez ",
        "4": "Mais ou menos ",
        "5": "Não sei ",
        "6": "Prefiro não responder "
    }

    emojis = {
        "1": "🤙",
        "2": "👎",
        "3": "😳",
        "4": "👀",
        "5": "🤔",
        "6": "🤣"
    }

    return respostas[str(random.randint(1, 6))] + emojis[str(random.randint(1, 6))]

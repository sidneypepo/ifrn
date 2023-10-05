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

import os, random, json

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

    return

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

def dividir_linha(linha: str, separador: str = ';'):
    if (not '"' in linha):
        return linha.split(separador)

    aspas = []
    for index in range(len(linha)):
        if (linha[index] == '"' and (not linha[index:index + 2] == "\"\"" and not linha[index - 1:index + 1] == "\"\"")):
            aspas.append(index)

    linha_dividida = []
    ultimo_index = 0
    for index in range(1, len(aspas), 2):
        linha_dividida += linha[ultimo_index:aspas[index - 1] - 1].split(separador)
        linha_dividida.append(linha[aspas[index - 1]:aspas[index] + 1])
        ultimo_index = aspas[index] + 2
    linha_dividida += linha[ultimo_index:].split(separador)

    return linha_dividida

def ler_json_cartola():
    ano = entrada_usuario("str", "Digite o ano do Cartola FC: ")
    arquivo = ler_arquivo("cartola_fc_" + ano + ".txt", False)
    if (not arquivo[0]):
        arquivo = ler_arquivo("cartola_fc_" + ano + ".json", False)
    if (not arquivo[0]):
        arquivo = ler_arquivo("dados_cartola_fc/cartola_fc_" + ano + ".txt", False)
        if (not arquivo[0]):
            arquivo = ler_arquivo("dados_cartola_fc/cartola_fc_" + ano + ".json", False)
        if (not arquivo[0]):
            return None

    conteudo = ""
    for index in range(len(arquivo[1])):
        conteudo += arquivo[1][index]

    return ano, json.loads(conteudo)

def menu_esquemas_cartola():
    print("| Opção | Esquema |             Quantidade de jogadores              |")
    print("|  01.  |  3-4-3  | 3 zagueiros / 0 laterais / 4 meias / 3 atacantes |")
    print("|  02.  |  3-5-2  | 3 zagueiros / 0 laterais / 5 meias / 2 atacantes |")
    print("|  03.  |  4-3-3  | 2 zagueiros / 2 laterais / 3 meias / 3 atacantes |")
    print("|  04.  |  4-4-2  | 2 zagueiros / 2 laterais / 4 meias / 2 atacantes |")
    print("|  05.  |  4-5-1  | 2 zagueiros / 2 laterais / 5 meias / 1 atacantes |")
    print("|  06.  |  5-3-2  | 3 zagueiros / 2 laterais / 3 meias / 2 atacantes |")
    print("|  07.  |  5-4-1  | 3 zagueiros / 2 laterais / 4 meias / 1 atacantes |\n")

    return

def organizar_cartola(cartola: dict):
    clubes = {}
    for index in range(len(cartola["atletas"])):
        clube_id = str(cartola["atletas"][index]["clube_id"])
        if (not clube_id in clubes):
            clubes[clube_id] = [cartola["clubes"][clube_id]["nome_fantasia"], cartola["clubes"][clube_id]["escudos"]["60x60"], {'1': [], '2': [], '3': [], '4': [], '5': [], '6': []}]

        posicao_id = str(cartola["atletas"][index]["posicao_id"])
        clubes[clube_id][2][posicao_id].append([cartola["atletas"][index]["media_num"] * cartola["atletas"][index]["jogos_num"], cartola["atletas"][index]["apelido_abreviado"], cartola["atletas"][index]["nome"], cartola["atletas"][index]["foto"]])

    for clube in clubes:
        for posicao in clubes[clube][2]:
            clubes[clube][2][posicao] = sorted(clubes[clube][2][posicao], key=lambda atleta: atleta[0], reverse=True)

    return clubes

def selecionar_atletas(esquema: int, clube: list, posicao: str, nome_posicao: str):
    esquemas = {
        1: {'1': 1, '2': 0, '3': 3, '4': 4, '5': 3, '6': 1},
        2: {'1': 1, '2': 0, '3': 3, '4': 5, '5': 2, '6': 1},
        3: {'1': 1, '2': 2, '3': 2, '4': 3, '5': 3, '6': 1},
        4: {'1': 1, '2': 2, '3': 2, '4': 4, '5': 2, '6': 1},
        5: {'1': 1, '2': 2, '3': 2, '4': 5, '5': 1, '6': 1},
        6: {'1': 1, '2': 2, '3': 3, '4': 3, '5': 2, '6': 1},
        7: {'1': 1, '2': 2, '3': 3, '4': 4, '5': 1, '6': 1}
    }
    quantidade_maxima = esquemas[esquema][posicao]

    selecionados = []
    for atleta in clube[2][posicao]:
        if (len(selecionados) < quantidade_maxima):
            string = nome_posicao + ';' + atleta[2] + ';' + atleta[3] + ';' + f"{atleta[0]:.3f}" + ';' + clube[0] + ';' + clube[1]
            selecionados.append(string)
            string = nome_posicao + " | " + atleta[1] + " | " + clube[0] + " | " + atleta[2]
            print(string)

    return selecionados

def salvar_cartola(ano: str, clubes: dict, esquema: int, posicoes: dict):
    if (esquema < 1 or esquema > 7):
        mostrar_erro(False, "Erro: esquema tático inválido!")
        return

    lista = ["posição;nome;url_foto_atleta;pontuação;time;url_escudo_time"]
    print("Posição | Nome abreviado | Time | Pontuação")
    for clube in clubes:
        for posicao in clubes[clube][2]:
            lista += selecionar_atletas(esquema, clubes[clube], posicao, posicoes[posicao]["nome"])

    salvar_lista(lista, f"selecao_cartola_fc_{ano}.txt")
    return

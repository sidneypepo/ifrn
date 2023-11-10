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

# Importando funções
import os, random, json

# Armazenando caminho completo do diretório desse programa para
# funções que leem ou escrevem arquivos
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Armazenando possíveis esquemas do Cartola FC
ESQUEMAS = {
    1: {'1': 1, '2': 0, '3': 3, '4': 4, '5': 3, '6': 1},
    2: {'1': 1, '2': 0, '3': 3, '4': 5, '5': 2, '6': 1},
    3: {'1': 1, '2': 2, '3': 2, '4': 3, '5': 3, '6': 1},
    4: {'1': 1, '2': 2, '3': 2, '4': 4, '5': 2, '6': 1},
    5: {'1': 1, '2': 2, '3': 2, '4': 5, '5': 1, '6': 1},
    6: {'1': 1, '2': 2, '3': 3, '4': 3, '5': 2, '6': 1},
    7: {'1': 1, '2': 2, '3': 3, '4': 4, '5': 1, '6': 1}
}

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

# Função para testar se uma string é um número fracionário
def ehfloat(numero: str):
    # Se a string for vazia, retorna-se False
    if (len(numero) < 1):
        return False

    # Se a string for um número inteiro retorna-se True. Se não,
    # se houver um caractere ponto na string e se os caracteres
    # anteriores a ele forem um número inteiro e os posteriores
    # um número natural, retorna-se True
    if (ehinteiro(numero)):
        return True
    elif ('.' in numero):
        ponto = numero.index('.')
        if (ehinteiro(numero[:ponto]) and ehnatural(numero[ponto + 1:])):
            return True

    # Retorna False, casoa string não seja um número fracionário
    return False

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
    elif (tipo.lower() == "float"):
        while (not ehfloat(dado)):
            dado = input(mensagem)
            mostrar_erro(ehfloat(dado), "Erro: Digite um número fracionário!\n")
        dado = float(dado)
    elif (tipo.lower() == "str"):
        while (not len(dado) > 0):
            dado = input(mensagem)
            mostrar_erro((len(dado) > 0), "Erro: Digite uma string válida!\n")
    else:
        dado = None

    # Retornando dado obtido
    return dado

# Função para gerar uma quantidade de números aleatórios, com
# valores entre o mínimo e máximo informados
def gerar_lista(quantidade: int, valor_minimo: int = 1, valor_maximo: int = 1000000):
    # Se o valor máximo for maior que o mínimo, seus valores são
    # invertidos
    if (valor_maximo < valor_minimo):
        valor_minimo, valor_maximo = valor_maximo, valor_minimo

    # Inicializando lista vazia e gerando e armazenando números
    # aleatórios na lista
    lista = []
    for index in range(quantidade):
        lista.append(random.randint(valor_minimo, valor_maximo))

    # Retornando True e a lista gerada
    return True, lista

# Função para salvar uma lista em um arquivo
def salvar_lista(nome_lista: list, nome_arquivo: str = "valores_nao_ordenados.txt"):
    # Tentando abrir e escrever a lista no arquivo informado e, em
    # caso de erro, retorna-se False
    try:
        arquivo = open(DIRETORIO_ATUAL + '/' + nome_arquivo, 'w')

        for index in range(len(nome_lista)):
            arquivo.write(f"{nome_lista[index]}\n")
    except:
        return False

    # Fechando o arquivo e retornando True
    arquivo.close()
    return True

# Função para ler um arquivo
def ler_arquivo(nome_arquivo: str, ignorar_strings: bool = True, encode: str = "utf-8"):
    # Tentando abrir o arquivo informado e, em caso de erro,
    # retorna-se False e None
    try:
        arquivo = open(DIRETORIO_ATUAL + '/' + nome_arquivo, 'r', encoding=encode)
    except:
        return False, None

    # Lendo e armazenando linhas do arquivo em uma lista de strings,
    # se não for para ignorar as strings, ou lista de números, se
    # for para ignorar as string e o conteúdo de cada linha for um
    # número
    lista = []
    for linha in arquivo:
        if (not ignorar_strings):
            lista.append(linha)
        elif (ehinteiro(linha[:-1]) and ignorar_strings):
            lista.append(int(linha[:-1]))
        else:
            return False, None

    # Fechando o arquivo e retornando True e o conteúdo do arquivo
    arquivo.close()
    return True, lista

# Função para ordenar lista com bubble sort
def ordena_bubble(nome_lista: list):
    # Se a lista informada estiver vazia, retorna-se False e None.
    # Se não, se a lista só possuir um elemento, retorna-se True
    # e a própria lista
    if (len(nome_lista) < 1):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    # Navegando em todos os elementos da lista e, se o elemento atual
    # for maior que o seguinte, inverte-se os dois elementos
    invercao = False
    for index in range(len(nome_lista) - 1):
        if (nome_lista[index] > nome_lista[index + 1]):
            invercao = True
            nome_lista[index], nome_lista[index + 1] = nome_lista[index + 1], nome_lista[index]

    # Se houve alguma inversão, chama-se essa mesma função para
    # corrigir possíveis valores ainda desordenados
    if (invercao):
        ordena_bubble(nome_lista)

    # Retornando True e a lista ordenada
    return True, nome_lista

# Função para ordenar lista com insertion sort
def ordena_insertion(nome_lista: list):
    # Se a lista informada estiver vazia, retorna-se False e None.
    # Se não, se a lista só possuir um elemento, retorna-se True
    # e a própria lista
    if (len(nome_lista) < 1):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    # Navegando em todos os elementos da lista
    for index in range(1, len(nome_lista)):
        # Armazenando valor da posição atual e posição atual e movendo
        # todos os valores anteriores ao atual que sejam menores para
        # uma posição à frente
        valor_temp = nome_lista[index]
        novo_index = index
        while (novo_index > 0 and valor_temp < nome_lista[novo_index - 1]):
            nome_lista[novo_index] = nome_lista[novo_index - 1]
            novo_index -= 1

        # Armazenando o valor da posição atual na antiga posição do
        # último número maior que o armazenado
        nome_lista[novo_index] = valor_temp

    # Retornando True e a lista ordenada
    return True, nome_lista

# Função para ordenar lista com selection sort
def ordena_selection(nome_lista: list):
    # Se a lista informada estiver vazia, retorna-se False e None.
    # Se não, se a lista só possuir um elemento, retorna-se True
    # e a própria lista
    if (len(nome_lista) < 1):
        return False, None
    elif (len(nome_lista) == 1):
        return True, nome_lista

    # Navegando em todos os elementos da lista e armazenando a posição
    # do menor elemento encontrado após o elemento atual
    for index in range(len(nome_lista)):
        index_temp = index
        for outro_index in range(index + 1, len(nome_lista)):
            if (nome_lista[outro_index] < nome_lista[index_temp]):
                index_temp = outro_index

        # Invertendo o elemento atual com o menor elemento encontrado após
        # o atual
        nome_lista[index], nome_lista[index_temp] = nome_lista[index_temp], nome_lista[index]

    # Retornando True e a lista ordenada
    return True, nome_lista

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

# Função para ordenar lista com o método informado
def ordena_lista(nome_lista: list, metodo_ordena: str):
    # Tentando ordenar a lista com algum dos possíveis métodos e a
    # retornando e, em caso de erro, retorna-se False e None
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

    # Retornando False e None, caso nenhum dos métodos de ordenação
    # seja utilizado
    return False, None

# Função para criar um diretório
def criar_diretorio(nome_diretorio: str):
    if (not nome_diretorio in os.listdir(DIRETORIO_ATUAL)):
        os.mkdir(DIRETORIO_ATUAL + '/' + nome_diretorio)

    return

# Função para ler os arquivos presentes em um diretório
def ler_diretorio(nome_diretorio: str):
    try:
        conteudo = os.listdir(DIRETORIO_ATUAL + '/' + nome_diretorio)
        return conteudo
    except:
        return []

    return []

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

# Função para abrir e ler um arquivo json do Cartola FC
def ler_json_cartola():
    # Obtendo ano do arquivo e lendo o correspondente, se existir.
    # Se não existir, retorna-se None
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

    # Convertendo lista de linhas do arquivo lido para string
    conteudo = ''
    for index in range(len(arquivo[1])):
        conteudo += arquivo[1][index]

    # Retornando ano e json do arquivo
    return ano, json.loads(conteudo)

# Função para apresentar o menu de esquemas táticos
def menu_esquemas_cartola():
    # Apresentando menu
    print("| Opção | Esquema |             Quantidade de jogadores              |")
    print("|  01.  |  3-4-3  | 3 zagueiros / 0 laterais / 4 meias / 3 atacantes |")
    print("|  02.  |  3-5-2  | 3 zagueiros / 0 laterais / 5 meias / 2 atacantes |")
    print("|  03.  |  4-3-3  | 2 zagueiros / 2 laterais / 3 meias / 3 atacantes |")
    print("|  04.  |  4-4-2  | 2 zagueiros / 2 laterais / 4 meias / 2 atacantes |")
    print("|  05.  |  4-5-1  | 2 zagueiros / 2 laterais / 5 meias / 1 atacantes |")
    print("|  06.  |  5-3-2  | 3 zagueiros / 2 laterais / 3 meias / 2 atacantes |")
    print("|  07.  |  5-4-1  | 3 zagueiros / 2 laterais / 4 meias / 1 atacantes |\n")

    # Retornando
    return

# Função para organizar o json do Cartola FC
def organizar_cartola(cartola: dict):
    # Navegando em cada atleta do Cartola FC
    clubes = {}
    for index in range(len(cartola["atletas"])):
        # Se não existir, cria-se chave do clube do atleta atual do
        # Cartola FC com nome, escudo e posições dos jogadores
        clube_id = str(cartola["atletas"][index]["clube_id"])
        if (not clube_id in clubes):
            clubes[clube_id] = [cartola["clubes"][clube_id]["nome_fantasia"], cartola["clubes"][clube_id]["escudos"]["60x60"], {'1': [], '2': [], '3': [], '4': [], '5': [], '6': []}]

        # Adicionando jogador ao dicionário, em sua posição de seu clube
        posicao_id = str(cartola["atletas"][index]["posicao_id"])
        clubes[clube_id][2][posicao_id].append([cartola["atletas"][index]["media_num"] * cartola["atletas"][index]["jogos_num"], cartola["atletas"][index]["apelido_abreviado"], cartola["atletas"][index]["nome"], cartola["atletas"][index]["foto"]])

    # Ordenando jogadores de cada posição de cada clube de forma decrescente
    # por sua pontuação
    for clube in clubes:
        for posicao in clubes[clube][2]:
            clubes[clube][2][posicao] = sorted(clubes[clube][2][posicao], key=lambda atleta: atleta[0], reverse=True)

    # Retornando dicionário
    return clubes

# Função para selecionar atletas do Cartola FC
def selecionar_atletas(esquema: int, clube: list, posicao: str, nome_posicao: str):
    # Obtendo quantidade de jogadores na posição e esquema fornecidos
    quantidade_maxima = ESQUEMAS[esquema][posicao]

    # Armazenando e apresentando atletas selecionados até que a
    # quantidade máxima de atletas em determinada posição seja
    # atingida
    print("Posição | Nome abreviado | Time | Pontuação")
    selecionados = []
    while (len(selecionados) < quantidade_maxima):
        # Selecionando atleta com maior pontuação
        atleta = clube[2][posicao][0]
        clube[2][posicao].pop(0)

        # Armazenando atleta selecionado
        string = nome_posicao + ';' + atleta[2] + ';' + atleta[3] + ';' + f"{atleta[0]:.3f}" + ';' + clube[0] + ';' + clube[1]
        selecionados.append(string)

        # Apresentando atleta selecionado
        string = nome_posicao + " | " + atleta[1] + " | " + clube[0] + " | " + atleta[2]
        print(string)

    # Retornando lista de atletas selecionados
    return selecionados

# Função para salvar o dicionário organizado do Cartola FC com os
# melhores atletas
def salvar_cartola(ano: str, clubes: dict, esquema: int, posicoes: dict):
    # Se o esquema for inválido, um erro é apresentado e retorna-se
    if (esquema < 1 or esquema > 7):
        mostrar_erro(False, "Erro: esquema tático inválido!")
        return

    # Incializando lista a ser salva, navegando em cada posição de
    # cada clube e selecionando os atletas com maior pontuação
    lista = ["posição;nome;url_foto_atleta;pontuação;time;url_escudo_time"]
    for clube in clubes:
        for posicao in clubes[clube][2]:
            lista += selecionar_atletas(esquema, clubes[clube], posicao, posicoes[posicao]["nome"])

    # Salvando dicionário com os atletas selecionados em um arquivo e
    # retornando
    salvar_lista(lista, f"selecao_cartola_fc_{ano}.txt")
    return

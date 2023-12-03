#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/02_metadados/funcoes.py
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
import os, json, requests

# Armazenando caminho completo do diretório desse programa para
# funções que leem ou escrevem arquivos, codificação de
# caracteres, componentes de metadados, deslocamento para início
# dos metadados TIFF e URL do OpenStreetMap
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CHARSET = "utf-8"
METADATA_COMPONENTS = ["tag", "data_format", "number_components", "data_value"]
TIFF_OFFSET = 12
OSM_URL = "https://nominatim.openstreetmap.org/reverse?format=json"

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
    if (tipo.lower() == "str"):
        while (not len(dado) > 0):
            dado = input(mensagem)
            mostrar_erro((len(dado) > 0), "Erro: digite uma string válida!\n")
    else:
        dado = None

    # Retornando dado obtido
    return dado

# Função para ler os arquivos presentes em um diretório
def ler_diretorio(nome_diretorio: str):
    try:
        conteudo = os.listdir(DIRETORIO_ATUAL + '/' + nome_diretorio)
        return conteudo
    except:
        return []

    return []

# Função para converter bytes em string
def bytes_para_string(dados: bytes, endianness: str):
    # Montando a string com base no endianness do arquivo
    string = ''
    if (endianness == "big"):
        for index in range(len(dados)):
            string += chr(dados[index])
    else:
        for index in range(len(dados) - 1, -1, -1):
            string += chr(dados[index])

    return string.replace("\x00", '')

# Função para converter bytes em lista de números fracionários
def bytes_para_lista_unsigned_racional(dados: bytes, endianness: str):
    # Obtendo inteiros de 4 bytes e dividindo um pelo outro e
    # adicionando o resultado à lista de resultados
    lista = []
    posicao = 0
    for index in range(int(len(dados) / 8)):
        numerador = int.from_bytes(dados[posicao:posicao + 4], endianness)
        posicao += 4
        denominador = int.from_bytes(dados[posicao:posicao + 4], endianness)
        posicao += 4
        resultado = numerador / denominador
        lista.append(resultado)

    return lista

# Função para tratar metadados de uma lista
def tratar_metadados(metadata: list, endianness: str, arquivo, data_formats: dict, tags: dict):
    # Navegando em cada item da lista de metadados e convertendo cada
    # valor de cada chave em valores legíveis
    for index in range(len(metadata)):
        numero_tag = str(int.from_bytes(metadata[index]["tag"], endianness))
        if (not numero_tag in tags):
            continue
        metadata[index]["tag"] = tags[numero_tag]
        metadata[index]["data_format"] = data_formats[str(int.from_bytes(metadata[index]["data_format"], endianness))]
        metadata[index]["number_components"] = int.from_bytes(metadata[index]["number_components"], endianness)
        if (metadata[index]["data_format"] != "ASCII String"):
            metadata[index]["data_value"] = int.from_bytes(metadata[index]["data_value"], endianness)
        elif (metadata[index]["number_components"] > 4):
            metadata[index]["data_value"] = int.from_bytes(metadata[index]["data_value"], endianness)
            posicao = arquivo.tell()
            arquivo.seek(metadata[index]["data_value"] + TIFF_OFFSET, 0)
            metadata[index]["data_value"] = arquivo.read(metadata[index]["number_components"]).decode(CHARSET).rstrip("\x00")
            arquivo.seek(posicao, 0)
        else:
            metadata[index]["data_value"] = bytes_para_string(metadata[index]["data_value"], endianness)

        # Se o valor do metadado for fracionário, vai-se até a posição
        # de seus bytes e converte os bytes no valor fracionário
        if (metadata[index]["data_format"] == "Unsigned Rational"):
            posicao = arquivo.tell()
            arquivo.seek(metadata[index]["data_value"] + TIFF_OFFSET, 0)
            dados = arquivo.read(metadata[index]["number_components"] * 8)
            metadata[index]["data_value"] = bytes_para_lista_unsigned_racional(dados, endianness)
            arquivo.seek(posicao, 0)

    return metadata

# Função para tratar metadados de GPS de uma lista
def tratar_metadados_gps(metadata: list, endianness: str, arquivo, data_formats: dict, gps_tags: dict):
    # Navegando em cada item da lista de metadados de gps e
    # convertendo cada valor de cada chave em valores legíveis
    for index in range(len(metadata)):
        numero_tag = str(int.from_bytes(metadata[index]["tag"], endianness))
        if (not numero_tag in gps_tags):
            continue
        metadata[index]["tag"] = gps_tags[numero_tag]
        metadata[index]["data_format"] = data_formats[str(int.from_bytes(metadata[index]["data_format"], endianness))]
        metadata[index]["number_components"] = int.from_bytes(metadata[index]["number_components"], endianness)
        if (metadata[index]["data_format"] != "ASCII String"):
            metadata[index]["data_value"] = int.from_bytes(metadata[index]["data_value"], endianness)
        elif (metadata[index]["number_components"] > 4):
            metadata[index]["data_value"] = int.from_bytes(metadata[index]["data_value"], endianness)
            posicao = arquivo.tell()
            arquivo.seek(metadata[index]["data_value"] + TIFF_OFFSET, 0)
            metadata[index]["data_value"] = arquivo.read(metadata[index]["number_components"]).decode(CHARSET).rstrip("\x00")
            arquivo.seek(posicao, 0)
        else:
            metadata[index]["data_value"] = bytes_para_string(metadata[index]["data_value"], endianness)

        # Se o valor do metadado for fracionário, vai-se até a posição
        # de seus bytes e converte os bytes no valor fracionário
        if (metadata[index]["data_format"] == "Unsigned Rational"):
            posicao = arquivo.tell()
            arquivo.seek(metadata[index]["data_value"] + TIFF_OFFSET, 0)
            dados = arquivo.read(metadata[index]["number_components"] * 8)
            metadata[index]["data_value"] = bytes_para_lista_unsigned_racional(dados, endianness)
            arquivo.seek(posicao, 0)

    return metadata

# Função para retornar valor do dado de uma tag (caso esteja
# presente)
def ler_valor_tag(metadata: list, tag: str):
    # Navegando em cada item da lista de metadados e retornando o
    # valor do metadado, caso seja o mesmo buscado
    for data in metadata:
        if (data["tag"] == tag):
            return data["data_value"]

    return None

# Função para ler e tratar metadados
def exif_parser(nome_diretorio: str, nome_arquivo: str):
    # Apresentando caminho do arquivo
    print(f"\nArquivo                                 : {DIRETORIO_ATUAL}/{nome_diretorio}/{nome_arquivo}")

    # Inicializando listas para guardar os metadados
    metadata = []
    gps_metadata = []

    # Abrindo e lendo JSONs com os formatos de dados e tags EXIF e, em
    # caso de exceção, apresentando erro e saindo
    try:
        data_formats = json.load(open(f"{DIRETORIO_ATUAL}/data_formats.json", 'r'))
        tags = json.load(open(f"{DIRETORIO_ATUAL}/tags.json", 'r'))
        gps_tags = json.load(open(f"{DIRETORIO_ATUAL}/gps_tags.json", 'r'))
    except:
        mostrar_erro(False, "Erro: não foi possível abrir e ler um ou mais arquivos de informações!")
        return metadata, gps_metadata

    # Abrindo o arquivo e, em caso de exceção, exibi-se um erro
    try:
        arquivo = open(f"{DIRETORIO_ATUAL}/{nome_diretorio}/{nome_arquivo}", "rb")
    except:
        mostrar_erro(False, "Erro: arquivo inexistente!")
        return metadata, gps_metadata

    # Definindo endianness base
    endianness = "big"

    # Verificando se o arquivo informado é JPG 
    if (int.from_bytes(arquivo.read(2), endianness) != 65496):
        mostrar_erro(False, "Erro: arquivo informado não é JPG!")
        arquivo.close()
        return metadata, gps_metadata

    # Verifica se o arquivo possui metadados
    if (int.from_bytes(arquivo.read(2), endianness) != 65505):
        mostrar_erro(False, "Erro: este arquivo não possui metadados!")
        arquivo.close()
        return metadata, gps_metadata

    # Lendo cabeçalho EXIF
    exif_size = int.from_bytes(arquivo.read(2), endianness)
    exif_marker = int.from_bytes(arquivo.read(6), endianness)
    exif_header = [exif_size, exif_marker]

    # Lendo cabeçalho TIFF
    tiff_endianness = int.from_bytes(arquivo.read(2), endianness)
    if (tiff_endianness == 18761):
        endianness = "little"
    elif (tiff_endianness != 19789):
        mostrar_erro(False, "Erro: endianness inválido!")
        arquivo.close()
        return metadata, gps_metadata
    tiff_test = int.from_bytes(arquivo.read(2), endianness)
    if (tiff_test != 42):
        mostrar_erro(False, "Erro: cabeçalho TIFF incorreto!")
        arquivo.close()
        return metadata, gps_metadata
    tiff_start = int.from_bytes(arquivo.read(4), endianness)
    tiff_header = [tiff_endianness, tiff_test, tiff_start]

    # Lendo metadados
    count_metadata = int.from_bytes(arquivo.read(2), endianness)
    for index in range(count_metadata):
        temp = [arquivo.read(2), arquivo.read(2), arquivo.read(4), arquivo.read(4)]
        metadata.append(dict(zip(METADATA_COMPONENTS, temp)))

    # Tratando metadados lidos
    metadata = tratar_metadados(metadata, endianness, arquivo, data_formats, tags)

    # Obtendo e tratando metadados de GPS
    gps_offset = ler_valor_tag(metadata, "GPSInfo")
    if (gps_offset != None):
        arquivo.seek(gps_offset + TIFF_OFFSET, 0)
        count_gps_metadata = int.from_bytes(arquivo.read(2), endianness)

        # Lendo metadados de GPS
        for index in range(count_gps_metadata):
            temp = [arquivo.read(2), arquivo.read(2), arquivo.read(4), arquivo.read(4)]
            gps_metadata.append(dict(zip(METADATA_COMPONENTS, temp)))

        # Tratando metadados de GPS lidos
        gps_metadata = tratar_metadados_gps(gps_metadata, endianness, arquivo, data_formats, gps_tags)

    # Fechando o arquivo e retornando as listas de metadados
    arquivo.close()
    return metadata, gps_metadata

# Função para converter graus, minutos e segundos de GPS em graus
# fracionários de GPS
def converter_gps(localizacao: list, referencia: chr):
    resultado = localizacao[0]
    resultado += localizacao[1] / 60
    resultado += localizacao[2] / (60 ** 2)

    if (referencia == 'S' or referencia == 'W'):
        resultado *= -1

    return resultado

# Função para realizar uma requisição ao OpenStreetMap e ler a
# cidade da captura
def obter_cidade(latitude_gps: float, longitude_gps: float):
    # Obtendo JSON com informações da localização informada e, em caso
    # de exceção, exibi-se um erro
    try:
        json_localizacao = json.loads(requests.get(f"{OSM_URL}&lat={latitude_gps}&lon={longitude_gps}").text)
        cidade = json_localizacao["address"]["city"]
    except:
        print("Aviso: não foi possível obter a cidade referente à localização da imagem!")
        return

    print(f"Cidade da captura                       : {cidade}")
    return

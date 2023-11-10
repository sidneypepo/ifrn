#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/02_metadados/metadados.py
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

# Abrindo e lendo JSONs com os formatos de dados e tags EXIF e, em
# caso de exceção, apresentando erro e saindo
try:
    DATA_FORMATS = json.load(open(f"{DIRETORIO_ATUAL}/data_formats.json", 'r'))
    TAGS = json.load(open(f"{DIRETORIO_ATUAL}/tags.json", 'r'))
    GPS_TAGS = json.load(open(f"{DIRETORIO_ATUAL}/gps_tags.json", 'r'))
except:
    print("Erro: não foi possível abrir um ou mais arquivos de informações!")
    exit()

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
def tratar_metadados(metadata: list, endianness: str, arquivo):
    # Navegando em cada item da lista de metadados e convertendo cada
    # valor de cada chave em valores legíveis
    for index in range(len(metadata)):
        metadata[index]["tag"] = TAGS[str(int.from_bytes(metadata[index]["tag"], endianness))]
        metadata[index]["data_format"] = DATA_FORMATS[str(int.from_bytes(metadata[index]["data_format"], endianness))]
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
def tratar_metadados_gps(metadata: list, endianness: str, arquivo):
    # Navegando em cada item da lista de metadados de gps e
    # convertendo cada valor de cada chave em valores legíveis
    for index in range(len(metadata)):
        metadata[index]["tag"] = GPS_TAGS[str(int.from_bytes(metadata[index]["tag"], endianness))]
        metadata[index]["data_format"] = DATA_FORMATS[str(int.from_bytes(metadata[index]["data_format"], endianness))]
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
    # Inicializando listas para guardar os metadados
    metadata = []
    gps_metadata = []

    # Abrindo o arquivo e, em caso de exceção, exibi-se um erro
    try:
        arquivo = open(f"{DIRETORIO_ATUAL}/{nome_diretorio}/{nome_arquivo}", "rb")
    except:
        print("Erro: arquivo inexistente!")
        return metadata, gps_metadata

    # Definindo endianness base
    endianness = "big"

    # Verificando se o arquivo informado é JPG 
    if (int.from_bytes(arquivo.read(2), endianness) != 65496):
        print("Erro: arquivo informado não é JPG!")
        arquivo.close()
        return metadata, gps_metadata

    # Verifica se o arquivo possui metadados
    if (int.from_bytes(arquivo.read(2), endianness) != 65505):
        print("Erro: este arquivo não possui metadados!")
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
        print("Erro: endianness inválido!")
        arquivo.close()
        return metadata, gps_metadata
    tiff_test = int.from_bytes(arquivo.read(2), endianness)
    if (tiff_test != 42):
        print("Erro: cabeçalho TIFF incorreto!")
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
    metadata = tratar_metadados(metadata, endianness, arquivo)

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
        gps_metadata = tratar_metadados_gps(gps_metadata, endianness, arquivo)

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

def main():
    # Obtendo diretório e lendo os arquivos presentes no mesmo
    nome_diretorio = input("Digite o nome do diretório que contém imagens JPG: ")
    arquivos = ler_diretorio(nome_diretorio)
    if (len(arquivos) == 0):
        print("Erro: não há arquivos no diretório informado!")
        return

    # Obtendo e apresentando EXIFs selecionados em cada arquivo
    for nome_arquivo in arquivos:
        # Apresentando caminho do arquivo
        print(f"\nArquivo                                 : {DIRETORIO_ATUAL}/{nome_diretorio}/{nome_arquivo}")

        # Lendo metadados do arquivo
        exif = exif_parser(nome_diretorio, nome_arquivo)
        metadata = exif[0]
        gps_metadata = exif[1]
        if (len(metadata) == 0):
            continue

        # Apresentando largura e altura da imagem
        largura = ler_valor_tag(metadata, "ImageWidth")
        altura = ler_valor_tag(metadata, "ImageLength")
        if (largura != None and altura != None):
            print(f"Largura | Altura da imagem              : {largura} | {altura}")

        # Apresentando fabricante da câmera
        fabricante = ler_valor_tag(metadata, "Make")
        if (fabricante != None):
            print(f"Fabricante da câmera                    : {fabricante}")

        # Apresentando modelo da câmera
        modelo_camera = ler_valor_tag(metadata, "Model")
        if (modelo_camera != None):
            print(f"Modelo da câmera                        : {modelo_camera}")

        # Apresentando data e hora da captura
        data_hora = ler_valor_tag(metadata, "DateTime")
        if (data_hora != None):
            print(f"Data e hora da captura                  : {data_hora}")

        # Se há latitude e longitude, apresenta-se ambas e a cidade da
        # captura
        latitude_ref = ler_valor_tag(gps_metadata, "GPSLatitudeRef")
        latitude = ler_valor_tag(gps_metadata, "GPSLatitude")
        longitude_ref = ler_valor_tag(gps_metadata, "GPSLongitudeRef")
        longitude = ler_valor_tag(gps_metadata, "GPSLongitude")
        if (latitude_ref != None and latitude != None and longitude_ref != None and longitude != None):
            latitude_gps = converter_gps(latitude, latitude_ref)
            longitude_gps = converter_gps(longitude, longitude_ref)
            print(f"Latitude | Longitude do local da captura: {latitude_gps:.7f} | {longitude_gps:.7f}")

            obter_cidade(latitude_gps, longitude_gps)

    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

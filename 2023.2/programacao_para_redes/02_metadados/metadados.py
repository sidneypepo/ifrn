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
import funcoes

def main():
    # Obtendo diretório e lendo os arquivos presentes no mesmo
    nome_diretorio = funcoes.entrada_usuario("str", "Digite o nome do diretório que contém imagens JPG: ")
    arquivos = funcoes.ler_diretorio(nome_diretorio)
    if (len(arquivos) == 0):
        print("Erro: não há arquivos no diretório informado!")
        return

    # Obtendo e apresentando EXIFs selecionados em cada arquivo
    for nome_arquivo in arquivos:
        # Lendo metadados do arquivo
        exif = funcoes.exif_parser(nome_diretorio, nome_arquivo)
        metadata = exif[0]
        gps_metadata = exif[1]
        if (len(metadata) == 0):
            continue

        # Apresentando largura e altura da imagem
        largura = funcoes.ler_valor_tag(metadata, "ImageWidth")
        altura = funcoes.ler_valor_tag(metadata, "ImageLength")
        if (largura != None and altura != None):
            print(f"Largura | Altura da imagem              : {largura} | {altura}")

        # Apresentando fabricante da câmera
        fabricante = funcoes.ler_valor_tag(metadata, "Make")
        if (fabricante != None):
            print(f"Fabricante da câmera                    : {fabricante}")

        # Apresentando modelo da câmera
        modelo_camera = funcoes.ler_valor_tag(metadata, "Model")
        if (modelo_camera != None):
            print(f"Modelo da câmera                        : {modelo_camera}")

        # Apresentando data e hora da captura
        data_hora = funcoes.ler_valor_tag(metadata, "DateTime")
        if (data_hora != None):
            print(f"Data e hora da captura                  : {data_hora}")

        # Se há latitude e longitude, apresenta-se ambas e a cidade da
        # captura
        latitude_ref = funcoes.ler_valor_tag(gps_metadata, "GPSLatitudeRef")
        latitude = funcoes.ler_valor_tag(gps_metadata, "GPSLatitude")
        longitude_ref = funcoes.ler_valor_tag(gps_metadata, "GPSLongitudeRef")
        longitude = funcoes.ler_valor_tag(gps_metadata, "GPSLongitude")
        if (latitude_ref != None and latitude != None and longitude_ref != None and longitude != None):
            latitude_gps = funcoes.converter_gps(latitude, latitude_ref)
            longitude_gps = funcoes.converter_gps(longitude, longitude_ref)
            print(f"Latitude | Longitude do local da captura: {latitude_gps:.7f} | {longitude_gps:.7f}")

            funcoes.obter_cidade(latitude_gps, longitude_gps)

    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

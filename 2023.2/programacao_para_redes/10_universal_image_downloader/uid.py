#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/10_universal_image_downloader/uid.py
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
    # Obtendo endereço do arquivo do usuário
    endereco = funcoes.entrada_usuario("addr", "Digite o endereço completo da imagem (também pode ser um arquivo): ")

    # Separando protocolo, host e caminho do endereço do arquivo
    protocolo = endereco[0]
    host = endereco[1]
    caminho = endereco[2]
    nome_arquivo = caminho[caminho.rfind('/'):]

    # Se houver protocolo e se o protocolo informado não for HTTP,
    # exibe-se um erro
    if (protocolo != "http://" and protocolo != ''):
        funcoes.mostrar_erro(False, "Erro: protocolo não suportado/implementado!")
        return

    # Apresentando tentativa de baixar o arquivo e tentando obter
    # dados do arquivo. Se não houverem dados, exibe-se um erro
    print("\nBaixando arquivo...")
    arquivo = funcoes.obter_arquivo(host, 80, caminho)
    if (not len(arquivo) > 0):
        funcoes.mostrar_erro((len(arquivo) > 0), "Erro: não foi possível baixar o arquivo!")
        return

    print("Salvando arquivo...")
    funcoes.salvar_arquivo(arquivo, nome_arquivo)

    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/10_universal_http_downloader/uhd.py
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
    endereco = funcoes.entrada_usuario("addr", "Digite o endereço completo do arquivo: ")

    protocolo = endereco[0]
    host = endereco[1]
    caminho = endereco[2]
    nome_arquivo = caminho[caminho.rfind('/'):]

    if (protocolo == "http://" or protocolo == ''):
        print("\nBaixando arquivo...")
        arquivo = funcoes.obter_arquivo(host, 80, caminho)
        if (len(arquivo) > 0):
            print("Salvando arquivo...")
            funcoes.salvar_arquivo(arquivo, nome_arquivo)
        else:
            funcoes.mostrar_erro((len(arquivo) > 0), "Erro: não foi possível baixar o arquivo!")
    else:
        funcoes.mostrar_erro(False, "Erro: protocolo não suportado/implementado!")

    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

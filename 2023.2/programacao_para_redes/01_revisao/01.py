#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/01_revisao/01.py
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

import funcoes

def main():
    quantidade = funcoes.entrada_usuario("nat", "Digite a quantidade de números a serem gerados: ")
    valor_minimo = funcoes.entrada_usuario("nat", "Digite o menor valor numérico a ser gerado: ")
    valor_maximo = funcoes.entrada_usuario("nat", "Digite o maior valor numérico a ser gerado: ")

    lista = funcoes.gerar_lista(quantidade, valor_minimo, valor_maximo)
    if (lista[1] == None):
        print("Erro: não foi possível gerar a lista!")
        return

    nome_arquivo = funcoes.entrada_usuario("str", "Digite o nome do arquivo a ser salvo (com extensão): ")

    saida = funcoes.salvar_lista(lista[1], nome_arquivo)

    if (not saida):
        print("Erro: não foi possível salvar o arquivo!")
        return

    print("Arquivo salvo com sucesso!")

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

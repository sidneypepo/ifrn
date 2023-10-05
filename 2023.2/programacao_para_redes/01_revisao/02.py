#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/01_revisao/02.py
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
    nome_arquivo = funcoes.entrada_usuario("str", "Digite o nome do arquivo: ")

    lista = funcoes.ler_arquivo(nome_arquivo)
    if (lista[1] == None):
        funcoes.mostrar_erro(False, "Erro: não foi possível ler o arquivo!")
        return

    metodos_ordenacao = ("BUBBLE", "INSERTION", "SELECTION", "QUICK")
    metodo_ordena = ""
    while (not metodo_ordena.upper() in metodos_ordenacao):
        metodo_ordena = funcoes.entrada_usuario("str", "Digite o método de ordenação (bubble/insertion/selection/quick): ")
        funcoes.mostrar_erro((metodo_ordena.upper() in metodos_ordenacao), "Erro: método inválido!\n")

    lista_ordenada = funcoes.ordena_lista(lista[1], metodo_ordena)
    if (lista_ordenada[1] == None):
        funcoes.mostrar_erro(False, "Erro: não foi possível ordenar a lista!")
        return

    print("Lista ordenada com sucesso!\nResultado:", end=' ')
    for item in range(len(lista_ordenada[1])):
        print(lista_ordenada[1][item], end=' ')

    print()
    return

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

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

# Importando funções
import funcoes

def main():
    # Obtendo nome do arquivo e o lendo. Caso o retorno da lista seja
    # False e None, um erro é apresentado e o programa é finalizado
    lista = funcoes.ler_arquivo(funcoes.entrada_usuario("str", "Digite o nome do arquivo: "))
    if (lista[1] == None):
        funcoes.mostrar_erro(False, "Erro: não foi possível ler o arquivo!")
        return

    # Definindo possíveis métodos de ordenação da lista e obtendo
    # método do usuário. Caso o método não exista, um erro é
    # apresentado e o programa é finalizado
    metodos_ordenacao = ("BUBBLE", "INSERTION", "SELECTION", "QUICK")
    metodo_ordena = funcoes.entrada_usuario("str", "Digite o método de ordenação (bubble/insertion/selection/quick): ")
    if (not metodo_ordena.upper() in metodos_ordenacao):
        funcoes.mostrar_erro(False, "Erro: método inválido!")
        return

    # Ordenando lista com o método selecionado pelo usuário. Caso o
    # retorno da lista seja False e None, um erro é apresentado e o
    # programa é finalizado
    lista = funcoes.ordena_lista(lista[1], metodo_ordena)
    if (lista[1] == None):
        funcoes.mostrar_erro(False, "Erro: não foi possível ordenar a lista!")
        return

    # Apresentando lista ordenada e saindo do programa
    print("Lista ordenada com sucesso!\nResultado:", end=' ')
    for item in range(len(lista[1])):
        print(lista[1][item], end=' ')
    print()
    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

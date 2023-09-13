#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PC2023-1-ativ5-q3.py
#
# Aluno 1: Sidney Pedro
# Aluno 2: Iuri da Silva
#
# Última alteração: 2023-07-30
#

# Definindo função para dividir lista de números em sublistas
def lista_crescente(lista):
    # Tratando possíveis erros
    if (isinstance(lista, list) == False):
        print("Erro: o argumento passado não é uma lista!")
        return
    elif (len(lista) == 0):
        print("Erro: lista vazia!")
        return

    # Definindo lista de saída e variável para armazenar índice
    # das sublistas
    nova_lista = [[]]
    sublista = 0

    # Copiando itens da lista em sublistas
    for item in range(len(lista)):
        # Se a sublista atual possuir quantidade de itens igual
        # a seu índice, cria-se uma nova sublista e os próximos
        # números serão copiados para a nova sublista
        if (len(nova_lista[sublista]) == sublista + 1):
            nova_lista.append([])
            sublista += 1

        nova_lista[sublista].append(int(lista[item]))

    return nova_lista

# Exemplo para teste
# lista = [5, 6, 7, 23, 45, 43, 12, 1, 13, 90]
# print(lista_crescente(lista))

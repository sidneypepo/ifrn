#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PC2023-1-ativ5-q4.py
#
# Aluno 1: Sidney Pedro
# Aluno 2: Iuri da Silva
#
# Última alteração: 2023-07-30
#

# Definindo função para testar se todos os números de uma lista
# são ímpares ou pares
def lista_impar_par(lista):
    # Tratando possíveis erros
    if (isinstance(lista, list) == False):
        print("Erro: o argumento passado não é uma lista!\n")
        return
    elif (len(lista) == 0):
        print("Erro: lista vazia!\n")
        return

    # Definindo variável com resto da divisão do primeiro
    # número da lista por 2
    resto = int(lista[0]) % 2

    # Testando todos os números da lista
    for numero in lista:
        # Se o resto da divisão do número testado por 2 não for
        # igual ao resto armazenado anteriormente, a lista não
        # é toda ímpar ou toda par
        if (int(numero) % 2 != resto):
            return False

    return True

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

# Definindo lista, a dividindo em sublistas e definindo
# variável para armazenar se a lista de listas é piramidal
lista = [12, 3, 7, 2, 10, 4, 5, 13, 5, 11]
lista = lista_crescente(lista)
piramidal = True

# Navegando em cada sublista
for linha in range(len(lista)):
    # Testando sublista para saber se a mesma não é compatível
    # piramidalmente
    if (lista_impar_par(lista[linha]) == False or len(lista[linha]) != linha + 1):
        piramidal = False

    # Apresentando elementos da sublista
    for item in lista[linha]:
        print(item, end=' ')

    print()

# Apresentando se a lista de números é ou não piramidal
print("A sequência de números ", end='')
if (piramidal == False):
    print("não ", end='')
print("é piramidal.")

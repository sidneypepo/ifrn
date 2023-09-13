#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PC2023-1-ativ5-q2.py
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

# Exemplos para teste
# lista1 = [1,2,3]
# lista2 = [1,3,5]
# lista3 = [2,4,6]
# print(lista_impar_par(lista1))
# print(lista_impar_par(lista2))
# print(lista_impar_par(lista3))

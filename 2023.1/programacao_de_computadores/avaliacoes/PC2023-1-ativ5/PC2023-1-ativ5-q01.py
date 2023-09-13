#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PC2023-1-ativ5-q1.py
#
# Aluno 1: Sidney Pedro
# Aluno 2: Iuri da Silva
#
# Última alteração: 2023-07-30
#

# Definindo função para testar se um número é ou não primo
def e_primo(numero):
    # Testando 
    divisores = 0
    for tentativa in range(1, numero + 1):
        if (numero % tentativa == 0):
            divisores += 1

    # Se o número possuir só 2 divisores, é primo
    if (divisores == 2):
        return True
    else:
        return False

# Solicitando quantidade de números primos a serem encontrados
# e definindo variaveis para armazenar o numero testado e
# quantos primos foram encontrados
quantidade = int(input("Digite quantos números primos devem ser encontrados: "))
numero = 0
encontrados = 0

# Testando todos os números até obter a quantidade de primos
# solicitados pelo usuário
while (encontrados < quantidade):
    numero += 1
    # Se o numero testado for primo, apresenta-se o mesmo e é
    # contabilizado
    if (e_primo(numero) == True):
        encontrados += 1
        print(numero, end=' ')

print()

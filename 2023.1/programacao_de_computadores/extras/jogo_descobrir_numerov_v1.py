#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/jogo_descobrir_numero_v1.py
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

from random import randint

# Números limites
numero_minimo = 1
numero_maximo = 100
acertou = False

# Gerando número aleatório
numero_aleatorio = randint(numero_minimo, numero_maximo)

# Cabeçalho da "interface" do jogo
print("-> Jogo de descobrir o número v1.0 <-")
print(f"\nGerei um número aleatório entre {numero_minimo} e {numero_maximo}. Será que você consegue descobrir qual é?")

# Informando tentativas restantes, solicitando e adquirindo tentativa do jogador
print("Você tem 3 tentativas restantes")
tentativa = int(input("\nDigite sua primeira tentativa: "))

# Testando se o número foi acertado
if (tentativa == numero_aleatorio):
    print("\nVocê acertou de primeira! Parabéns :)")
    acertou = True
else:
    # Informando que o jogador errou e fornecendo ajuda
    print("Você errou! Tente novamente.")
    if (numero_aleatorio < tentativa):
        numero_maximo = tentativa
    else:
        numero_minimo = tentativa
    print(f"\nDica: O número aleatório está entre {numero_minimo} e {numero_maximo}.")

    # Informando tentativas restantes, solicitando e adquirindo tentativa do jogador
    print("Você tem 2 tentativas restantes")
    tentativa = int(input("\nDigite sua segunda tentativa: "))

# Testando se o número foi acertado na tentativa anterior
if (acertou == False and tentativa == numero_aleatorio):
    print("\nVocê acertou! Parabéns :)")
    acertou = True
else:
    # Informando que o jogador errou e fornecendo ajuda
    print("Você errou! Tente novamente.")
    if (numero_aleatorio < tentativa):
        numero_maximo = tentativa
    else:
        numero_minimo = tentativa
    print(f"\nDica: O número aleatório está entre {numero_minimo} e {numero_maximo}")

    # Informando tentativas restantes, solicitando e adquirindo tentativa do jogador
    print("Você tem 1 tentativa restantes")
    tentativa = int(input("\nDigite sua terceira (e última) tentativa: "))

# Testando se o número foi acertado na tentativa anterior
if (acertou == False and tentativa == numero_aleatorio):
    print("\nVocê acertou! Parabéns :)")
else:
    # Informando que o jogador errou e informando fim de jogo
    print(f"O número aleatório era {numero_aleatorio}, mas infelizmente você não acertou nenhuma vez. Jogue novamente")

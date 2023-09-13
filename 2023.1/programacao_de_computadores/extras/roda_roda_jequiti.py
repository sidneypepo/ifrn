#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/roda_roda_jequiti.py
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

palavras = ("abacaxi", "abacate", "laranja", "pera", "tangerina", "banana")
palavra_oculta = palavras[randint(0, len(palavras) - 1)]
visivel = "_" * len(palavra_oculta)

print("-> Roda Roda Jequiti v1.0 <-")
print("Escolhi uma palavra aleatória. Será que você consegue descobrir?")

tentativa = 0
while (visivel != palavra_oculta):
    print(f"\nPalavra oculta -> {visivel}")
    letra = input("Digite sua tentativa: ")
    for posicao in range(len(palavra_oculta)):
        if (visivel[posicao] == "_"):
            if (letra == palavra_oculta[posicao]):
                visivel = visivel[0:posicao] + letra + visivel[posicao + 1:]
    tentativa += 1

print(f"\nParabéns! A palavra oculta era \"{visivel}\" e você acertou em sua {tentativa}ª tentativa.")

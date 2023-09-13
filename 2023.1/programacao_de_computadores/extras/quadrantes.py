#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/quadrantes.py
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

x = int(input("Digite a posição de X: "))
y = int(input("Digite a posição de Y: "))

if (x == 0 and y == 0):
    print("\nA posição é o ponto de origem (0, 0).")
elif (y == 0):
    print("\nA posição está em cima do eixo X.")
elif (x == 0):
    print("\nA posição está em cima do eixo Y.")
elif (x > 0):
    if (y > 0):
        print("\nA posição está no 1º quadrante.")
    else:
        print("\nA posição está no 4º quadrante.")
else:
    if (y > 0):
        print("\nA posição está no 2º quadrante.")
    else:
        print("\nA posição está no 3º quadrante.")

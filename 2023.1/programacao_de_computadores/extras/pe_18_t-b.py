#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/pe_18_t-b.py
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

piramide = [[75],
            [95, 64],
            [17, 47, 82],
            [18, 35, 87, 10],
            [20, 4, 82, 47, 65],
            [19, 1, 23, 75, 3, 34],
            [88, 2, 77, 73, 7, 63, 67],
            [99, 65, 4, 28, 6, 16, 70, 92],
            [41, 41, 26, 56, 83, 40, 80, 70, 33],
            [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
            [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
            [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
            [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
            [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
            [4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]]

maior_soma = 0

for linha in range(1, len(piramide)):
    for coluna in range(len(piramide[linha])):
        if (coluna == 0):
            piramide[linha][coluna] += piramide[linha - 1][coluna]
        elif (linha == 1 and coluna == len(piramide[linha]) - 1):
            piramide[linha][coluna] += piramide[linha - 1][coluna - 1]
        elif (coluna == len(piramide[linha]) - 1):
            piramide[linha][coluna] += piramide[linha - 1][coluna - 1]
        elif (piramide[linha - 1][coluna] > piramide[linha - 1][coluna - 1]):
            piramide[linha][coluna] += piramide[linha - 1][coluna]
        else:
            piramide[linha][coluna] += piramide[linha - 1][coluna - 1]

        if (linha == len(piramide) - 1 and piramide[linha][coluna] > maior_soma):
            maior_soma = piramide[linha][coluna]

print(f"{maior_soma}")

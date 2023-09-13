#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/triangulo.py
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

triangulo = []
colunas = 1

for linha in range(100):
    triangulo.append([])
    for coluna in range(colunas):
        if (coluna == 0 or coluna == colunas - 1):
            triangulo[linha].append(1)
        else:
            triangulo[linha].append(triangulo[linha - 1][coluna - 1] + triangulo[linha - 1][coluna])
        print(f"{triangulo[linha][coluna]:02d}", end=' ')
    colunas += 1
    print()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/fatorial.py
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

numero = int(input("Digite um número: "))
temp = numero
fatorial = 1

while (temp > 0):
    fatorial *= temp
    temp -= 1

print(numero, fatorial)

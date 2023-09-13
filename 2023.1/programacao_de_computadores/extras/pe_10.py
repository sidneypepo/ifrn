#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/pe_10.py
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

soma = 0
numero = 1

while (numero < 1000):
    divisor_numero = 0
    numero_testado = 1
    while (numero_testado <= numero):
        if (numero % numero_testado == 0):
            divisor_numero += 1
        numero_testado += 1
    if (divisor_numero == 2):
        soma += numero
    numero += 1
print(f"{soma}")

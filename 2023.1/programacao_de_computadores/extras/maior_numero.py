#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/maior_numero.py
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

numero_1 = float(input("Digite o primeiro número: "))
numero_2 = float(input("Digite o segundo número: "))
numero_3 = float(input("Digite o terceiro número: "))

if (numero_1 > numero_2 and numero_1 > numero_3):
    maior_numero = "primeiro"
    maior_valor = numero_1
elif (numero_2 > numero_1 and numero_2 > numero_3):
    maior_numero = "segundo"
    maior_valor = numero_2
else:
    maior_numero = "terceiro"
    maior_valor = numero_3

print(f"\nO maior número digitado é o {maior_numero} ({maior_valor:.2f})")

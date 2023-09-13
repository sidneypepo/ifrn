#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/maior_trio.py
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

# 567912345681347582
numero = int(input("Digite um número: "))

temp = numero
potencia_dez = 1
while (temp >= 10):
    temp //= 10
    potencia_dez += 1

maior = 0
contagem = 0
while (contagem <= potencia_dez - 2):
    grupo = numero % (10 ** (3 + contagem))
    grupo //= 10 ** contagem
    if (grupo > maior):
        maior = grupo
    contagem += 1

print(f"O maior trio do número {numero} é {maior}.")

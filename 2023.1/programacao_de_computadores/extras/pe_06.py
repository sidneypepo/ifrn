#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/pe_06.py
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

soma_quadrados = 0
quadrado_somas = 0

numero = 1
while (numero <= 100):
    soma_quadrados = soma_quadrados + (numero ** 2)
    numero += 1

numero = 1
while (numero <= 100):
    quadrado_somas = soma_quadrados + numero
    numero += 1
quadrado_somas = quadrado_somas ** 2

print(f"A diferença entre a soma dos quadrados até 100 ({soma_quadrados}) e o quadrado das somas até 100 ({quadrado_somas}) é {quadrado_somas - soma_quadrados}.")

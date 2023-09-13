#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/circunferencia.py
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

from math import pi, sin, cos
from matplotlib import pyplot as plot
from random import randint

plot.axis((-150, 150, -150, 150))

raio = 100

precisao = 5

for angulo in range(360 * precisao):
    # print(f"({raio * cos(angulo * (pi / 180)):03.2f}, {raio * sin(angulo * (pi / 180)):03.2f})")
    rand = randint(1, 6)
    if (rand == 1):
        string = "#f00"
    elif (rand == 2):
        string = "#ff0"
    elif (rand == 3):
        string = "#0f0"
    elif (rand == 4):
        string = "#0ff"
    elif (rand == 5):
        string = "#00f"
    else:
        string = "#f0f"
    plot.plot(raio * cos((angulo / precisao) * (pi / 180)), raio * sin((angulo / precisao) * (pi / 180)), ".", color=string)

plot.show()

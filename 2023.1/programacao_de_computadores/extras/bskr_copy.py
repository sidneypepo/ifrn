#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/bskr_copy.py
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

from sys import argv
from math import sqrt

def main(a, b, c):
    delta = (b ** 2) - (4 * a * c)
    x1 = (-b + (sqrt(delta))) / (2 * a)
    x2 = (-b - (sqrt(delta))) / (2 * a)

    print(f"\nx1 = {x1:.2f}\nx2 = {x2:.2f}")

if (__name__ == "__main__"):
    main(int(argv[1]), int(argv[2]), int(argv[3]))

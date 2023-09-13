#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/listas-exercicios-fixacao/exemplo_01.py
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

str_uf        = 'Alagoas;Bahia;Ceará;Maranhão;Paraíba;Pernambuco;Piauí;Rio Grande do Norte;Sergipe'
str_siglas    = 'AL;BA;CE;MA;PB;PE;PI;RN;SE'
str_populacao = '3365351;14985284;9240580;7153262;4059905;9674793;3289290;3560903;2338474'

# Preencher as listas a partir das respectivas strings
# lst_uf        <- str_uf
# lst_siglas    <- str_siglas
# lst_populacao <- str_populacao (lembrar de converter para int)

lst_uf = str_uf.split(';')
lst_siglas = str_siglas.split(';')
lst_populacao = str_populacao.split(';')
for item in range(len(lst_populacao)):
    lst_populacao[item] = int(lst_populacao[item])

print(lst_uf)
print(lst_siglas)
print(lst_populacao)

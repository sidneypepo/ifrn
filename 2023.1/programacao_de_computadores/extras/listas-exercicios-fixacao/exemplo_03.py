#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/listas-exercicios-fixacao/exemplo_03.py
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

lst_uf        = ['Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe']
lst_siglas    = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
lst_populacao = [3365351, 14985284, 9240580, 7153262, 4059905, 9674793, 3289290, 3560903, 2338474]

# Imprimir na tela os dados obedecendo o seguinte layout:
# 'O estado NOME_ESTADO (SIGLA) possui (QUANTIDADE) habitantes'

# E no final imprimir a seguinte informação:
# 'O Nordeste possui um total de (QUANTIDADE TOTAL) habitantes'

quantidade_total = 0

for estado in range(len(lst_uf)):
    print(f"O estado {lst_uf[estado]} {lst_siglas[estado]} possui {lst_populacao[estado]} habitantes")
    quantidade_total += lst_populacao[estado]

print(f"\nO Nordeste possui um total de {quantidade_total} habitantes")

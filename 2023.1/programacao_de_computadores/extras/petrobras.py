#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/petrobras.py
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

arquivo = open("D:/code/py_code/PETR4.SA.csv", "r")

menor_acao = 1000000000
fechamentos = 0
volumes = 0
maior_valor = 0
linhas = 0

for linha in arquivo:
    linhas += 1
    if (linhas == 1):
        continue
    linha = linha.split(',')

    # menor acao
    if (float(linha[3]) < menor_acao):
        menor_acao = float(linha[3])

    # maior acao
    if (float(linha[2]) > maior_valor):
        maior_valor = float(linha[2])
        maior_dia = linha[0]

    # somando fechamentos
    fechamentos += float(linha[4])

    # somando volumes
    if (linha[6][-1] == '\n'):
        volumes += int(linha[6][0:-1])
    else:
        volumes += int(linha[6])

arquivo.close()

media_fechamentos = fechamentos / linhas
media_volumes = volumes / linhas

print(f"Menor valor da ação: {menor_acao}")
print(f"Preço médio de fechamento: {media_fechamentos}")
print(f"Volume médio negociado: {media_volumes}")
print(f"Dia com maior valor: {maior_dia}")

saida = open("resultados.txt", "w")
saida.write(f"Menor valor da ação: {menor_acao}\n")
saida.write(f"Preço médio de fechamento: {media_fechamentos}\n")
saida.write(f"Volume médio negociado: {media_volumes}\n")
saida.write(f"Dia com maior valor: {maior_dia}\n")
saida.close()

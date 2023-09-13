#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.1/programacao_de_computadores/extras/contas_v2.py
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

conta = float(input("Qual o valor da conta a pagar? R$"))

pagamento = int(input(f"Com quanto dinheiro você quer pagar a conta de R${conta:.2f}? R$"))

troco = pagamento - conta

print(f"\n* Então teu troco é R${troco:.2f} e uma maneira de pagar seu troco, é com:")

notas = troco // 200
print(f"- {notas} notas de R$200")
troco = troco % 200

notas = troco // 100
print(f"- {notas} notas de R$100")
troco = troco % 100

notas = troco // 50
print(f"- {notas} notas de R$50")
troco = troco % 50

notas = troco // 20
print(f"- {notas} notas de R$20")
troco = troco % 20

notas = troco // 10
print(f"- {notas} notas de R$10")
troco = troco % 10

notas = troco // 5
print(f"- {notas} notas de R$5")
troco = troco % 5

notas = troco // 2
print(f"- {notas} notas de R$2")
troco = troco % 2

notas = troco // 1
print(f"- {notas} moedas de R$1")
troco = troco % 1

notas = troco // 0.5
print(f"- {notas} moedas de R$0.50")
troco = troco % 0.5

notas = troco // 0.25
print(f"- {notas} moedas de R$0.25")
troco = troco % 0.25

notas = troco // 0.1
print(f"- {notas} moedas de R$0.10")
troco = troco % 0.1

notas = troco // 0.05
print(f"- {notas} moedas de R$0.05")

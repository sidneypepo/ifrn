#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/06_netscan/netscan.py
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

# Importando funções
import funcoes

def main():
    portas = funcoes.ler_arquivo("portas.csv", False)
    if (not portas[0]):
        funcoes.mostrar_erro(False, "Erro: não foi possível abrir o arquivo de informações!")
        return

    ip = funcoes.entrada_usuario("ip", "Digite o nome do host a ser escaneado (domínio ou IP): ")
    print()
    for index in range(1, len(portas[1])):
        funcoes.testar_porta(ip, portas[1][index][:-1])

    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

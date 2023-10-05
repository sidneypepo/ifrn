#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/01_revisao/04.py
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

import funcoes

def main():
    conteudo = funcoes.ler_json_cartola()
    if (conteudo == None):
        funcoes.mostrar_erro(False, "Erro: não foi possível abrir o arquivo!")
        return

    funcoes.menu_esquemas_cartola()
    esquema = funcoes.entrada_usuario("nat", "Escolha o esquema tático (1-7): ")
    if (esquema < 1 or esquema > 7):
        funcoes.mostrar_erro(False, "Erro: esquema tático inválido!")
        return

    clubes = funcoes.organizar_cartola(conteudo[1])
    funcoes.salvar_cartola(conteudo[0], clubes, esquema, conteudo[1]["posicoes"])
    return

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

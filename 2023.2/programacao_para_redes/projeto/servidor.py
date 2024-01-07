#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/servidor.py
# Copyright (C) 2023-2024  Sidney Pedro
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

# Importando bibliotecas
import funcoes_servidor, constantes, funcoes, os

def main():
    # Verificando se há outra instância de servidor em execução
    try:
        arquivo_trava = open(f"{constantes.DIRETORIO_ATUAL}/servidor.pid", 'r')
        arquivo_trava.close()
        print("Erro: outra instância do servidor já está em execução!")
        return
    except:
        arquivo_trava = open(f"{constantes.DIRETORIO_ATUAL}/servidor.pid", 'w')
        arquivo_trava.write(f"{os.getpid()}\n")
        arquivo_trava.close()

    try:
        funcoes_servidor.servidor()
    except:
        print("\nSaindo...")

    # Removendo trava de execução
    funcoes.remover_arquivo("servidor.pid")
    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

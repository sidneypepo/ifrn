#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/01_revisao/01.py
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
    # Obtendo quantidade de números aleatórios e seus valores máximos
    # e mínimos
    quantidade = funcoes.entrada_usuario("nat", "Digite a quantidade de números a serem gerados: ")
    valor_minimo = funcoes.entrada_usuario("nat", "Digite o menor valor numérico a ser gerado: ")
    valor_maximo = funcoes.entrada_usuario("nat", "Digite o maior valor numérico a ser gerado: ")

    # Gerando e armazenando lista a partir dos valores obtidos
    # anteriormente e, se o retorno for False e None, um erro é
    # apresentado e o programa é finalizado
    lista = funcoes.gerar_lista(quantidade, valor_minimo, valor_maximo)
    if (lista[1] == None):
        funcoes.mostrar_erro(False, "Erro: não foi possível gerar a lista!")
        return

    # Obtendo nome do arquivo para salvar a lista
    nome_arquivo = funcoes.entrada_usuario("str", "Digite o nome do arquivo a ser salvo (com extensão): ")

    # Salvando lista em um arquivo com o nome informado anteriormente
    # e, se o retorno for False, um erro é apresentado e o programa é
    # finalizado
    saida = funcoes.salvar_lista(lista[1], nome_arquivo)
    if (not saida):
        funcoes.mostrar_erro(False, "Erro: não foi possível salvar o arquivo!")
        return

    # Informando sucesso e saindo do programa
    print("Arquivo salvo com sucesso!")
    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

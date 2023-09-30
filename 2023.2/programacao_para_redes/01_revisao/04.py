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
    funcoes.criar_diretorio("dados_estatisticos")
    arquivos = funcoes.ler_diretorio("serie_historica_anp")
    print("Lendo e gerando arquivos...")

    conteudos = ["Regiao – Sigla;Estado – Sigla;Produto;Data da Coleta;Valor de Venda;Bandeira"]
    media_bandeira = {}
    media_produto_regiao = {}
    for arquivo in arquivos:
        conteudo = funcoes.ler_arquivo("serie_historica_anp/" + arquivo, False, "latin-1")
        if (not conteudo[0]):
            print(f"Aviso: Não foi possível ler o arquivo {arquivo}")
            continue
        conteudo[1].pop(0)

        for index in range(len(conteudo[1])):
            conteudo[1][index] = funcoes.dividir_linha(conteudo[1][index][:-1])
            conteudos.append(f"{conteudo[1][index][0]};{conteudo[1][index][1]};{conteudo[1][index][10]};{conteudo[1][index][11]};{conteudo[1][index][12]};{conteudo[1][index][15]}")

            chave = f"{conteudo[1][index][15]};{conteudo[1][index][10]};{conteudo[1][index][11][-4:]};"
            if (not chave in media_bandeira):
                media_bandeira[chave] = [0, 0]
            media_bandeira[chave][0] += float(conteudo[1][index][12].replace(',', '.'))
            media_bandeira[chave][1] += 1

            chave = f"{conteudo[1][index][10]};{conteudo[1][index][0]};{conteudo[1][index][11][-4:]};"
            if (not chave in media_produto_regiao):
                media_produto_regiao[chave] = [0, 0]
            media_produto_regiao[chave][0] += float(conteudo[1][index][12].replace(',', '.'))
            media_produto_regiao[chave][1] += 1

    saida = funcoes.salvar_lista(conteudos, "dados_estatisticos/serie_historica_anp.txt")
    if (not saida):
        print("Erro: não foi possível salvar o arquivo serie_historica_anp.txt!")
        return

    conteudos = ["bandeira;produto;ano;valor_medio_venda;quantidade_postos"]
    for chave in media_bandeira:
        media_bandeira[chave][0] /= media_bandeira[chave][1]
        conteudos.append(f"{chave}{media_bandeira[chave][0]:.3f};{media_bandeira[chave][1]}")
    saida = funcoes.salvar_lista(conteudos, "dados_estatisticos/media_bandeira.txt")
    if (not saida):
        print("Erro: não foi possível salvar o arquivo media_bandeira.txt!")
        return

    conteudos = ["produto;região;ano;valor_medio;quantidade_postos"]
    for chave in media_produto_regiao:
        media_produto_regiao[chave][0] /= media_produto_regiao[chave][1]
        conteudos.append(f"{chave}{media_produto_regiao[chave][0]:.3f};{media_produto_regiao[chave][1]}")
    saida = funcoes.salvar_lista(conteudos, "dados_estatisticos/media_produto_regiao.txt")
    if (not saida):
        print("Erro: não foi possível salvar o arquivo media_produto_regiao.txt!")
        return

    print("Arquivos gerados com sucesso!")
    return

if (__name__ == "__main__"):
    # try:
    main()
    # except:
        # print("\nSaindo...")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/01_revisao/03.py
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
    # Criando diretório de saída e lendo conteúdo do diretório de entrada
    funcoes.criar_diretorio("dados_estatisticos")
    arquivos = funcoes.ler_diretorio("serie_historica_anp")

    # Inicializando dicionários de médias e lista da série histórica e
    # navegando na lista de arquivos presentes no diretório de entrada
    print("Lendo e gerando arquivos...")
    media_bandeira = {}
    media_produto_regiao = {}
    conteudos = ["Regiao – Sigla;Estado – Sigla;Produto;Data da Coleta;Valor de Venda;Bandeira"]
    for arquivo in arquivos:
        # Lendo conteúdo do atual arquivo e removendo primeira linha
        conteudo = funcoes.ler_arquivo("serie_historica_anp/" + arquivo, False, "latin-1")
        if (not conteudo[0]):
            print(f"Aviso: Não foi possível ler o arquivo {arquivo}")
            continue
        conteudo[1].pop(0)

        # Navegando em cada linha do arquivo lido
        conteudo = conteudo[1]
        for index in range(len(conteudo)):
            # Dividindo linha, formatando dados e adicionando linha na lista
            # da série histórica
            conteudo[index] = funcoes.dividir_string(conteudo[index][:-1])
            conteudos.append(f"{conteudo[index][0]};{conteudo[index][1]};{conteudo[index][10]};{conteudo[index][11]};{conteudo[index][12]};{conteudo[index][15]}")

            # Obtendo chave para o dicionário "media_bandeira" e, se não
            # existir, inicializa-se, então soma-se o valor da venda ao valor
            # já existente e soma-se um à quantidade de postos
            chave = f"{conteudo[index][15]};{conteudo[index][10]};{conteudo[index][11][-4:]};"
            if (not chave in media_bandeira):
                media_bandeira[chave] = [0, 0]
            media_bandeira[chave][0] += float(conteudo[index][12].replace(',', '.'))
            media_bandeira[chave][1] += 1

            # Obtendo chave para o dicionário "media_produto_regiao" e, se não
            # existir, inicializa-se, então soma-se o valor da venda ao valor
            # já existente e soma-se um à quantidade de postos
            chave = f"{conteudo[index][10]};{conteudo[index][0]};{conteudo[index][11][-4:]};"
            if (not chave in media_produto_regiao):
                media_produto_regiao[chave] = [0, 0]
            media_produto_regiao[chave][0] += float(conteudo[index][12].replace(',', '.'))
            media_produto_regiao[chave][1] += 1

    # Salvando arquivo da série história. Caso o retorno do salvamento
    # seja False, um erro é apresentado e o programa é finalizado
    saida = funcoes.salvar_lista(conteudos, "dados_estatisticos/serie_historica_anp.txt")
    if (not saida):
        funcoes.mostrar_erro(False, "Erro: não foi possível salvar o arquivo serie_historica_anp.txt!")
        return

    # Inicializando lista da "media_bandeira", fazendo a média do
    # valor da venda, formatando dados e adicionando linha na lista da
    # "media_bandeira" e salvando arquivo da "media_bandeira". Caso o
    # retorno do salvamento seja False, um erro é apresentado e o
    # programa é finalizado
    conteudos = ["bandeira;produto;ano;valor_medio_venda;quantidade_postos"]
    for chave in media_bandeira:
        media_bandeira[chave][0] /= media_bandeira[chave][1]
        conteudos.append(f"{chave}{media_bandeira[chave][0]:.3f};{media_bandeira[chave][1]}")
    saida = funcoes.salvar_lista(conteudos, "dados_estatisticos/media_bandeira.txt")
    if (not saida):
        funcoes.mostrar_erro(False, "Erro: não foi possível salvar o arquivo media_bandeira.txt!")
        return

    # Inicializando lista da "media_produto_regiao", fazendo a média
    # do valor da venda, formatando dados e adicionando linha na lista
    # da "media_produto_regiao" e salvando arquivo da
    # "media_produto_regiao". Caso o retorno do salvamento seja False,
    # um erro é apresentado e o programa é finalizado
    conteudos = ["produto;região;ano;valor_medio;quantidade_postos"]
    for chave in media_produto_regiao:
        media_produto_regiao[chave][0] /= media_produto_regiao[chave][1]
        conteudos.append(f"{chave}{media_produto_regiao[chave][0]:.3f};{media_produto_regiao[chave][1]}")
    saida = funcoes.salvar_lista(conteudos, "dados_estatisticos/media_produto_regiao.txt")
    if (not saida):
        funcoes.mostrar_erro(False, "Erro: não foi possível salvar o arquivo media_produto_regiao.txt!")
        return

    # Informando sucesso na geração dos arquivos e finalizando
    # programa
    print("Arquivos gerados com sucesso!")
    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/11_bot_telegram/bot_telegram.py
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
import requisicoes

def main():
    print("Para acessar o bot, pesquise @progredes_dummy_bot ou clique no link direto: https://t.me/progredes_dummy_bot")
    print("Para encerrar o bot, pressione Ctrl-C\n")

    # Loop de funcionamento do bot
    continuar = True
    latest_update_id = 0
    while (continuar):
        # Obtendo última atualização e mensagem e, em caso de exceção,
        # tenta-se novamente
        try:
            latest_update_id, latest_message = requisicoes.obter_atualizacoes(latest_update_id)
        except KeyboardInterrupt:
            continuar = False
            continue
        except:
            continue

        # Se não houver novas mensagens, volta-se ao início
        if (latest_message == None):
            continue

        # Interpretando mensagem e salvando última atalização
        try:
            requisicoes.interpretar_mensagem(latest_message)
            requisicoes.salvar_update_id(latest_update_id)
        except:
            continuar = False
            continue

    print()
    return

# Entrando na função main e, em caso de exceção, saindo
if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

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

import requests

API_KEY = "6308631803:AAEArbA5TdVhJRtv1xofzjgkWIfpCp-KWMk" # @progredes_dummy_bot
TELEGRAM_API = f"https://api.telegram.org/bot{API_KEY}"

def main():
    latest_date = 0

    while (True):
        try:
            updates = requests.get(TELEGRAM_API + "/getUpdates")
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            continue

        retorno = updates.json()
        if (updates.status_code == 409):
            print("Error: another connection is being established! Trying again...")
            continue
        elif (updates.status_code != 200):
            return
        elif (len(retorno["result"]) == 0):
            continue

        try:
            arquivo = open("timestamp.txt", "r")
        except:
            arquivo = open("timestamp.txt", "w")
            arquivo.write(f"{latest_date}\n")
            arquivo.close()

            arquivo = open("timestamp.txt", "r")

        latest_date = int(arquivo.readline())
        arquivo.close()

        latest_message = retorno["result"][-1]
        message_date = latest_message["message"]["date"]

        if (not message_date > latest_date):
            continue
        else:
            latest_date = message_date

        print(f"{latest_message}")

        chat_id = latest_message["message"]["chat"]["id"]
        message_id = latest_message["message"]["message_id"]

        if (latest_message["message"]["text"] == "/start"):
            message = "Comando recebido"
        else:
            message = "Bom dia 🌞"

        dados = {"chat_id": chat_id, "reply_to_message_id": message_id, "text": message}
        post = requests.post(TELEGRAM_API + "/sendMessage", data=dados)

        arquivo = open("timestamp.txt", "w")
        arquivo.write(f"{latest_date}\n")
        arquivo.close()

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

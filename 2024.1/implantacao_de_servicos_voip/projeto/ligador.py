#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2024.1/implementacao_de_servicos_de_voip/projeto/ligador.py
# Copyright (C) 2024  Sidney Pedro
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

from constantes import *
from funcoes import *
from asterisk.manager import Manager
import time, threading

AMI = Manager()

# doc:
# {
#  ramal: {
#   timestamp (com timezone incluida): tentativas
#  }
# }

# feito
def ligar(ramal: str, timestamp: str, tentativas: int):
    try:
        timestamp_int = int(timestamp)
        timestamp_agora = int(time.time())
    except:
        return

    if ((timestamp_int > timestamp_agora) or (timestamp_int <= timestamp_agora and tentativas > 2)):
        return

    ligacao = {
        "Action": "Originate",
        "Channel": f"SIP/{ramal}",
        "CallerID": f"Lembrete de compromisso",
        "Application": "AGI",
        "Data": f"{DIRETORIO_ATUAL}/ramal.py,{ramal},{timestamp}"
    }

    if (str(AMI.send_action(ligacao)) == "Success"):
        editar_compromisso(ramal, timestamp, NEUTRO, 3)
    else:
        editar_compromisso(ramal, timestamp, NEUTRO, tentativas + 1)
    return

# feito
def verificar_agenda(agenda: dict):
    if (len(agenda.keys()) < 1):
        return

    for ramal in agenda:
        for timestamp in agenda[ramal]:
            threading.Thread(target=ligar, args=(ramal, timestamp, agenda[ramal][timestamp])).start()

    return

# feito
def main():
    try:
        AMI.connect(IP, PORTA)
        AMI.login(USUARIO, SENHA)
    except:
        print("Erro: usuário e/ou senha inválidos!")
        return

    while (True):
        try:
            threading.Thread(target=verificar_agenda, args=(ler_agenda(),)).start()
            time.sleep(60)
        except KeyboardInterrupt:
            print("\nParando programa... (aguarde enquanto as threads remanescentes são finalizadas)")
            break
        except:
            continue

    AMI.close()
    return

if (__name__ == "__main__"):
    main()

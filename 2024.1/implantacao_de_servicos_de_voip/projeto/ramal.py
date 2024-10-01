#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2024.1/implementacao_de_servicos_de_voip/projeto/ramal.py
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
from asterisk.agi import AGI as Gateway
import time, sys

AGI = Gateway()

# feito
def tocar_compromisso(ramal: str, timestamp: str):
    retorno = False
    tentativa = NEUTRO
    tocar = True
    while (tentativa < INATIVO):
        if (tocar):
            valor = tocar_audio(f"{DIRETORIO_ATUAL}/compromissos/{ramal}_{timestamp}", AGI)
            tocar = False
        if (valor == DESLIGAR):
            tentativa = DESLIGAR
            retorno = retorno, tentativa
            continue

        valor = AGI.get_data(REESCUTAR, 5000, 1)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            retorno = retorno, tentativa
            AGI.stream_file(INATIVIDADE)
            continue

        if (valor == ''):
            AGI.stream_file(VOU_REPETIR)
        elif (valor == '*'):
            tentativa = DESLIGAR
            retorno = True, VOLTAR
        elif (valor == '0'):
            tentativa = DESLIGAR
            retorno = retorno, tentativa
        elif (valor == '1'):
            tocar = True
        elif (valor == '2'):
            retorno, tentativa = editar_compromisso(ramal, timestamp, APAGAR, agi = AGI)
            retorno = retorno, tentativa
        else:
            tentativa = NEUTRO
            AGI.stream_file(DADO_INVALIDO)

    return retorno

# feito
def compromisso_selecionado(ramal: str, timestamp: str):
    retorno = False
    tentativa = NEUTRO
    while (tentativa < INATIVO):
        valor = AGI.get_data(COMPROMISSO_SELECIONADO, 5000, 1)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            retorno = retorno, tentativa
            AGI.stream_file(INATIVIDADE)
            continue

        if (valor == ''):
            AGI.stream_file(VOU_REPETIR)
        elif (valor == '*'):
            tentativa = DESLIGAR
            retorno = True, VOLTAR
        elif (valor == '0'):
            tentativa = DESLIGAR
            retorno = retorno, tentativa
        elif (valor == '1'):
            retorno, tentativa = tocar_compromisso(ramal, timestamp)
            retorno = retorno, tentativa
        elif (valor == '2'):
            retorno, tentativa = editar_compromisso(ramal, timestamp, agi = AGI)
            retorno = retorno, tentativa
        elif (valor == '3'):
            retorno, tentativa = editar_compromisso(ramal, timestamp, APAGAR, agi = AGI)
            retorno = retorno, tentativa
        else:
            tentativa = NEUTRO
            AGI.stream_file(DADO_INVALIDO)

    return retorno

# feito
def listar_compromissos(ramal: str):
    retorno = False
    tentativa = NEUTRO

    try:
        if (len(ler_agenda()[ramal]) < 1):
            raise
    except:
        retorno = True, tentativa
        AGI.stream_file(SEM_COMPROMISSOS)
        return retorno

    while (tentativa < INATIVO):
        compromissos = tuple(ler_agenda()[ramal].keys())
        valor = falar_compromissos(compromissos, AGI)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            retorno = retorno, tentativa
            AGI.stream_file(INATIVIDADE)
            continue

        if (valor == ''):
            AGI.stream_file(VOU_REPETIR)
        elif (valor == '*'):
            tentativa = DESLIGAR
            retorno = True, VOLTAR
        elif (valor == '0'):
            tentativa = DESLIGAR
            retorno = retorno, tentativa
        elif (int(valor) <= len(compromissos)):
            retorno, tentativa = compromisso_selecionado(ramal, compromissos[int(valor) - 1])
        else:
            tentativa = NEUTRO
            AGI.stream_file(DADO_INVALIDO)

    return retorno

# feito
def marcar_compromisso(ramal: str):
    retorno = preparar_data(ramal, AGI)
    if (isinstance(retorno[0], bool)):
        return retorno

    timestamp = retorno[0]
    retorno, salvar = preparar_audio(ramal, timestamp, AGI)
    if (retorno == salvar and not salvar[0]):
        return retorno
    elif (salvar[0]):
        agenda = ler_agenda()
        agenda[ramal][timestamp] = 0
        salvar_agenda(agenda)

        AGI.stream_file(MARCADO)

    return retorno

# feito
def main():
    continuar = True

    AGI.answer()
    ramal = AGI.get_variable("CHANNEL").split('/')[1].split('-')[0]

    if (len(sys.argv) == 3):
        ramal = sys.argv[1]
        continuar = tocar_compromisso(sys.argv[1], sys.argv[2])[0]
    else:
        AGI.stream_file(BOAS_VINDAS)

    tentativa = NEUTRO
    while (continuar and tentativa < INATIVO):
        valor = AGI.get_data(MENU_INICIAL, 5000, 1)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            continuar = False
            AGI.stream_file(INATIVIDADE)
            continue

        if (valor == ''):
            AGI.stream_file(VOU_REPETIR)
        elif (valor == '0'):
            continuar = False
        elif (valor == '1'):
            continuar, tentativa = listar_compromissos(ramal)
        elif (valor == '2'):
            continuar, tentativa = marcar_compromisso(ramal)
        else:
            tentativa = NEUTRO
            AGI.stream_file(DADO_INVALIDO)

    AGI.stream_file(ATE_MAIS)
    AGI.hangup()
    return

if (__name__ == "__main__"):
    main()

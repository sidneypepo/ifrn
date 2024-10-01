#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2024.1/implementacao_de_servicos_de_voip/projeto/funcoes.py
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
import json, os, time

# feito
def operar_arquivo(caminho: str, modo: str = 'r', dados = None, charset = "utf-8"):
    retorno = None
    arquivo = open(caminho, modo, encoding = charset)

    if (modo == 'r'):
        retorno = json.load(arquivo)
    elif (modo == "rb"):
        retorno = arquivo.read()
    elif (modo == 'w'):
        json.dump(dados, arquivo, indent = 4)
    elif (modo == "wb"):
        arquivo.write(dados)

    arquivo.close()
    return retorno

# feito
def salvar_agenda(agenda: dict):
    backup_agenda = agenda

    try:
        if (os.path.isfile(f"{DIRETORIO_ATUAL}/agenda.json")):
            backup_agenda = operar_arquivo(f"{DIRETORIO_ATUAL}/agenda.json", "rb", None, None)
            operar_arquivo(f"{DIRETORIO_ATUAL}/agenda.json.bak", "wb", backup_agenda, None)

        operar_arquivo(f"{DIRETORIO_ATUAL}/agenda.json", 'w', agenda)
    except:
        pass

    return

# feito
def ler_agenda():
    agenda = {}

    try:
        agenda = operar_arquivo(f"{DIRETORIO_ATUAL}/agenda.json", 'r')
    except:
        try:
            agenda = operar_arquivo(f"{DIRETORIO_ATUAL}/agenda.json.bak", 'r')
        except:
            pass
        salvar_agenda(agenda)

    return agenda

# feito
def data_valida(valores: list):
    retorno = True
    try:
        time.mktime(time.strptime(f"{valores[0]} {valores[1]} {valores[2]} {valores[3]} {valores[4]}", "%Y %m %d %H %M"))
    except:
        retorno = False

    return retorno

# feito
def selecionar_data(agi):
    data = [
        [0, 4, "ano"],
        [1, 2, "mes"],
        [1, 2, "dia"],
        [0, 2, "hora"],
        [0, 2, "minuto"]
    ]

    index = 0
    tentativa = NEUTRO
    while (index < 5 and tentativa < INATIVO):
        valor = agi.get_data(f"{DIRETORIO_ATUAL}/res/audios/selecionar_{data[index][2]}", 5000, data[index][1])
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            return False, INATIVO

        if (valor == ''):
            agi.stream_file(VOU_REPETIR)
            continue
        elif (valor == '*'):
            return True, VOLTAR
        elif (valor == '0'):
            return False, DESLIGAR

        valor = int(valor)
        valores = [data[0][0], data[1][0], data[2][0], data[3][0], data[4][0]]
        valores[index] = valor
        if (not data_valida(valores)):
            tentativa = NEUTRO
            agi.stream_file(DADO_INVALIDO)
            continue

        data[index][0] = valor
        index += 1

    return str(int(time.mktime(time.strptime(f"{data[0][0]} {data[1][0]} {data[2][0]} {data[3][0]} {data[4][0]}", "%Y %m %d %H %M"))) + CORRECAO_HORARIO), VOLTAR

# feito
def falar_data(timestamp: str, agi):
    timestamp_real = int(timestamp) - CORRECAO_HORARIO
    data = time.strftime("%Y %m %d %H %M", time.gmtime(timestamp_real)).split()
    data = [
        [int(data[0]), "ano"],
        [int(data[1]), "mes"],
        [int(data[2]), "dia"],
        [int(data[3]), "hora"],
        [int(data[4]), "minuto"]
    ]

    valor = ''
    for index in range(len(data)):
        valor = agi.get_data(f"{DIRETORIO_ATUAL}/res/audios/{data[index][1]}", 500)
        if (valor != ''):
            break
        valor = agi.say_number(data[index][0], "#*1234567890")
        if (valor != ''):
            valor += agi.get_data(SILENCIO, 5000)
            break

    return valor

# feito
def falar_compromissos(compromissos: tuple, agi):
    valor = agi.get_data(FALAR_COMPROMISSOS, 1000)
    if (valor != ''):
        return valor

    for index in range(len(compromissos)):
        valor = agi.get_data(NUMERO, 500)
        if (valor != ''):
            valor += agi.get_data(SILENCIO, 5000)
            break
        valor = agi.say_number(index + 1, "#*1234567890")
        if (valor != ''):
            valor += agi.get_data(SILENCIO, 5000)
            break
        valor = falar_data(compromissos[index], agi)
        if (valor != ''):
            break

    return valor

# feito
def gravar_audio(agi):
    timestamp_agora = str(time.time())

    try:
        valor = agi.record_file(f"/tmp/{timestamp_agora}", escape_digits = "#*1234567890", timeout = 120000)
    except:
        agi.verbose(f"Erro: não foi possível armazenar o áudio temporário no diretório /tmp!")
        agi.stream_file(ERRO_SALVAR)
        return False, DESLIGAR

    if (valor == '0'):
        return False, DESLIGAR

    return f"/tmp/{timestamp_agora}", VOLTAR

# feito
def tocar_audio(caminho: str, agi):
    try:
        valor = agi.get_data(caminho, 1000, 1)
    except:
        agi.verbose(f"Erro: não foi possível tocar o áudio {caminho}.gsm!")
        agi.stream_file(ERRO_TOCAR)
        return DESLIGAR

    if (valor == '0'):
        return DESLIGAR

    return VOLTAR

# feito
def salvar_audio(caminho: str, ramal: str, timestamp: str, agi):
    try:
        if (not os.path.isdir(f"{DIRETORIO_ATUAL}/compromissos")):
            os.mkdir(f"{DIRETORIO_ATUAL}/compromissos")
        audio = operar_arquivo(f"{caminho}.gsm", "rb", None, None)
        operar_arquivo(f"{DIRETORIO_ATUAL}/compromissos/{ramal}_{timestamp}.gsm", "wb", audio, None)
    except:
        agi.verbose(f"Erro: não foi possível salvar o áudio {DIRETORIO_ATUAL}/compromissos/{ramal}_{timestamp}.gsm!")
        agi.stream_file(ERRO_SALVAR)
        return False, DESLIGAR

    return True, VOLTAR

# feito
def preparar_data(ramal: str, agi):
    retorno = False
    continuar = True
    agi.stream_file(SELECIONAR_DATA)
    while (continuar):
        agenda = ler_agenda()
        if (not ramal in agenda):
            agenda[ramal] = {}
            salvar_agenda(agenda)

        valor = selecionar_data(agi)
        if (isinstance(valor[0], bool)):
            retorno = valor
            return retorno
        elif (valor[0] in agenda[ramal]):
            agi.stream_file(DATA_EXISTENTE)
            continue

        continuar = False
        agi.stream_file(DATA_ESCOLHIDA)

    timestamp = valor[0]
    tentativa = NEUTRO
    while (tentativa < INATIVO):
        valor = agi.get_data(OUVIR_DATA, 5000, 2)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            retorno = retorno, tentativa
            agi.stream_file(INATIVIDADE)
            return retorno

        if (valor == ''):
            agi.stream_file(VOU_REPETIR)
        elif (valor == '*'):
            tentativa = DESLIGAR
            retorno = True, VOLTAR
        elif (valor == '0'):
            tentativa = DESLIGAR
            retorno = retorno, tentativa
        elif (valor == '1'):
            tentativa = NEUTRO
            falar_data(timestamp, agi)
        else:
            tentativa = DESLIGAR
            retorno = timestamp, VOLTAR

    return retorno

# feito
def preparar_audio(ramal: str, timestamp: str, agi):
    agi.stream_file(GRAVAR_AUDIO)
    valor = gravar_audio(agi)
    if (isinstance(valor[0], bool)):
        retorno = valor
        return retorno

    caminho = valor[0]
    retorno = False
    tentativa = NEUTRO
    while (tentativa < INATIVO):
        valor = agi.get_data(OUVIR_AUDIO, 5000, 2)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            retorno = retorno, tentativa
            agi.stream_file(INATIVIDADE)
            continue

        if (valor == ''):
            agi.stream_file(VOU_REPETIR)
        elif (valor == '*'):
            tentativa = DESLIGAR
            salvar = retorno, tentativa
            retorno = True, VOLTAR
        elif (valor == '0'):
            tentativa = DESLIGAR
            retorno = salvar = retorno, tentativa
        elif (valor == '1'):
            tentativa = NEUTRO
            tocar_audio(caminho, agi)
        else:
            tentativa = DESLIGAR
            retorno = salvar = salvar_audio(caminho, ramal, timestamp, agi)

    return retorno, salvar

# feito
def editar_compromisso(ramal: str, timestamp: str, acao: int = NEUTRO, tentativas: int = -1, agi = None):
    agenda = ler_agenda()

    if (acao == APAGAR):
        valor = agi.get_data(CONFIRMACAO, 5000, 1)
        if (valor != '5'):
            return True, VOLTAR

        agenda[ramal].pop(timestamp)
        salvar_agenda(agenda)
        try:
            os.remove(f"{DIRETORIO_ATUAL}/compromissos/{ramal}_{timestamp}.gsm")
        except:
            pass
        agi.stream_file(APAGADO)
        return False, FEITO

    if (acao == NEUTRO and tentativas > -1):
        agenda[ramal][timestamp] = tentativas
        salvar_agenda(agenda)
        return False, FEITO

    retorno = False
    tentativa = NEUTRO
    edicao = 0
    while (tentativa < INATIVO):
        valor = agi.get_data(EDITAR_COMPROMISSO, 5000, 1)
        if (valor == ''):
            tentativa += 1

        if (tentativa > 2):
            retorno = retorno, tentativa
            agi.stream_file(INATIVIDADE)
            return retorno

        if (valor == ''):
            agi.stream_file(VOU_REPETIR)
        elif (valor == '*'):
            retorno = True, VOLTAR
        elif (valor == '0'):
            tentativa = DESLIGAR
            retorno = retorno, tentativa
        elif (valor == '1'):
            tentativa = DESLIGAR
            edicao = 1
        elif (valor == '2'):
            tentativa = DESLIGAR
            edicao = 2
        else:
            tentativa = NEUTRO

    if (edicao == 1):
        timestamp_antiga = timestamp
        retorno = preparar_data(ramal, agi)
        if (isinstance(retorno[0], bool)):
            return retorno

        timestamp = retorno[0]
        retorno = salvar_audio(f"{DIRETORIO_ATUAL}/compromissos/{ramal}_{timestamp_antiga}", ramal, timestamp, agi)
        if (not retorno[0]):
            return retorno
        agenda = ler_agenda()
        agenda[ramal].pop(timestamp_antiga)
        agenda[ramal][timestamp] = 0
        salvar_agenda(agenda)
        retorno = True, FEITO
    elif (edicao == 2):
        retorno, salvar = preparar_audio(ramal, timestamp, agi)
        if (retorno == salvar and not salvar[0]):
            return retorno
        retorno = True, FEITO

    if (retorno[0]):
        agi.stream_file(EDICAO_REALIZADA)
    return retorno

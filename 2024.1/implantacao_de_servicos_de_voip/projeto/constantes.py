#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2024.1/implementacao_de_servicos_de_voip/projeto/constantes.py
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

USUARIO = "agenda" # MUDE-ME
SENHA = "voip2024.1" # MUDE-ME
IP = "localhost"
PORTA = 5038

FUSO_HORARIO = -3 # America/Recife (-0300)

import time, os

# A CORRECAO_HORARIO se dá pela soma das diferenças entre o fuso horário local
# invertido e o fuso horário GMT (0), e entre o fuso horário local invertido e
# o FUSO_HORARIO (em segundos)
# Nota: as inversões do fuso horário local na fórmula são necessárias devido ao
# "time.timezone" armazenar o fuso horário local de forma invertida. Exemplo:
# se o "time.timezone" está para o fuso America/Recife, ele deveria armazenar o
# equivalente a -3 horas, porém ele armazena o equivalente a +3 horas
CORRECAO_HORARIO = (-time.timezone - 0) + (-time.timezone - (FUSO_HORARIO * 60 * 60))

APAGAR = -1
VOLTAR = NEUTRO = 0
DESLIGAR = INATIVO = FEITO = 3

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_AUDIOS = f"{DIRETORIO_ATUAL}/res/audios"

VOU_REPETIR = f"{DIRETORIO_AUDIOS}/vou_repetir"
DADO_INVALIDO = f"{DIRETORIO_AUDIOS}/dado_invalido"
FALAR_COMPROMISSOS = f"{DIRETORIO_AUDIOS}/falar_compromissos"
SILENCIO = f"{DIRETORIO_AUDIOS}/silencio" # Áudio extraído do repositório https://github.com/anars/blank-audio
NUMERO = f"{DIRETORIO_AUDIOS}/numero"
ERRO_SALVAR = f"{DIRETORIO_AUDIOS}/erro_salvar"
ERRO_TOCAR = f"{DIRETORIO_AUDIOS}/erro_tocar"
SELECIONAR_DATA = f"{DIRETORIO_AUDIOS}/selecionar_data"
DATA_EXISTENTE = f"{DIRETORIO_AUDIOS}/data_existente"
DATA_ESCOLHIDA = f"{DIRETORIO_AUDIOS}/data_escolhida"
OUVIR_DATA = f"{DIRETORIO_AUDIOS}/ouvir_data"
INATIVIDADE = f"{DIRETORIO_AUDIOS}/inatividade"
GRAVAR_AUDIO = f"{DIRETORIO_AUDIOS}/gravar_audio"
OUVIR_AUDIO = f"{DIRETORIO_AUDIOS}/ouvir_audio"
CONFIRMACAO = f"{DIRETORIO_AUDIOS}/confirmacao"
APAGADO = f"{DIRETORIO_AUDIOS}/apagado"
EDITAR_COMPROMISSO = f"{DIRETORIO_AUDIOS}/editar_compromisso"
EDICAO_REALIZADA = f"{DIRETORIO_AUDIOS}/edicao_realizada"
REESCUTAR = f"{DIRETORIO_AUDIOS}/reescutar"
COMPROMISSO_SELECIONADO = f"{DIRETORIO_AUDIOS}/compromisso_selecionado"
SEM_COMPROMISSOS = f"{DIRETORIO_AUDIOS}/sem_compromissos"
MARCADO = f"{DIRETORIO_AUDIOS}/marcado"
BOAS_VINDAS = f"{DIRETORIO_AUDIOS}/boas_vindas"
MENU_INICIAL = f"{DIRETORIO_AUDIOS}/menu_inicial"
ATE_MAIS = f"{DIRETORIO_AUDIOS}/ate_mais"

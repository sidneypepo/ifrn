#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/projeto/funcoes.py
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

# Importando bibliotecas
from constantes import *
import os, socket, json, browser_history, time
if (OS == "nt"):
    import winreg
    CHAVES_WINDOWS = (
        winreg.HKEY_LOCAL_MACHINE,
        winreg.HKEY_CURRENT_USER
    )
    CAMINHOS_CHAVES = (
        "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    )

# Função para remover um arquivo no diretório local do programa
def remover_arquivo(nome_arquivo: str):
    os.remove(f"{DIRETORIO_ATUAL}/{nome_arquivo}")
    return

# Função para testar se uma string é um número natural
def ehnatural(numero: str):
    # Se a string for vazia, retorna-se False
    if (len(numero) < 1):
        return False

    # Navegando em cada caractere da string e, se algum deles não for
    # um caractere numérico, retorna-se False
    for index in range(len(numero)):
        if (numero[index] < '0' or numero[index] > '9'):
            return False

    # Retorna True, caso a string seja um número natural
    return True

# Função para testar se uma string é um número inteiro
def ehinteiro(numero: str):
    # Se a string for vazia, retorna-se False
    if (len(numero) < 1):
        return False

    # Se a string for um número natural retorna-se True. Se não,
    # se o primeiro caractere for um hífem e o resto da string
    # for um número natural, retorna-se True
    if (ehnatural(numero)):
            return True
    elif (numero[0] == '-' and ehnatural(numero[1:])):
        return True

    # Retorna False, casoa string não seja um número inteiro
    return False

# Função para obter total de ram de um cliente Windows
def obter_ram():
    ram = 0
    for linha in os.popen("wmic memorychip get capacity | findstr /i /v \"capacity\"").readlines():
        if (linha != '\n'):
            ram += int(linha.strip())

    return ram

# Função para retornar as informações de um cliente
def obter_informacoes():
    retorno = ''
    if (OS == "nt"):
        retorno += os.popen("wmic cpu get name | findstr /i /v \"name\"").readlines()[0]
        retorno += f"{os.cpu_count()}\n"
        retorno += f"{obter_ram() / (1024 * 1024)} MiB\n"
        retorno += os.popen("wmic diskdrive get size | findstr /i /v \"size\"").readlines()[0]
        so = os.popen("systeminfo | findstr /i /c:\"os name\"").readlines()[0].split(':')[1].strip()
        retorno += f"{so}\n"
        retorno += f"{os.getlogin()}\n"
        retorno += f"{os.path.expanduser('~')}\n"
        retorno += "Informação desconhecida!\n"
        retorno += "Informação desconhecida!\n"
        retorno += "Informação desconhecida!\n"
        retorno += "Informação desconhecida!\n"
        retorno += f"{socket.gethostname()}"
    else:
        retorno += os.popen("uname -p").readlines()[0]
        retorno += f"{os.cpu_count()}\n"
        ram = int(os.popen("cat /proc/meminfo | grep -i \"memtotal:\"").readlines()[0].split(':')[1].strip().split()[0])
        retorno += f"{ram / 1024:.2f} MiB\n"
        disco = os.popen("df -h --output=size / | grep -iv \"size\"").readlines()[0].strip()
        retorno += f"{disco[:-1]} {disco[-1]}iB\n"
        retorno += os.popen("cat /etc/os-release | grep -i \"pretty_name\" | cut -d '=' -f 2 | tr -d '\"'").readlines()[0]
        retorno += f"{os.getlogin()}\n"
        retorno += f"{os.path.expanduser('~')}\n"
        retorno += os.popen("id -u").readlines()[0]
        retorno += os.popen("id -ng").readlines()[0]
        retorno += os.popen("id -nG").readlines()[0]
        retorno += os.popen("printf \"%s\\n\" ${SHELL}").readlines()[0]
        retorno += f"{socket.gethostname()}"

    return retorno

# Função para retornar os clientes online
def obter_clientes(clientes: list):
    retorno = "ID | IP e porta | Nome do host | Usuário logado | Tempo online\n"

    identificador = 0
    for cliente in clientes:
        identificador += 1
        socket = cliente[2]["socket"]
        nome_host = cliente[2]["nome_host"]
        nome_usuario = cliente[2]["usuario"]
        diferenca_tempo = time.time() - cliente[2]["momento_conexao"]

        horas = int(diferenca_tempo // (60 * 60))
        minutos = int((diferenca_tempo % (60 * 60)) // 60)
        segundos = int(diferenca_tempo % 60)
        tempo_online = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

        retorno += f"{identificador} | {socket} | {nome_host} | {nome_usuario} | {tempo_online}\n"

    return retorno

# Função para retornar informações de hardware de um cliente
def obter_hardware(clientes: list, index: int):
    nome_cpu = clientes[index][2]["nome_cpu"]
    nucleos_cpu = clientes[index][2]["nucleos_cpu"]
    ram = clientes[index][2]["ram"]
    disco = clientes[index][2]["disco"]
    so = clientes[index][2]["so"]

    retorno = ''
    retorno += f"Socket (processador): {nome_cpu}\n"
    retorno += f"Threads (processadores lógicos): {nucleos_cpu}\n"
    retorno += f"Memória RAM (tamanho total): {ram}\n"
    retorno += f"Disco (tamanho total): {disco}\n"
    retorno += f"Sistema Operacional: {so}\n"

    return retorno

# Função para retornar informações do usuário logado de um cliente
def obter_usuario(clientes: list, index: int):
    usuario = clientes[index][2]["usuario"]
    home = clientes[index][2]["home"]
    uid = clientes[index][2]["uid"]
    grupo_principal = clientes[index][2]["grupo_principal"]
    grupos = clientes[index][2]["grupos"]
    shell = clientes[index][2]["shell"]

    retorno = ''
    retorno += f"Usuário: {usuario}\n"
    retorno += f"Diretório home: {home}\n"
    retorno += f"UID (ID de usuário): {uid}\n"
    retorno += f"Grupo principal: {grupo_principal}\n"
    retorno += f"Grupos secundários: {grupos}\n"
    retorno += f"Shell: {shell}\n"

    return retorno

# Função para ler o conteúdo de uma chave do registro do Windows
def ler_chave(registro_chave, modo_leitura: int):
    # Armazenando função de enumeração com base no modo de leitura
    if (modo_leitura == 1):
        funcao = winreg.EnumKey
    elif (modo_leitura == 2):
        funcao = winreg.EnumValue

    # Lendo todo o conteúdo da chave
    index = 0
    chaves = []
    while (True):
        try:
            chaves.append(funcao(registro_chave, index))
            index += 1
        except:
            break

    return chaves

# Função para ler registro de um cliente Windows
def ler_registro(diretorio_chave, caminho_chave):
    # Abrindo registro e chave do mesmo
    registro = winreg.ConnectRegistry(None, diretorio_chave)
    chave_registro = winreg.OpenKey(registro, caminho_chave)

    # Enumerando subchaves
    chaves = []
    for nome_subchave in ler_chave(chave_registro, 1):
        subchave = winreg.OpenKey(registro, f"{caminho_chave}\\{nome_subchave}")
        valores = {}

        # Enumerando valores da subchave
        for valor_subchave in ler_chave(subchave, 2):
            valores[valor_subchave[0]] = valor_subchave[1]

        chaves.append(valores)

    return chaves

# Função para retornar a lista de programas instalados em um
# cliente Windows
def programas_windows():
    programas = []
    for programa in ler_registro(CHAVES_WINDOWS[0], CAMINHOS_CHAVES[0]) + ler_registro(CHAVES_WINDOWS[0], CAMINHOS_CHAVES[1]) + ler_registro(CHAVES_WINDOWS[1], CAMINHOS_CHAVES[1]):
        if ("DisplayName" in programa):
            programas.append(programa["DisplayName"])

    return sorted(programas)

# Função para retornar a lista de programas instalados em um
# cliente Linux
def programas_linux():
    # Baseados em Debian
    programas = os.popen("apt list 2> /dev/null").readlines()[1:]
    if (len(programas) > 2):
        return programas

    # Baseados em RedHat
    programas = os.popen("dnf repoquery --qf \"%{name}.%{arch} %{version}.%{release} %{from_repo}\" --installed 2> /dev/null").readlines()
    if (len(programas) > 2):
        return programas

    # Baseados em Arch
    programas = os.popen("pacman -Q 2> /dev/null").readlines()
    if (len(programas) > 2):
        return programas

    # Baseados em Gentoo
    programas = os.popen("ls -d /var/db/pkg/*/* | cut -d '/' -f 5- 2> /dev/null").readlines()
    if (len(programas) > 2):
        return programas

    return ["Não foi possível obter lista de programas instalados!\n"]

# Função para formatar a lista de programas instalados em um
# cliente
def formatar_lista_programas(programas: list):
    retorno = ''
    for programa in programas:
        retorno += f"{programa.strip()}\n"

    return retorno

# Função para retornar os programas instalads em um cliente
def obter_programas():
    if (OS == "nt"):
        retorno = formatar_lista_programas(programas_windows())
    else:
        retorno = formatar_lista_programas(programas_linux())

    return retorno

# Função para retornar o histórico de navegação de um cliente
def obter_historico():
    historico = json.loads(browser_history.get_history().to_json())["history"]

    if (len(historico) > 200):
        historico = historico[-200:]

    retorno = ''
    for index in historico:
        retorno += index["URL"] + '\n'

    return retorno

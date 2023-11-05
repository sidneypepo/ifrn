#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ifrn/2023.2/programacao_para_redes/03_tcpdump/tcpdump.py
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

import os, funcoes

def main():
    pcap_info = funcoes.ler_pcap()
    if (pcap_info == None):
        return

    endianness = pcap_info[0]
    precision = pcap_info[1]
    pcap_header = pcap_info[2]
    pacotes = pcap_info[3]

    if (pcap_header["link_type"] != 1):
        funcoes.mostrar_erro(False, "Erro: protocolo de enlace desconhecido!" + pcap_header["link_type"])
        return

    ips = {}
    pares = {}
    media_pacotes = 0
    maior_pacote = 0
    incompletos = 0
    for index in range(len(pacotes)):
        media_pacotes += pacotes[index]["original_length"]

        if (pacotes[index]["original_length"] > maior_pacote):
            maior_pacote = pacotes[index]["original_length"]
        if (pacotes[index]["original_length"] != pacotes[index]["captured_length"]):
            incompletos += 1
        if (int.from_bytes((pacotes[index]["data"][12:14]), "big") != 2048):
            continue

        source_ip = (int.from_bytes(pacotes[index]["data"][26:27], "big"), int.from_bytes(pacotes[index]["data"][27:28], "big"), int.from_bytes(pacotes[index]["data"][28:29], "big"), int.from_bytes(pacotes[index]["data"][29:30], "big"))
        source_ip = f"{source_ip[0]}.{source_ip[1]}.{source_ip[2]}.{source_ip[3]}"
        if (not source_ip in ips):
            ips[source_ip] = 0
        ips[source_ip] += 1

        destination_ip = (int.from_bytes(pacotes[index]["data"][30:31], "big"), int.from_bytes(pacotes[index]["data"][31:32], "big"), int.from_bytes(pacotes[index]["data"][32:33], "big"), int.from_bytes(pacotes[index]["data"][33:34], "big"))
        destination_ip = f"{destination_ip[0]}.{destination_ip[1]}.{destination_ip[2]}.{destination_ip[3]}"
        if (not destination_ip in ips):
            ips[destination_ip] = 0
        ips[destination_ip] += 1

        if (f"{source_ip}-{destination_ip}" in pares):
            pares[f"{source_ip}-{destination_ip}"] += 1
        elif (f"{destination_ip}-{source_ip}" in pares):
            pares[f"{destination_ip}-{source_ip}"] += 1
        else:
            pares[f"{source_ip}-{destination_ip}"] = 1

    media_pacotes /= len(pacotes)
    ips = dict(sorted(ips.items(), key=lambda item: item[1], reverse=True))
    pares = dict(sorted(pares.items(), key=lambda item: item[1], reverse=True))

    inicio_captura = funcoes.segundos_data(pacotes[0]["timestamp"], pacotes[0]["precision"], precision, -3)
    fim_captura = funcoes.segundos_data(pacotes[-1]["timestamp"], pacotes[-1]["precision"], precision, -3)
    if (inicio_captura != None and fim_captura != None):
        print(f"Início | fim captura                : {inicio_captura} | {fim_captura}")
    else:
        return

    print(f"Tamanho maior pacote (em bytes)     : {maior_pacote}")

    print(f"Pacotes incompletos capturados      : ", end='')
    if (incompletos > 0):
        print(f"Sim, {incompletos} pacotes")
    else:
        print(f"Não")

    print(f"Tamanho médio dos pacotes (em bytes): {media_pacotes:.2f}")

    print(f"Par de IP's com maior tráfego       : {list(pares.items())[0][0]}")
    print(f"Total de IP's distintos             : {len(ips) - 1:02d}")

    return

if (__name__ == "__main__"):
    try:
        main()
    except:
        print("\nSaindo...")

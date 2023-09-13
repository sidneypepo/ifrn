#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PC2023-1-ativ5-q5.py
#
# Aluno 1: Sidney Pedro
# Aluno 2: Iuri da Silva
#
# Última alteração: 2023-07-30
#

# Definindo variáveis utilizadas ao longo das funções
NOME_ARQUIVO = "dados.json"
ALTERACOES = {
    "adicoes": {},
    "remocoes": {}
}

# Definindo função para exibir menus
def menus(menu_id):
    # Apresentando menu correspondente ao ID passado
    if (menu_id == 0):
        print("1. Cadastrar um CPF")
        print("2. Remover um CPF")
        print("3. Adicionar um MAC vinculado a um CPF")
        print("4. Remover um MAC vinculado a um CPF")
        print("5. Listar os CPFs cadastrados")
        print("6. Listar os MACs vinculados a um CPF")
        print("7. Sair\n")
    elif (menu_id == 1):
        print("1. Voltar")
        print("Digite o CPF a ser cadastrado\n")
    elif (menu_id == 2):
        print("1. Voltar")
        print("Digite o CPF a ser removido\n")
    elif (menu_id == 3):
        print("1. Voltar")
        print("Digite o CPF o qual o MAC deve ser vinculado\n")
    elif (menu_id == 4):
        print("1. Voltar")
        print("Digite o MAC a ser cadastrado\n")
    elif (menu_id == 5):
        print("1. Voltar")
        print("Digite o CPF o qual o MAC deve ser desvinculado\n")
    elif (menu_id == 6):
        print("1. Voltar")
        print("Digite o MAC a ser removido\n")
    elif (menu_id == 7):
        print("1. Voltar")
        print("Digite o CPF o qual deseja-se listar os MACs vinculados\n")
    elif (menu_id == 8):
        print("1. Voltar")
        print("2. Sair sem salvar")
        print("3. Salvar e sair\n")

    return

# Definindo função para exibir erros
def erro(erro_id):
    # Apresentando erro correspondente ao ID passado
    if (erro_id == 0):
        print("Erro: opção inválida!\n")
    elif (erro_id == 1):
        print("Erro: CPF inválido!\n")
    elif (erro_id == 2):
        print("Erro: MAC inválido!\n")
    elif (erro_id == 3):
        print("Erro: CPF já cadastrado!\n")
    elif (erro_id == 4):
        print("Erro: CPF não cadastrado!\n")
    elif (erro_id == 5):
        print("Erro: MAC já cadastrado!\n")
    elif (erro_id == 6):
        print("Erro: MAC não cadastrado!\n")

    return

# Definindo função para padronizar o recebimento de dado do
# usuário e evitar repetição de código
def entrada_padrao():
    entrada = input(">>> ")
    print()

    return entrada

# Definindo função para receber, formatar e validar dado
def receber_dado(tipo_dado):
    # Se o tipo de dado informado for 1, então o dado será
    # obtido e tratado como CPF e o retorna se for válido
    if (tipo_dado == 1):
        cpf = entrada_padrao().replace('.', '').replace('-', '')
        if ((cpf.isnumeric() == True and len(cpf) == 11) or cpf == '1'):
            return cpf
        else:
            erro(1)
            return False
    # Se o tipo de dado informado for 2, então o dado será
    # obtido e tratado como MAC e o retorna se for válido
    elif (tipo_dado == 2):
        mac = entrada_padrao().replace(':', '').replace('-', '')
        if (len(mac) == 12 or mac == '1'):
            return mac
        else:
            erro(2)
            return False

# Definindo função para testar se o arquivo de dados existe
def testar_arquivo():
    # Se o arquivo não existir, ele será criado
    try:
        arquivo = open(NOME_ARQUIVO, 'r')
        existe = True
    except:
        arquivo = open(NOME_ARQUIVO, 'w')
        arquivo.write("{\n}\n")
        existe = False
    arquivo.close()

    return existe

# Definindo função para localizar um CPF
def buscar_cpf(cpf):
    # Se o CPF for uma chave do subdicionario "remocoes" e sua
    # lista possuir um elemento (o 0), significa não encontrou
    # o CPF, pois o mesmo será removido do arquivo se salvar as
    # alterações e sair do programa
    if (cpf in ALTERACOES["remocoes"]):
        if (ALTERACOES["remocoes"][cpf][0] == 0):
            return False

    # Lendo as linhas do arquivo de dados e, se estiver em
    # alguma, significa que encontrou o CPF
    testar_arquivo()
    arquivo = open(NOME_ARQUIVO, 'r')
    for linha in arquivo:
        if (cpf in linha.split(':')[0]):
            arquivo.close()
            return True
    arquivo.close()

    # Se o CPF for uma chave do subdicionario "adicoes",
    # significa que o encontrou
    if (cpf in ALTERACOES["adicoes"]):
        return True

    # Retorna-se falso se nenhuma das buscas anteriores
    # encontrou o CPF
    return False

# Definindo função para localizar um MAC vinculado a um CPF
def buscar_mac(cpf, mac):
    # Se o CPF for uma chave do subdicionario "remocoes" e o
    # MAC estiver em sua lista, significa não o encontrou,
    # pois o mesmo será removido do arquivo se salvar as
    # alterações e sair do programa
    if (cpf in ALTERACOES["remocoes"]):
        if (mac in ALTERACOES["remocoes"][cpf]):
            return False

    # Lendo as linhas do arquivo de dados e, se o MAC estiver
    # na mesma linha que o CPF, significa que o encontrou
    testar_arquivo()
    arquivo = open(NOME_ARQUIVO, 'r')
    for linha in arquivo:
        if (cpf in linha.split(':')[0] and mac in linha.split(':')[1]):
            arquivo.close()
            return True
    arquivo.close()

    # Se o CPF for uma chave do subdicionario "adicoes" e o
    # MAC estiver em sua lista, significa que o encontrou
    if (cpf in ALTERACOES["adicoes"]):
        if (mac in ALTERACOES["adicoes"][cpf]):
            return True

    # Retorna-se falso se nenhuma das buscas anteriores
    # encontrou o MAC
    return False

# Definindo função para obter dado e testar se está adequado
# ao contexto especificado
def obter_testar_dado(menu_id, tipo_dado, cpf=0):
    while (True):
        # Apresentando menu
        menus(menu_id)

        # Recebendo dado do usuário e retornando 1 se o dado
        # recebido for 1
        dado = receber_dado(tipo_dado)
        if (dado == '1'):
            return 1

        # Testando a existência do dado e definindo ID para
        # erro em relação ao contexto
        if (dado != False and menu_id == 1):
            resultado_teste = buscar_cpf(dado) == True
            erro_id = 3
        elif (dado != False and (menu_id == 2 or menu_id == 3 or menu_id == 5 or menu_id == 7)):
            resultado_teste = buscar_cpf(dado) == False
            erro_id = 4
        elif (dado != False and menu_id == 4):
            resultado_teste = buscar_mac(cpf, dado) == True
            erro_id = 5
        elif (dado != False and menu_id == 6):
            resultado_teste = buscar_mac(cpf, dado) == False
            erro_id = 6

        # Apresentando erro se o resultado do teste anterior
        # for verdadeiro ou retornando o dado (se for válido)
        if (dado != False and resultado_teste == True):
            erro(erro_id)
        elif (dado != False):
            return dado

# Definindo função para apresentar um dado
def apresentar_se_existir(tipo_dado, item, cpf=0):
    # Apresentando CPF se ele já estiver armazenado no arquivo
    esta_no_arquivo = True
    if (item in ALTERACOES["adicoes"]):
        if (ALTERACOES["adicoes"][item][0] == 0):
            esta_no_arquivo = False
    if (tipo_dado == 1):
        if (buscar_cpf(item) == True and esta_no_arquivo == True):
            print(f"- {item}")
    # Apresentano MAC
    elif (tipo_dado == 2):
        if (buscar_mac(cpf, item) == True and item != 0 and item != ''):
            print(f"- {item}")

    return

# Definindo função para adicionar MAC(s) a uma linha
def adicionar_macs(linha):
    # Testando se a linha passada possui chave correspondente
    # a uma das chaves armazenadas no subdicionario "adicoes"
    cpf = ''
    for chave in ALTERACOES["adicoes"].keys():
        if (chave in linha.split(':')[0]):
            cpf = chave
    if (cpf == ''):
        return linha

    # Removendo o finalizador de linha (se houver)
    if (linha[-1] == ']'):
        linha = linha[:-1]

    # Adicionando MAC(s) à linha
    for mac in ALTERACOES["adicoes"][cpf]:
        if (linha[-1] != '['):
            inicio_proximo = ", "
        else:
            inicio_proximo = ''
        linha += inicio_proximo + f"\"{mac}\""

    # Removendo chave do subdicionario "adicoes" e retornando
    # linha com fechamento
    ALTERACOES["adicoes"].pop(cpf)
    return linha + ']'

# Definindo função para remover linha ou MAC(s) de uma linha
def remover_linha(linha):
    # Testando se a linha passada possui chave correspondente
    # a uma das chaves armazenadas no subdicionario "remocoes"
    cpf = ''
    for chave in ALTERACOES["remocoes"].keys():
        if (chave in linha.split(':')[0]):
            cpf = chave
    if (cpf == ''):
        return linha

    # Se a chave do subdicionario "remocoes" for uma lista
    # com um elemento (o 0), significa que a linha deve ser
    # totalmente removida
    if (len(ALTERACOES["remocoes"][cpf]) == 1):
        if (ALTERACOES["remocoes"][cpf][0] == 0):
            # Removendo chave do subdicionario "remocoes"
            ALTERACOES["remocoes"].pop(cpf)
            # Retornando linha vazia
            return ''

    # Removendo o finalizador de linha (se houver)
    if (linha[-1] == ']'):
        linha = linha[:-1]

    # Removendo MAC(s) da linha
    for mac in ALTERACOES["remocoes"][cpf]:
        inicio_mac = linha.find(mac) - 1
        if (linha[inicio_mac - 1] != '['):
            inicio_mac -= 2
        final_mac = inicio_mac + len(mac) + 4
        linha = linha[:inicio_mac] + linha[final_mac:]

    # Removendo chave do subdicionario "remocoes" e
    # retornando linha com fechamento
    ALTERACOES["remocoes"].pop(cpf)
    return linha + ']'

# Definindo função para adicionar uma linha
def adicionar_linha(linha_anterior, cpf):
    # Escolhendo qual quebra de linha deve ser utilizada
    if (linha_anterior != "{\n"):
        quebra_de_linha = ",\n"
    else:
        quebra_de_linha = ''

    # Se a chave do subdicionario "adicoes" só possuir um
    # elemento (o 0), a chave possuirá uma lista vazia no
    # arquivo. Caso contrário, a chave possuirá todos os
    # elementos de sua lista, exceto o primeiro (que é o 0)
    if (len(ALTERACOES["adicoes"][cpf]) == 1):
        return f"{quebra_de_linha}    \"{cpf}\": []"
    else:
        macs = ''
        for mac in ALTERACOES["adicoes"][cpf]:
            macs += f", \"{mac}\""
        return f"{quebra_de_linha}    \"{cpf}\": [{macs[7:]}]"

# Definindo função para salvar as alterações feitas no arquivo
def salvar():
    # Se não houver nenhuma alteração feita, apenas retorna
    if (len(ALTERACOES["adicoes"]) == 0 and len(ALTERACOES["remocoes"]) == 0):
        print("Nenhuma alteração feita. Saindo.\n")
        return

    print("Salvando alterações...", end='')

    # Copiando conteúdo do arquivo original para um arquivo
    # temporário
    testar_arquivo()
    arquivo_original = open(NOME_ARQUIVO, 'r')
    arquivo_temp = open(f"{NOME_ARQUIVO}.temp", 'w')
    for linha in arquivo_original:
        arquivo_temp.write(linha)
    arquivo_original.close()
    arquivo_temp.close()

    # Abrindo arquivo temporário e arquivo final e aplicando
    # alterações de adição de MAC(s) e remoção de linha(s)
    arquivo_original = open(f"{NOME_ARQUIVO}.temp", 'r')
    arquivo_final = open(NOME_ARQUIVO, 'w')
    linha_anterior = "{\n"
    for linha in arquivo_original:
        # Removendo final da linha
        if (linha[-3:] == "],\n"):
            linha = linha[:-2]
        elif (linha[-2:] == "]\n"):
            linha = linha[:-1]

        # Testando se há alterações a serem realizadas e, se
        # sim, submetendo a linha às alterações
        if (len(ALTERACOES["adicoes"]) != 0):
            linha = adicionar_macs(linha)
        if (len(ALTERACOES["remocoes"]) != 0):
            linha = remover_linha(linha)

        # Adicionando finalização à linha anterior se a
        # mesma não for a primeira e a atual não for vazia ou
        # a última
        if (linha != '' and linha != "}\n" and linha_anterior != "{\n"):
            linha = ",\n" + linha
        # Armazenando linha anterior se a atual não for vazia
        # ou a última
        if (linha != '' and linha != "}\n"):
            linha_anterior = linha
        # Escrevendo linha se a mesma não for a última
        if (linha != "}\n"):
            arquivo_final.write(linha)
    arquivo_original.close()

    # Se ainda houver alterações a serem feitas, navega-se nas
    # chaves restantes e as mesmas são escritas no arquivo
    if (len(ALTERACOES["adicoes"]) != 0):
        for chave in ALTERACOES["adicoes"].keys():
            arquivo_final.write(adicionar_linha(linha_anterior, chave))
            linha_anterior = adicionar_linha(linha_anterior, chave)

    # Se a linha for a última e a anterior não for a primeira,
    #adiciona-se uma quebra de linha
    if (linha == "}\n" and linha_anterior != "{\n"):
        arquivo_final.write('\n')

    # Escrevendo última linha, fechando o arquivo e saindo
    arquivo_final.write(linha)
    arquivo_final.close()
    print(" Salvo com sucesso!\n")
    return

# Definindo função para cadastrar um CPF
def cadastrar_cpf():
    # Obtendo um CPF e voltando se o mesmo for igual a 1
    cpf = obter_testar_dado(1, 1)
    if (cpf == 1):
        return

    # Se o CPF informado estiver no subdicionario "remocoes" e
    # sua lista possuir um elemento (o 0), o mesmo é removido
    # do subdicionario
    if (cpf in ALTERACOES["remocoes"]):
        if (ALTERACOES["remocoes"][cpf][0] == 0):
            ALTERACOES["remocoes"].pop(cpf)

    # Se o CPF não estiver armazenado no arquivo, o mesmo é
    # adicionado ao subdicionario "adicoes" com o primeiro
    # elemento da lista igual a 0
    if (buscar_cpf(cpf) == False):
        ALTERACOES["adicoes"][cpf] = [0]
        print(f"O CPF {cpf} será adicionado ao salvar as alterações e sair.\n")

    return

# Definindo função para remover um CPF
def remover_cpf():
    # Obtendo um CPF e voltando se o mesmo for igual a 1
    cpf = obter_testar_dado(2, 1)
    if (cpf == 1):
        return

    # Se o CPF informado estiver no subdicionario "adicoes", o
    # mesmo é removido do subdicionario
    if (cpf in ALTERACOES["adicoes"]):
        ALTERACOES["adicoes"].pop(cpf)

    # Se o CPF estiver armazenado no arquivo, o mesmo é
    # adicionado ao subdicionario "remocoes" com o primeiro
    # elemento da lista igual a 0
    if (buscar_cpf(cpf) == True):
        ALTERACOES["remocoes"][cpf] = [0]
        print(f"O CPF {cpf} será removido ao salvar as alterações e sair.\n")

    return

# Definindo função para
def cadastrar_mac():
    # Obtendo um CPF e voltando se o mesmo for igual a 1
    cpf = obter_testar_dado(3, 1)
    if (cpf == 1):
        return

    # Obtendo um MAC e voltando se o mesmo for igual a 1
    mac = obter_testar_dado(4, 2, cpf)
    if (mac == 1):
        return

    # Se o CPF informado estiver no subdicionario "remocoes" e
    # o MAC estiver em sua lista, o mesmo é removido da lista
    # e, se a lista ficar vazia, a mesma é removida do
    # subdicionario
    if (cpf in ALTERACOES["remocoes"]):
        if (mac in ALTERACOES["remocoes"][cpf]):
            ALTERACOES["remocoes"][cpf].remove(mac)
        if (len(ALTERACOES["remocoes"][cpf]) == 0):
            ALTERACOES["remocoes"].pop(cpf)

    # Se o MAC não estiver armazenado no arquivo vinculado ao
    # CPF, o CPF é adicionado ao subdicionario "adicoes" (caso
    # já não esteja) e é adicionado o MAC à sua lista
    if (buscar_mac(cpf, mac) == False):
        if (not cpf in ALTERACOES["adicoes"]):
            ALTERACOES["adicoes"][cpf] = []
        ALTERACOES["adicoes"][cpf].append(mac)
        print(f"O MAC {mac} será vinculado ao CPF {cpf} ao salvar as alterações e sair.\n")

    return

# Definindo função para
def remover_mac():
    # Obtendo um CPF e voltando se o mesmo for igual a 1
    cpf = obter_testar_dado(5, 1)
    if (cpf == 1):
        return

    # Obtendo um MAC e voltando se o mesmo for igual a 1
    mac = obter_testar_dado(6, 2, cpf)
    if (mac == 1):
        return

    # Se o CPF informado estiver no subdicionario "adicoes" e o
    # MAC estiver em sua lista, o mesmo é removido da lista e,
    # se a lista ficar vazia, a mesma é removida do
    # subdicionario
    if (cpf in ALTERACOES["adicoes"]):
        if (mac in ALTERACOES["adicoes"][cpf]):
            ALTERACOES["adicoes"][cpf].remove(mac)
        if (len(ALTERACOES["adicoes"][cpf]) == 0):
            ALTERACOES["adicoes"].pop(cpf)

    # Se o MAC estiver armazenado no arquivo vinculado ao CPF,
    # o CPF é adicionado ao subdicionario "remocoes" (caso
    # já não esteja) e é adicionado o MAC à sua lista
    if (buscar_mac(cpf, mac) == True):
        if (not cpf in ALTERACOES["remocoes"]):
            ALTERACOES["remocoes"][cpf] = []
        ALTERACOES["remocoes"][cpf].append(mac)
        print(f"O MAC {mac} será desvinculado do CPF {cpf} ao salvar as alterações e sair.\n")

    return

# Definindo função para listar os CPFs existentes 
def listar_cpfs():
    # Listando os CPFs ainda não armazenados no arquivo
    for cpf in ALTERACOES["adicoes"].keys():
        if (ALTERACOES["adicoes"][cpf][0] == 0):
            print(f"- {cpf}")

    # Se o arquivo não existir, retorna-se
    arquivo_existe = testar_arquivo()
    if (arquivo_existe == False):
        print()
        return

    # Abrindo o arquivo e apresentando os CPFs armazenados
    arquivo = open(NOME_ARQUIVO, 'r')
    itens_arquivo = []
    for linha in arquivo:
        if (':' in linha):
            linha = linha.split()
            apresentar_se_existir(1, linha[0][1:-2])
    arquivo.close()
    print()
    return

# Definindo função para
def listar_macs():
    # Obtendo um CPF e voltando se o mesmo for igual a 1
    cpf = obter_testar_dado(7, 1)
    if (cpf == 1):
        return

    # Listando os MACs vinculados ao CPF ainda não armazenados
    # no arquivo
    if (cpf in ALTERACOES["adicoes"]):
        for mac in ALTERACOES["adicoes"][cpf]:
            apresentar_se_existir(2, mac, cpf)

    # Se o arquivo não existir, retorna-se
    arquivo_existe = testar_arquivo()
    if (arquivo_existe == False):
        print()
        return

    # Abrindo o arquivo e armazenando os MACs vinculados ao CPF
    arquivo = open(NOME_ARQUIVO, 'r')
    macs = 0
    for linha in arquivo:
        if (cpf in linha):
            macs = linha.split()[1:]
    arquivo.close()

    # Apresentando os MACs vinculados ao CPF do arquivo
    if (macs != 0):
        for mac in macs:
            mac = mac.replace('[', '').replace(']', '').replace(',', '').replace('"', '')
            apresentar_se_existir(2, mac, cpf)

    print()
    return

# Definindo função para sair do programa
def sair():
    while (True):
        # Apresentando menu de saída e obtendo opção do usuário
        menus(8)
        opcao = entrada_padrao()

        # Voltando se a opção digitada for 1, saindo se for 2,
        # salvando e saindo se for 3 ou apresentando erro se
        # não for nenhuma das três
        if (opcao == '1'):
            return False
        elif (opcao == '2'):
            return True
        elif (opcao == '3'):
            salvar()
            return True
        else:
            erro(0)

# Definindo variável de controle de repetições do programa
finalizar = False
while (finalizar == False):
    # Apresentando menu principal e obtendo opção do usuário
    menus(0)
    # print(ALTERACOES) # Descomente para ver as alterações armazenadas
    opcao = entrada_padrao()

    # Realizando operação de acordo com a opção selecionada ou
    # apresentando erro se a opção digitada for inválida
    if (opcao == '1'):
        cadastrar_cpf()
    elif (opcao == '2'):
        remover_cpf()
    elif (opcao == '3'):
        cadastrar_mac()
    elif (opcao == '4'):
        remover_mac()
    elif (opcao == '5'):
        listar_cpfs()
    elif (opcao == '6'):
        listar_macs()
    elif (opcao == '7'):
        finalizar = sair()
    else:
        erro(0)

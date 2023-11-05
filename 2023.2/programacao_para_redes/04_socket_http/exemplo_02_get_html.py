import socket, sys

# --------------------------------------------------
PORT        = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 256
CL_SIZE     = len("Content-Length: ")
# --------------------------------------------------

# host = input('\nInforme o nome do HOST ou URL do site: ')
host = "aquitemremedio.prefeitura.sp.gov.br"
# host = "gaia.cs.umass.edu"
# host = "www.bancocn.com"

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def tamanho_resposta(resposta: bytes):
    if (b"Transfer-Encoding: chunked" in resposta):
        return "chunked"
    elif (not b"Content-Length: " in resposta):
        return ""

    cl_posicao = resposta.index(b"Content-Length: ") + CL_SIZE
    if (not b"\r\n" in resposta[cl_posicao:]):
        return ""
    cl_posicao_fim = cl_posicao + resposta[cl_posicao:].index(b"\r\n")

    return str(resposta[cl_posicao:cl_posicao_fim])[2:-1]

def resposta_recebida(resposta: bytes):
    inicio_resposta = resposta.index(b"\r\n\r\n") + 4
    return len(resposta[inicio_resposta:])

try:
    tcp_socket.connect((host, PORT))
except:
    print(f'\nERRO.... {sys.exc_info()[0]}')
    exit()

# tcp_socket.settimeout(5)
requisicao = f"GET / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n"
try:
    tcp_socket.sendall(requisicao.encode(CODE_PAGE))
except:
    print(f'\nERRO.... {sys.exc_info()[0]}')
    exit()

print('-'*50)
resposta = b""
tipo_tamanho = ""
bytes_recebidos = 0
total_bytes = 1
while ((tipo_tamanho != "chunked" or resposta[-5:] != b"0\r\n\r\n") and bytes_recebidos != total_bytes):
    nova_resposta = tcp_socket.recv(BUFFER_SIZE)
    resposta += nova_resposta
    # print(str(nova_resposta)[2:-1], end="")
    print(nova_resposta.decode(CODE_PAGE), end="")

    if (tipo_tamanho.isdecimal()):
        total_bytes = int(tipo_tamanho)
        bytes_recebidos = resposta_recebida(resposta)
    elif (tipo_tamanho == ""):
        tipo_tamanho = tamanho_resposta(resposta)

print('-'*50)
tcp_socket.close()

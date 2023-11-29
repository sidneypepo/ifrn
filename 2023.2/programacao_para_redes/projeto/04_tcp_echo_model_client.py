import socket
from socket_constants import *

# Criando o socket TDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket a porta
tcp_socket.connect((HOST_SERVER, SOCKET_PORT))

while True:
    # Recebendo echo do servidor
    dado_recebido     = tcp_socket.recv(BUFFER_SIZE)
    mensagem_recebida = dado_recebido.decode(CODE_PAGE)
    print(f'Mensagem Recebida: {mensagem_recebida}')

    # Devolvendo uma mensagem (echo) ao cliente
    mensagem_retorno = 'Devolvendo mensagem: ' + mensagem_recebida
    tcp_socket.send(mensagem_retorno.encode(CODE_PAGE))

# Fechando o socket
tcp_socket.close()

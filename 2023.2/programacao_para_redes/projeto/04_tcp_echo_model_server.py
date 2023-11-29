import socket
from socket_constants import *

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket a porta
tcp_socket.bind((HOST_SERVER, SOCKET_PORT))

# Máximo de conexões enfileiradas
tcp_socket.listen(MAX_LISTEN)

while True:
    # Aceita a conexão com o cliente
    conexao, cliente = tcp_socket.accept()
    print('Conectado por: ', cliente)
    while True:
        mensagem = input('Digite a mensagem: ')
        if not mensagem:
            continue
        # Convertendo a mensagem digitada de string para bytes
        mensagem = mensagem.encode(CODE_PAGE)
        # Enviando a mensagem ao cliente
        conexao.send(mensagem)

        mensagem = conexao.recv(BUFFER_SIZE)
        if not mensagem:
            break
        print(cliente, mensagem.decode(CODE_PAGE))

    print('Finalizando Conexão do Cliente ', cliente)
    conexao.close()

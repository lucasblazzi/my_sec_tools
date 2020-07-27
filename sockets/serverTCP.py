import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "0.0.0.0"                          # qualquer IP (local, rede interna, rede externa)
port = 777

try:
    server.bind((ip, port))
    server.listen(5)                    # numero de conexoes consecutivas
    print("Listening in: {}:{}".format(ip, port))

    client_socket, address = server.accept()                     # aguarda a conexao do client

    print("Connection received from: {}" .format(address[0]))

    while True:
        data = client_socket.recv(1024)
        print(data)
        client_socket.send("\n_____\nData received\n_____\n".encode())

except Exception as error:
    print("Error: " + str(error))
    server.close()                      # fecha a conexao

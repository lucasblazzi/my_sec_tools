import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET-->IPV4, SOCK_DGRAM-->UDP
target_host = ""
target_port = 80
msg = "MENSAGEM"

try:
    client.sendto(msg.encode(), (target_host, target_port))  # conectando client ao target
    response = client.recvfrom(4096)
    print(response)
except:
    print("Falha na conexao")
    exit()


import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET-->IPV4, SOCK_STREAM-->TCP
client.settimeout(3)
target_host = ""
target_port = 80
msg = "GET / HTTP/1.1\nHost: example.com\n\n"

try:
    client.connect((target_host, target_port))  # conectando client ao target
    client.send(msg.encode())
    response = client.recv(4096)
    print(response.decode())
except:
    print("Falha na conexao")
    exit()


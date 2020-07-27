import paramiko

host = 'ip'
port = 22
user = 'username'
passwd = 'password'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(host, username=user, password=passwd)

while True:
    cmd = input('#')
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.readlines())
    print(stderr.readlines())

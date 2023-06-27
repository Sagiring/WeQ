import socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('10.21.237.247',16666))
client_socket.send(b'login\r\n\r\n{"user":"Ming","passwd":"123446"}')
print(client_socket.recv(5))
import socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('10.21.155.104',16666))
client_socket.send(b'register\r\n\r\n{"user":"Ming","passwd":"123456"}')
print(client_socket.recv(5))
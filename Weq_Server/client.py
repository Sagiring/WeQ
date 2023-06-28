import socket
import time
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('10.21.155.104',16666))

# client_socket.send(b'login\r\n\r\n{"user":"Ming","passwd":"123456"}')
# time.sleep(1)
# print(client_socket.recv(1024))
# client_socket.send(b'getFriends\r\n\r\n{"user":"Ming"}')
# print(client_socket.recv(1024))
# client_socket.send(b'getAllusers\r\n\r\n{"user":"Ming"}')
# print(client_socket.recv(1024))
client_socket.send(b'deleteFriend\r\n\r\n{"user":"Ming","friend":"xiaoming"}')
print(client_socket.recv(5))
# client_socket.send(b'close\r\n\r\n{"user":"Ming"}')
# print(client_socket.recv(5))
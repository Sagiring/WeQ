import socket
import time
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('10.21.237.247',16666))

client_socket.send(b'login\r\n\r\n{"user":"Ming","passwd":"123456"}')
# print(client_socket.recv(5))

# print(client_socket.recv(1024))
client_socket.send(b'getFriends\r\n\r\n{"user":"Ming"}')
# print(client_socket.recv(1024))
client_socket.send(b'getAllusers\r\n\r\n{"user":"Ming"}')
# # print(client_socket.recv(1024))
# client_socket.send(b'deleteFriend\r\n\r\n{"user":"Ming","friend":"xiaoming"}')
# print(client_socket.recv(5))
# client_socket.send(b'close\r\n\r\n{"user":"Ming"}')
# print(client_socket.recv(5))
# client_socket.send(b'addPubkey\r\n\r\n{"user":"Ming","pubkey":"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwbWjxcf18824JNK3xU/j\nDCcnIlsuUB5nMZYqhyEzp2cWrlzlwyxLiWvn8J3z7nS74ygvYWrnq1bHGjFyw5Ya\n8vSZc09Txgct3cuVjLzPHGySEKeqiVCj1F82AXAgUlGnW33MtMLmCyMIcbLMC5dK\n+LqKBBswgZ7O7EVvPo7ComU1bsSi0klnqDWEQUcoCzqoS9ucDQWoMsRtkJjGAYcK\n/MxwLrVuz+GiyR0ooNPNMJTW1a8siJ38i6C0uIk4/O17dufMz5L6/EsngSi3m90q\n5ssrsPFkp2msADctDbQqEpkFQAF9T3wl2hDFeXXW8gpO3BPfhwD/NNpv01mtBBo0\nsQIDAQAB\n-----END PUBLIC KEY-----"}')
# print(client_socket.recv(5))

client_socket.send(b'getPubkey\r\n\r\n{"user":"Ming","sendto":"Ming"}')
print(client_socket.recv(1024))
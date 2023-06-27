import socket
import threading
from log import Log
from login import Login
import json
_logger = Log()


def server():
    http_ip = 'localhost'
    addrs = socket.getaddrinfo(socket.gethostname(), None)
    for item in [addr[4][0] for addr in addrs]:
        if item[:2] == '10':
            http_ip = item
    http_port = 16666
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #                           地址簇 IPv4         使用TCP传输控制协议
    server_socket.bind((http_ip,http_port))
    server_socket.listen(5)
    _logger.i(f'服务器启动成功{http_ip}:{http_port}')
    _logger.i('监听中...')
    while 1:
        client_socket,addr = server_socket.accept() #阻塞进程无法退出
        _logger.i(f'已连接{addr}')
        msg = b''
        while 1:
            data = client_socket.recv(1024)
            msg += data
            if  len(data) < 1024:
                break

        msg = msg.decode()
        do_msg = threading.Thread(target=do_command,args=(msg,addr,client_socket))
        do_msg.start()

def do_command(msg:str,addr,client_socket):
    result = False
    action = {'login':Login.getLogin,
              'register':Login.getRegister,
              'addPubkey':Login.addPubkey,
              'getPubkey':Login.getPubkey
              }
    command = msg.split('\r\n\r\n')[0]
    if command not in action.keys():
        return False
    else:
        data = msg.split('\r\n\r\n')[1]
        print(data)
        data = json.loads(data)
        if command == 'login':
            result = action[command](data['user'],data['passwd'],addr)
            if result:
                client_socket.send(b'1\r\n\r\n')
            else:
                client_socket.send(b'0\r\n\r\n')

        elif command == 'register':
            result = action[command](data['user'],data['passwd'],data['email'])
            if result:
                client_socket.send(b'1\r\n\r\n')
            else:
                client_socket.send(b'0\r\n\r\n')

        elif command == 'addPubkey':
            result = action[command](data['user'],data['pubkey'])
            if result:
                client_socket.send(b'1\r\n\r\n')
            else:
                client_socket.send(b'0\r\n\r\n')

        elif command == 'getPubkey':
            result = action[command](data['user'],data['sendto'])
            if result:
                client_socket.send(result.encode('utf-8'))
            else:
                client_socket.send(b'0\r\n\r\n')

        return result
            

if __name__ == '__main__':
    server()




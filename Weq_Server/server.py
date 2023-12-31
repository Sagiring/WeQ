import socket
import threading
from log import Log
from login import Login
import json
import time
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
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    while 1:
        try:
            server_socket.bind((http_ip,http_port))
            break
        except OSError:
            _logger.i('端口冲突,3s后重试')
            time.sleep(3)
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
              'getPubkey':Login.getPubkey,
              'addFriend':Login.add_friend,
              'deleteFriend':Login.delete_friend,
              'getFriends':Login.get_friends,
              'getAllusers':Login.getAllusers,
              'close':Login.close
              }
    command = msg.split('\r\n\r\n')[0]
    if command not in action.keys():
        return False
    else:
        data = msg.split('\r\n\r\n')[1]
        _logger.i(command+'--->'+data)
        data = json.loads(data,strict=False)
        try:
            if command == 'login':
                result = action[command](data['user'],data['passwd'],addr)
            elif command == 'register':
                result = action[command](data['user'],data['passwd'],data['email'])
            elif command == 'addPubkey':
                result = action[command](data['user'],data['pubkey'])
            elif command == 'close':
                user = Login.getUser(data['user'])
                if user:
                    if user.addr[0] == addr[0]:
                        user.close()
                        result = True
                    else:
                        result = False
            elif command == 'addFriend' or command == 'deleteFriend':
                result = action[command](data['user'],data['friend'],addr)

            elif command == 'getAddr':
                result = action[command](data['user'],data['getUser'])
                if result:
                    result = {data['getUser']:str(result)}
                    result = '1\r\n\r\n' + json.dumps(result)
                    client_socket.send(result.encode('utf-8'))
                return result
                    
            elif command == 'getPubkey':
                pubkey = action[command](data['user'],data['sendto'])
                aeskey = Login.getSessionkey(data['user'])
                if aeskey and pubkey:
                    result = {"pubkey": pubkey,
                            "sessionkey": aeskey}
                    result = '1\r\n\r\n' + json.dumps(result)
                    client_socket.send(result.encode('utf-8'))
                else:
                    client_socket.send(b'0\r\n\r\n')
                client_socket.close()
                return aeskey
            

            elif command == 'getFriends':
                users = action[command](data['user'])
                if users != False:
                    result = '1\r\n\r\n' + json.dumps(users)
                else:
                    result ='0\r\n\r\n'
                client_socket.send(result.encode('utf-8'))
                return result


            elif  command == 'getAllusers':
                users = action[command](data['user'])
                if users != False:
                    users_list = []
                    for item in users:
                        users_list.append(item[0])
                    users = ','.join(list(set(users_list)))
                    result = {"user":users}
                    result = '1\r\n\r\n' + json.dumps(result)
                else:
                    result ='0\r\n\r\n'
                client_socket.send(result.encode('utf-8'))
                return result

            if result:
                client_socket.send(b'1\r\n\r\n')
            else:
                client_socket.send(b'0\r\n\r\n')
            client_socket.close()
            return result
        except Exception as e:
            client_socket.send(b'ServerError '+ str(e).encode())
            print(e)
        

if __name__ == '__main__':
    server()




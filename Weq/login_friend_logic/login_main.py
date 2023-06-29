import socket
import hashlib
import json
import re
from Crypto import Random
from Crypto.PublicKey import RSA



def register(username,password,email):
    k=check_password(password)
    md=hashlib.md5(password.encode('utf-8'))
    md=md.hexdigest()
    request = { "user": username, "passwd": md, "email": email}
    if k == 2:
        print('密码格式错误')
    command = 'register\r\n\r\n'
    request_register = command + json.dumps(request)
    response_register = send_msg(request_register.encode())  # 发送消息给服务器
    if response_register[0] == '0':
        print("该用户名已被注册！")
        return  False
    else:
        print("注册成功！")
        return  True

def login(username,passwd):
    md = hashlib.md5(passwd.encode('utf-8'))
    md=  md.hexdigest()
    request = {"user": username, "passwd": md}
    command = 'login\r\n\r\n'
    request_login = command + json.dumps(request)
    response_login = send_msg(request_login.encode())  # 发送消息给服务器
    # print(response_login)
    if response_login[0] == '0':
        print("用户名或密码错误！")
        return False
    else:
        print("登录成功！")
        return True


def addPubkey(username):
    Pubkey, Privkey = createkey()
    t={ "user": username, "pubkey": Pubkey.decode()}
    command='addPubkey\r\n\r\n'
    request = command + json.dumps(t)
    while True:
        response_pubkey = send_msg(request.encode())  # 发送消息给服务器
        if response_pubkey[0] == '0':
            print("公钥添加失败！")
            return False
        else:
            print("公钥添加成功！")
            return Privkey

def close(username):
    t={"user": username}
    command='close\r\n\r\n'
    request = command + json.dumps(t)
    response_close = send_msg(request.encode())  # 发送消息给服务器
    if response_close[0] == '0':
        print("退出失败！")
        return False
    else:
        print("退出成功！")
        return True


def check_password(password):
    result = re.compile(r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*.?]+$)[a-zA-Z\d!@#$%.?^&*]+$')
    if re.fullmatch(result, password):
        k=1
    else:
        k=2
    return k

def createkey():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    # 生成私钥
    private_key = rsa.exportKey()
    # 生成公钥
    public_key = rsa.publickey().exportKey()


    return public_key,private_key



def send_msg(msg:bytes):
    host = "10.21.237.247"  # 服务器 IP 地址
    port = 16666  # 端口号
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 TCP 套接字
    client_socket.connect((host, port))  #
    client_socket.send(msg)
    recv = client_socket.recv(1024).decode()
    client_socket.close()
    return recv







import socket
import hashlib
import json
import re
from Crypto import Random
from Crypto.PublicKey import RSA

def register():
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    email= input("请输入邮箱地址：")
    k=check_password(password)
    md=hashlib.md5(password.encode('utf-8'))
    md=md.hexdigest()
    request = { "user": username, "passwd": md, "email": email}
    return request,k

def login():
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    md = hashlib.md5(password.encode('utf-8'))
    md=  md.hexdigest()
    request = {"user": username, "passwd": md}
    return request

def addPubkey(username):
    Pubkey, Privkey = createkey()
    t={ "user": username, "pubkey": Pubkey.decode()}
    command='addPubkey\r\n\r\n'
    request = command + json.dumps(t)
    return  request

def close(username):
    t={"user": username}
    command='close\r\n\r\n'
    request = command + json.dumps(t)
    return  request


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

def address_book():
    username = input("请输入用户名: ")
    request={"action1":action1,"action2":action2,"username":username}
    return request

def response_address(response):
    print('OK')

def save_state(response):
    state=''
    with open("friendstate.txt", "w") as file:
        file.write(state)


def send_msg(msg:bytes):
    host = "10.21.237.247"  # 服务器 IP 地址
    port = 16666  # 端口号
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 TCP 套接字
    client_socket.connect((host, port))  #
    client_socket.send(msg)
    recv = client_socket.recv(1024).decode()
    client_socket.close()
    return recv
    

    
if __name__ == "__main__":
    while True:
        action = input("请选择操作（register/login/exit）：")
        request={}
        if action == "exit":
            break

        if action == "register":
            t=register()
            if t[1]==2:
                print('密码格式错误')
                continue
            command='register\r\n\r\n'
            request_register=command+json.dumps(t[0])
            response_register = send_msg(request_register.encode())# 发送消息给服务器
            if response_register[0] == '0':
                print("该用户名已被注册！")
                continue
            else:
                print("注册成功！")
                continue

        if action == "login":
            t=login()
            command='login\r\n\r\n'
            request_login=command+json.dumps(t)
            response_login = send_msg(request_login.encode())# 发送消息给服务器
            # print(response_login)
            if response_login[0] == '0':
                print("用户名或密码错误！")
                continue
            else:
                print("登录成功！")
                request_pubkey = addPubkey(t["user"])
                # print(request_pubkey)
                while True:
                    response_pubkey = send_msg(request_pubkey.encode())  # 发送消息给服务器
                    if response_pubkey[0] == '0':
                        print("公钥添加失败！")
                        continue
                    else:
                        print("公钥添加成功！")
                        break
            while True:
                action1 = input("请选择操作（address book/chat/exit）：")
                if action1=='exit':
                    break
                if action1=='address book':
                    action2 = input("请选择操作（add/delete/exit）：")
                    operation=address_book()
                    response_address_book = send_msg(json.dumps(operation).encode())  # 发送消息给服务器
                    response_address(response_address_book)
                if action1=='chat':
                    break

            while True:
                request_close=close(t.get("user"))
                response_close = send_msg(request_close.encode())  # 发送消息给服务器
                if response_close[0] == '0':
                    print("退出失败！")
                    continue
                else:
                    print("退出成功！")
                    break


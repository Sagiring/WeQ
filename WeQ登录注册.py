import socket
import hashlib
import json
import re
import threading
import sys
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



def friend(username):
    username_friend = input("请输入好友用户名: ")
    request={"user":username,"friend":username_friend}
    return request

def addFriend(username):
    k = friend(username)
    command = 'addFriend\r\n\r\n'
    request_addfriend = command + json.dumps(k)
    response_addfriend = send_msg(request_addfriend.encode())# 发送消息给服务器
    if response_addfriend[0] == '0':
        print("该用户名已在通讯录中！")
    else:
        print("通讯录添加成功！")
        getFriends(t.get("user"))

def deleteFriend(username):
    k = friend(username)
    command = 'deleteFriend\r\n\r\n'
    request_deletefriend = command + json.dumps(k)
    response_detelefriend = send_msg(request_deletefriend.encode()) # 发送消息给服务器
    if response_detelefriend[0] == '0':
        print("用户名删除失败！")
    else:
        print("用户名删除成功！")
        getFriends(t.get("user"))

def getFriends(username):
    k = {"user": username}
    command = 'getFriends\r\n\r\n'
    request_getfriends = command + json.dumps(k)
     # 发送消息给服务器
    response_getfriends = send_msg(request_getfriends.encode()) # 接收服务器的响应
    if response_getfriends[0] == '0':
        print("通讯录返回失败！")
    else:
        print("通讯录返回成功！")
        friendsfile(request_getfriends)

def getonlinefriends(username):
    k = {"user": username}
    command = 'getAllusers\r\n\r\n'
    request_getallusers = command + json.dumps(k)
    # 发送消息给服务器
    response_getallusers = send_msg(request_getallusers.encode())  # 接收服务器的响应
    if response_getallusers[0] == '0':
        print("在线列表返回失败！")
    else:
        print("在线列表返回成功！")
        usersfile(response_getallusers)
        online_friends_list("friendsfile.txt","usersfile.txt")


def friendsfile(response):
    data = response

    # 通过分割字符串获取 JSON 数据部分
    json_data = data.split('\r\n\r\n')[1]
    if json_data=='':
        with open("friendsfile.txt", "wb") as file:
            file.write(''.encode())
    else:
        if json_data[-1]!='}':
            json_data=json_data[-2]
    # 解析 JSON 数据
        parsed_data = json.loads(json_data)

        # 提取用户名
        username = parsed_data['user']

        with open("friendsfile.txt", "wb") as file:
            file.write(username.encode())

def usersfile(response):
    data = response
    json_data = data.split('\r\n\r\n')[1]
    if json_data== '':
        with open("usersfile.txt", "wb") as file:
            file.write(''.encode())
    else:
        # 解析 JSON 数据
        if json_data[-1]!='}':
            json_data=json_data[-2]
        print(json_data)
        parsed_data = json.loads(json_data)

        # 提取用户名
        username = parsed_data['user']

        with open("usersfile.txt", "wb") as file:
            file.write(username.encode())

def online_friends_list(a,b):
    # 读取第一个文件的数据
    with open(a, "r") as file1:
        data1 = set(file1.read().splitlines())

    # 读取第二个文件的数据
    with open(b, "r") as file2:
        data2 = set(file2.read().splitlines())

    # 取交集
    intersection = data1.intersection(data2)
    # 写交集数据
    with open("online_friends_list.txt", "wb") as file:
        for item in intersection:
            file.write(item.encode())

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
            sys.exit()
        if action == "register":
            t=register()
            if t[1]==2:
                print('密码格式错误')
                continue
            command='register\r\n\r\n'
            request_register=command+json.dumps(t[0])
            response_register = send_msg(request_register.encode())  #  发送消息给服务器
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
            if response_login[0] == '0':
                print("用户名或密码错误！")
                continue
            else:
                print("登录成功！")
                request_pubkey = addPubkey(t.get("user"))
                while True:
                    response_pubkey = send_msg(request_pubkey.encode())# 发送消息给服务器
                    if response_pubkey[0] == '0':
                        print("公钥添加失败！")
                        continue
                    else:
                        print("公钥添加成功！")
                        break
            getFriends(t.get("user"))
            # 创建一个线程用于发送请求x
            getonlinefriends(t.get("user"))

            request_thread = threading.Timer(300,getonlinefriends,args=t.get("user"))
            # 启动请求线程
            request_thread.start()
            while True:
                action1 = input("请选择操作（addfriend/deletefriend/getfriends/getonlinefriends/chat/exit）：")
                if action1 == 'exit':
                    request_close = close(t.get("user"))
                    response_close = send_msg(request_close.encode())  # 发送消息给服务器
                    if response_close[0] == '0':
                        print("退出失败！")
                        continue
                    else:
                        print("退出成功！")
                        break
                if action1 == 'addfriend':
                    addFriend(t.get("user"))
                    continue
                if action1 == 'deletefriend':
                    deleteFriend(t.get("user"))
                    continue
                if action1 == 'getfriends':
                    getFriends(t.get("user"))
                    continue
                if action1 == 'getonlinefriends':
                    getonlinefriends(t.get("user"))
                    continue
                if action1 == 'chat':
                    break





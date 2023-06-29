import socket
import json



def addFriend(username,friendname):
    k = {"user":username,"friend":friendname}
    command = 'addFriend\r\n\r\n'
    request_addfriend = command + json.dumps(k)
    response_addfriend = send_msg(request_addfriend.encode())# 发送消息给服务器
    if response_addfriend[0] == '0':
        print("该用户名已在通讯录中！")
        return False
    else:
        print("通讯录添加成功！")
        return True

def deleteFriend(username,friendname):
    k = {"user":username,"friend":friendname}
    command = 'deleteFriend\r\n\r\n'
    request_deletefriend = command + json.dumps(k)
    response_detelefriend = send_msg(request_deletefriend.encode()) # 发送消息给服务器
    if response_detelefriend[0] == '0':
        print("用户名删除失败！")
        return False
    else:
        print("用户名删除成功！")
        return True

def getFriends(username):
    k = {"user": username}
    command = 'getFriends\r\n\r\n'
    request_getfriends = command + json.dumps(k)
     # 发送消息给服务器
    response_getfriends = send_msg(request_getfriends.encode()) # 接收服务器的响应
    if response_getfriends[0] == '0':
        print("通讯录返回失败！")
        return False
    else:
        print("通讯录返回成功！")
       
        return friendstuple(response_getfriends)


def friendstuple(response):
    data = response

    # 通过分割字符串获取 JSON 数据部分
    json_data = data.split('\r\n\r\n')[1]

    # 解析 JSON 数据
    parsed_data = json.loads(json_data)

    # 构建元组
    result = [(key,) + tuple(value.strip('()').replace('\'', '').split(', ')) for key, value in parsed_data.items()]

    return result

def send_msg(msg:bytes):
    host = "10.21.237.247"  # 服务器 IP 地址
    port = 16666  # 端口号
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 TCP 套接字
    client_socket.connect((host, port))  #
    client_socket.send(msg)
    recv = client_socket.recv(1024).decode()
    client_socket.close()
    return recv









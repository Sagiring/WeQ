import socket
import hashlib
import json
import re
import base64
from Crypto import Random
from Crypto.PublicKey import RSA
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def register(username,password,email):
    k=check_password(password)
    if k == 2:
        print('密码格式错误')
        return False
    md=hashlib.md5(password.encode('utf-8'))
    md=md.hexdigest()
    c=checkemail(email)
    if c == 2:
        print('邮箱格式错误')
        return False
    r=mailverification(email)
    if r==2:
        print('邮箱验证失败')
        return False
    request = { "user": username, "passwd": md, "email": email}
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

def checkemail(address):
    """
    利用正则表达式检测邮箱格式
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex,address):
        t=1
    else:
        t=2
    return  t

def generate_verification_code():
    code = random.randint(100000, 999999)
    return str(code)

def create_email_message(code):
    body = f'您的验证码是: {code}'

    return body


def send_email(address,email_message):
    smtp_server = 'smtp.qq.com'  # 你的邮件服务器地址
    smtp_port = 25  # 邮件服务器端口号
    sender_email = '498618798@qq.com'  # 你的邮箱地址
    sender_password = 'ueaoenpgwgdgbjcg'  # 你的邮箱密码
    recipient_email=address
    subject = '验证码'

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((smtp_server, smtp_port))

            # 接收服务器返回的连接信息
            response = client_socket.recv(1024).decode()
            print(response)

            ehlo = "ehlo smtp.qq.com\r\n"
            client_socket.send(ehlo.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            auth = f"auth login\r\n"
            client_socket.send(auth.encode())



            auth = f"{base64.b64encode(bytes(sender_email, 'utf-8')).decode('utf-8')}\r\n"
            client_socket.send(auth.encode())


            auth = f"{base64.b64encode(bytes(sender_password, 'utf-8')).decode('utf-8')}\r\n"
            client_socket.send(auth.encode())



            # 发送发件人信息
            mail_from_command = f'mail from: <{sender_email}>\r\n'
            client_socket.send(mail_from_command.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            # 发送收件人信息
            rcpt_to_command = f'rcpt to: <{recipient_email}>\r\n'
            client_socket.send(rcpt_to_command.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            # 发送数据命令
            data_command = 'data\r\n'
            client_socket.send(data_command.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            From = f"From: <{sender_email}>\r\n"
            client_socket.send(From.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            To = f"To: <{recipient_email}>\r\n"
            client_socket.send(To.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            Subject = f"Subject: {subject}\r\n\r\n"
            client_socket.send(Subject.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            Message = f"{email_message}\r\n"
            client_socket.send(Message.encode())
            response = client_socket.recv(1024).decode()
            print(response)

            end = ".\r\n"
            client_socket.send(end.encode())
            response = client_socket.recv(1024).decode()
            print(response)


            # 断开连接
            quit_command = 'QUIT\r\n'
            client_socket.send(quit_command.encode())
            response = client_socket.recv(1024).decode()
            print(response)

        print('邮件发送成功')
        return True
    except Exception as e:
        print('邮件发送失败:', str(e))
        return False


def mailverification(address):
    verification_code = generate_verification_code()
    email_message = create_email_message(verification_code)
    r = 2
    s=send_email(address,email_message)
    if s:
        receive_code=input("请输入验证吗：")
        if receive_code==verification_code:
            r=1
        else:
            r=2
    return r








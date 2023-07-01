import socket
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

class KeyDistribution:

    _All_session_key = {}

    def __init__(self, key,port = 6666):
        self.session_key = b''
        self.rsa_public_key = ''
        self.rsa_private_key = key
        selfip = KeyDistribution.get_selfip()
        self.ip = selfip

        self.port = port

    def get_session_key_from_server(self, sender, receiver):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('10.21.237.247', 16666))
        send_data = {
            'user': sender,
            'sendto': receiver
        }
        send_data = json.dumps(send_data)
        client.send(f'getPubkey\r\n\r\n{send_data}'.encode('utf-8'))
        recv_data = client.recv(1024).decode('utf-8').replace('\r\n', '')
        if recv_data[0] == '0':
            print('获取失败')
            client.close()
        else:
            # print(recv_data)
            recv_data = json.loads(recv_data[1:])
            self.rsa_public_key = recv_data['pubkey']
            session_key = base64.b64decode(recv_data['sessionkey'])
            key = RSA.importKey(self.rsa_private_key)
            cipher = PKCS1_cipher.new(key)
            self.session_key = cipher.decrypt(session_key, 0)
            # print(self.rsa_public_key)
            # print(self.session_key)
            client.close()
        

    def send_session_key_to_peer(self, friend_ip, port = 6666):
        session_key = self.session_key
        pub_key = self.rsa_public_key

        key = RSA.importKey(pub_key)
        cipher = PKCS1_cipher.new(key)
        msg = base64.b64encode(cipher.encrypt(session_key))

        data = {
            "msg": msg.decode('utf-8'),
            "ip": self.ip,
            "port": self.port,
            "action": "chat"
        }

        data = json.dumps(data)
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((friend_ip, port))
        sk.connect((friend_ip, port))
        sk.send(data.encode('utf-8'))
        sk.close()
        selfip = self.ip
        if selfip < friend_ip:
            selfip,friend_ip = friend_ip,selfip
        KeyDistribution._All_session_key[f'{selfip},{friend_ip}'] = self.session_key
        return self.session_key

    @staticmethod
    def get_session_key_from_peer(priv_key,data,addr):
        friend_ip = addr[0]
        selfip = KeyDistribution.get_selfip()
        if selfip < friend_ip:
            selfip,friend_ip = friend_ip,selfip
        data = base64.b64decode(data['msg'])
        key = RSA.importKey(priv_key)
        cipher = PKCS1_cipher.new(key)
        data = cipher.decrypt(data, 0)
        
        KeyDistribution._All_session_key[f'{selfip},{friend_ip}'] = data
        return data
    
    @staticmethod
    def get_session_key(friend_ip):
        selfip = KeyDistribution.get_selfip()
        if selfip < friend_ip:
            selfip,friend_ip = friend_ip,selfip
        for item in KeyDistribution._All_session_key.keys():
                if f'{selfip},{friend_ip}' == item:
                    return KeyDistribution._All_session_key[item]
        else:
            return False
        
    @staticmethod
    def pop_session_key(friend_ip):
        selfip = KeyDistribution.get_selfip()
        
        if selfip < friend_ip:
            selfip,friend_ip = friend_ip,selfip
        for item in list(KeyDistribution._All_session_key.keys()):
                if f'{selfip},{friend_ip}' == item:
                    KeyDistribution._All_session_key.pop(item)
                    print('本次密钥已删除')

    @staticmethod
    def get_selfip():
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in [addr[4][0] for addr in addrs]:
            if item[:2] == '10':
                selfip = item
        return selfip




import socket
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

class KeyDistribution:
    def __init__(self, ip, port, key):
        self.session_key = b''
        self.rsa_public_key = ''
        self.rsa_private_key = key
        self.ip = ip
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
            recv_data = json.loads(recv_data[1:])
            self.rsa_public_key = recv_data['pubkey']
            session_key = base64.b64decode(recv_data['sessionkey'])
            key = RSA.importKey(self.rsa_private_key)
            cipher = PKCS1_cipher.new(key)
            self.session_key = cipher.decrypt(session_key, 0)
            # print(self.rsa_public_key)
            # print(self.session_key)
            client.close()

    def send_session_key_to_peer(self, ip, port):
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
        sk.connect((ip, port))
        sk.send(data.encode('utf-8'))
        sk.close()

    def get_session_key_from_peer(self, data):
        priv_key = self.rsa_private_key
        data = base64.b64decode(data)
        key = RSA.importKey(priv_key)
        cipher = PKCS1_cipher.new(key)
        data = cipher.decrypt(data, 0)
        self.session_key = data

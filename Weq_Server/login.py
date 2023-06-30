from sql_splite3 import *
import random
import string
from Crypto.Cipher  import PKCS1_v1_5 as PKCS1_cipher
import base64
from Crypto.PublicKey import RSA



class Login:
    __ALL_User = {}
    
    def __init__(self,username:str,addr) -> None:
        self.username = username
        self.addr = addr
        self.pubkey = ''
        Login.__ALL_User[username] = self



    @staticmethod
    def getLogin(username:str,passwd:str,addr):
        result = sqlLogin([username,passwd])
        if result:
            Login(username,addr)
        return result
    
    @staticmethod       
    def getRegister(username:str,passwd:str,email:str):
        return sqlRegister([username,passwd,email])

    @staticmethod
    def addPubkey(username:str,pubkey:str):
        if username in Login.__ALL_User.keys():
            Login.__ALL_User[username].pubkey = pubkey
            return True
        else:
            return False
    
    @staticmethod
    def getPubkey(username:str,sendto:str):
        if username in Login.__ALL_User.keys():
            return Login.__ALL_User[sendto].pubkey
        else:
            return False
    
    @staticmethod
    def getSessionkey(username):
        all_char_set = string.printable
        all_char_set*=16
        key =''.join(random.sample(all_char_set,k=16))
        user = Login.getUser(username)
        if user:
            public_key = user.pubkey
            pubkey = RSA.importKey(public_key)
            all_char_set = string.printable
            all_char_set*=16
            key =''.join(random.sample(all_char_set,k=16))
            cipher = PKCS1_cipher.new(pubkey)
            encrypto_key = base64.b64encode(cipher.encrypt(key.encode('utf-8')))
            # print(encrypto_key.decode('utf-8'))
            return encrypto_key.decode('utf-8')
        else:
            return False
    
    
    @staticmethod
    def getUser(username):
        if username in Login.__ALL_User.keys():
            return Login.__ALL_User[username]
        else:
            return False
        
    @staticmethod
    def getAllusers(username):
        user_str = []
        if Login.getUser(username):
            for user in Login.__ALL_User.keys():
                user_str.append((user,))
            return user_str
        else:
            return False

    @staticmethod
    def add_friend(username,friend_id,addr):
        user = Login.getUser(username)
        result = False
        if user:
            if addr[0] == user.addr[0]:
                result  = sql_add_friend(username,friend_id)
        return result
                

    @staticmethod
    def delete_friend(username,friend_id,addr):
        user = Login.getUser(username)
        result = False
        if user:
            if addr[0] == user.addr[0]:
                result  = sql_delete_friend(username,friend_id)
        return result

    @staticmethod
    def get_friends(username):
        user = Login.getUser(username)
        result = False
        friend_list  = {}
        if user:
            result = sql_get_friend(username)  
            for user in result:
                Addr = Login.getAddr(user[0])
                friend_list[user[0]] = str(Addr)

        return friend_list 
    
    @staticmethod
    def getAddr(getUser):
        user = Login.getUser(getUser)
        if user:
            return user.addr
        return(0,0)
 

    def close(self):
        Login.__ALL_User.pop(self.username)
        return True

    





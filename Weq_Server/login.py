from sql_splite3 import *
import random
import string
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
        if username in Login.__ALL_User.keys():
            return Login.__ALL_User[username]
        else:
            result = sqlLogin([username,passwd])
            if result:
                Login(username,addr)
            else:
                return False
            
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
    def getSessionkey():
        all_char_set = string.printable
        all_char_set*=16
        key =''.join(random.sample(all_char_set,k=16))
        return key
    
    @staticmethod
    def getUser(username):
        if username in Login.__ALL_User.keys():
            return Login.__ALL_User[username]
        else:
            return False

    def close(self):
        Login.__ALL_User.pop(self.username)
        return True

    





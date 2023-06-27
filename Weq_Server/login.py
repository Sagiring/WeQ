from sql_splite3 import *

class Login:
    __ALL_User = {}
    port = 66666
    def __init__(self,username:str,addr) -> None:
        self.username = username
        self.addr = addr
        self.pubkey = ''
        Login.__ALL_User[username] = self



    @staticmethod
    def getLogin(username:str,passwd:str,addr):
        if username in Login.__ALL_User.keys():
            return True
        else:
            result = sqlLogin([username,passwd])
            if result:
                Login(username,addr)
            else:
                return False
            
    @staticmethod       
    def getRegister(username:str,passwd:str):
        return sqlRegister([username,passwd])

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






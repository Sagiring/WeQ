# import json
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import threading
import traceback
import time
BLOCK_SIZE = 16
from ..log import Log
_logger = Log()

class Client:
    def __init__(self,session_key ,port = 8888):
        self.session_key = session_key
        self.server_port = port
        self.send_port = port
        self.isFisrt = threading.Event()
        self.isFisrt.set()
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in [addr[4][0] for addr in addrs]:
            if item[:2] == '10':
                ip = item
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        while 1:
            try:
                self.server.bind((ip, port))
                _logger.i(f'会话在端口为{port}监听')
                self.server_port = port
                break
            except OSError:
                _logger.i(f'端口冲突正在重试')
                time.sleep(0.1)
                port += 1
        self.server.listen(1)
        # _logger.i(f'recv_port:{self.server_port}')

    def __del__(self):
        self.server.close()

    def send_msg(self, recv_ip, msg,isByte = False):
       
        port = self.send_port
        if msg[:len('correct1\r\n')] != 'correct1\r\n' and msg != 'correct2\r\n':
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            key = self.session_key
            # self.send_port = 8888
            cipher = AES.new(key, AES.MODE_ECB)
            if isByte:
                msg = cipher.encrypt(pad(msg, BLOCK_SIZE))
            else:
                msg = cipher.encrypt(pad(msg.encode('utf-8'), BLOCK_SIZE))
           
            while 1:
                # try:
                    conn.connect((recv_ip,port))
                    self.send_port = port
                    break
                # except ConnectionRefusedError:
                #     time.sleep(0.1)
                #     port += 1
            # _logger.i((str(len(msg))).encode())
            # _logger.i(f'send_port:{self.send_port}')
            conn.send((str(len(msg))).encode()+ b'\r\n\r\n' + msg)
        else:
            if msg[:len(b'correct1\r\n')] == 'correct1\r\n' :
                
                while self.isFisrt.is_set():
                    try:
                        _logger.d(f'循环标志位为{self.isFisrt.is_set()}')
                        _logger.i(f'正在检查对方端口{self.send_port}')
                        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socket.setdefaulttimeout(1)
                        conn.connect((recv_ip,self.send_port))
                        conn.settimeout(1)
                        conn.send((str(len(msg))).encode()+ b'\r\n\r\n' +msg.encode())
                        time.sleep(1.5)

                    except ConnectionRefusedError:
                        time.sleep(0.1)
                        self.send_port += 1
                    except TimeoutError:
                        time.sleep(0.1)
                        self.send_port += 1
                    except OSError:
                        conn.close()
                        self.send_port += 1
                        if self.send_port > 9000:
                            self.send_port = 8888
                _logger.i(f'已确认对方端口号为{self.send_port}')
            else:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                while 1:
                    try:
                        conn.connect((recv_ip,self.send_port))
                        break
                    except TimeoutError:
                        time.sleep(0.5)
                conn.send((str(len(msg))).encode()+ b'\r\n\r\n' +msg.encode())
                conn.close()
                _logger.i(f'已收到握手请求,正在确认')

                
                    
        



    def recv_msg(self,isByte = True):
            
            try:
                conn, addr = self.server.accept()
                data = conn.recv(1024)
                # _logger.i(data.split(b'\r\n\r\n')[0])
                dataLen = int(data.split(b'\r\n\r\n')[0].decode())
                msg = data.split(b'\r\n\r\n')[1]
                Len = len(msg)
                while 1:
                    if  Len >= dataLen:
                        break
                    data = conn.recv(4096)
                    msg += data
                    Len += len(data)
                    
                if msg[:len(b'correct1\r\n')] != b'correct1\r\n' and msg != b'correct2\r\n':
                    # _logger.i(len(msg))
                    key = self.session_key
                    cipher = AES.new(key, AES.MODE_ECB)
                    if isByte:
                        msg = unpad(cipher.decrypt(msg), BLOCK_SIZE)
                    else:
                        msg = unpad(cipher.decrypt(msg), BLOCK_SIZE).decode('utf-8', errors='ignore')
                    return msg,conn,self.server
                else:
                    # msg = conn.recv(len(b'correct2\r\n'))
                    if msg == b'correct2\r\n':
                        _logger.i('已收到对方握手确认')
                        socket.setdefaulttimeout(None)
                        conn.settimeout(None)
                        self.isFisrt.clear()
 
                    return msg,conn,self.server
            except TimeoutError:
                pass
            except Exception as e:
                _logger.e(e)
                traceback.print_exc()


    def get_server_port(self):
        return self.server_port
    
    
    def modify_send_port(self,send_port):
        self.send_port = send_port
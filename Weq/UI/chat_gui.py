from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox
from ..client import KeyDistribution,Client
import threading
import time



class ChatGUI(tk.Toplevel):
    def __init__(self, parent, current_user, messages,friend,pri_key):
        super().__init__(parent)
        self.title("聊天界面")
        self.geometry("500x400")
        self.friend = friend
        self.pri_key = pri_key
        
        self.current_user = current_user
        self.messages = messages

        self.max_image_width = 400  # 设置图片的最大宽度
        self.max_image_height = 300  # 设置图片的最大高度
        Session = KeyDistribution.get_session_key(friend_ip = friend.ip)
        if Session:
            self.Session_key = Session
        else:
            Distributer = KeyDistribution(pri_key)
            Distributer.get_session_key_from_server(current_user,friend.username)
            self.Session_key = Distributer.send_session_key_to_peer(friend.ip)

        self.client = Client(self.Session_key)
        recv_isRunning = threading.Event()
        recv_isRunning.set()
        self.recv_isRunning = recv_isRunning
        recv_threading = threading.Thread(target=self.recv_msg,args=(recv_isRunning,))
        recv_threading.start()


        self.create_widgets()  # 创建聊天界面的各个部件。
        self.load_messages()  # 加载显示聊天消息。
        self.protocol('WM_DELETE_WINDOW', self.close)


    def create_widgets(self):
        self.message_box = tk.Text(self) # 文本框显示消息
        self.message_box.pack(fill=tk.BOTH, expand=True)

        self.send_frame = tk.Frame(self) # 框架容纳发送消息
        self.send_frame.pack(fill=tk.X) # 水平填充窗口

        self.message_entry = tk.Entry(self.send_frame) #文本输入框
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.send_button = tk.Button(self.send_frame, text="发送消息", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.send_image_button = tk.Button(self.send_frame, text="发送图片", command=self.select_image)
        self.send_image_button.pack(side=tk.RIGHT, padx=5)

 

    # 处理发送消息的逻辑
    def send_message(self):
        message = self.message_entry.get() # 获取用户在文本输入框中输入的消息内容
        if message:
            message = 'msg\r\n' + message
            friend_ip = self.friend.ip
            self.client.send_msg(friend_ip,message)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 获取当前时间，并将其格式化为字符串表示
            message = message.split('\r\n')[1]
            self.add_message(self.current_user, timestamp, message)
            self.message_entry.delete(0, tk.END) # 清空文本输入框


    def recv_msg(self,event:threading.Event):
        while event.is_set():
            msg,recv_socket = self.client.recv_msg()
            try:
                msg = msg.decode()
            except UnicodeDecodeError:
                msg = msg[len(b'img\r\n'):]
                # image_data = base64.b64decode(msg)
                digits = 10
                time_stamp = time.time()
                digits = 10 ** (digits -10)
                time_stamp = int(round(time_stamp*digits))
                path = './img/'+str(time_stamp)+'.png'
                with open(path,'wb') as f:
                    f.write(msg)
                time.sleep(1)
                self.show_photo(path)
                return 0

            if msg.split('\r\n')[0] == 'msg':
                msg = msg.split('\r\n')[1]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 获取当前时间，并将其格式化为字符串表示
                self.add_message(self.friend.username, timestamp, msg)
            elif msg.split('\r\n')[0] == 'close':
                self.close()
                message = '\r\n'
                friendip = self.friend.ip
                self.client.send_msg(friendip, message)
                # msg = msg.split('\r\n')[1]
                # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # self.add_message(self.friend.username, timestamp, msg)
            elif msg.split('\r\n')[0] == 'close1':
                self.close1()
            elif msg.split('\r\n')[0] == 'ACK1':
                recv_socket.close()
                message = 'ACK2\r\n'
                friendip = self.friend.ip
                self.client.send_msg(friendip, message)
            elif msg.split('\r\n')[0] == 'ACK2':
                recv_socket.close()

    def close(self):
        self.recv_isRunning.clear()
        message = 'close1\r\n'
        friendip = self.friend.ip
        self.client.send_msg(friendip, message)
        self.destroy()

    def close1(self):
        self.recv_isRunning.clear()
        message = 'ACK1\r\n'
        friendip = self.friend.ip
        self.client.send_msg(friendip, message)
        messagebox.showinfo('提示', '对方终止了聊天')
        self.destroy()

    # 发送图片
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.send_image(file_path)

    def send_image(self, file_path):
        with open(file_path,'rb') as f:
            context = f.read()
        
        # image_str = base64.encodebytes(context).decode("utf-8")
        context = b'img\r\n' + context
        friend_ip = self.friend.ip
        self.client.send_msg(friend_ip,context,isByte=True)
        self.show_photo(file_path)

    def show_photo(self,file_path):
        # 加载选定的图片
        image = Image.open(file_path)
        # 调整图片大小
        resized_image = self.resize_image(image)
        # 将图片转换为PhotoImage对象
        photo = ImageTk.PhotoImage(resized_image)
        # 添加消息到消息列表
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_message(self.friend.username, timestamp, photo)

    # 将当前用户、时间戳和消息内容作为参数添加到消息列表中，并将消息显示在聊天界面中。
    def add_message(self, username, timestamp, content):
        self.messages.append((username, timestamp, content))
        if isinstance(content, str):
            self.message_box.insert(tk.END, f"[{timestamp}] {username}: {content}\n")
            self.message_box.insert(tk.END, "\n")  # 在文字下方添加空白距离
        else:
            self.message_box.insert(tk.END, f"[{timestamp}] {username}:\n")
            self.message_box.image_create(tk.END, image=content)
            self.message_box.insert(tk.END, "\n")  # 在图片下方添加空白距离

    def load_messages(self):
        for message in self.messages:
            username, timestamp, content = message
            if isinstance(content, str):
                self.message_box.insert(tk.END, f"[{timestamp}] {username}: {content}\n")
            else:
                self.message_box.insert(tk.END, f"[{timestamp}] {username}:\n")
                self.message_box.image_create(tk.END, image=content)
                self.message_box.insert(tk.END, "\n")  # 在图片下方添加空白距离

    #将图片调整为固定比例大小
    def resize_image(self, image):
        width, height = image.size
        # 计算缩放比例
        if width > self.max_image_width or height > self.max_image_height:
            ratio = min(self.max_image_width / width, self.max_image_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            # 缩放图片
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
            return resized_image
        else:
            return image

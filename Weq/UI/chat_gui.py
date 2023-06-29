from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from ..client import KeyDistribution,Client

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

        keyDis =  KeyDistribution(pri_key)
        keyDis.get_session_key_from_server(current_user,friend.username)
        keyDis.send_session_key_to_peer(friend.ip)


        self.create_widgets()  # 创建聊天界面的各个部件。
        self.load_messages()  # 加载显示聊天消息。

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
        friend_ip = self.friend.ip
        client = Client()
        client.send_msg(friend_ip,message)

        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 获取当前时间，并将其格式化为字符串表示
            # self.add_message(self.current_user, timestamp, message)
            self.message_entry.delete(0, tk.END) # 清空文本输入框




    # 发送图片
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.send_image(file_path)

    def send_image(self, file_path):
        # 加载选定的图片
        image = Image.open(file_path)
        # 调整图片大小
        resized_image = self.resize_image(image)
        # 将图片转换为PhotoImage对象
        photo = ImageTk.PhotoImage(resized_image)
        # 添加消息到消息列表
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_message(self.current_user, timestamp, photo)

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

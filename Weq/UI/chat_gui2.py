import tkinter as tk
from tkinter import filedialog
from datetime import datetime

class ChatGUI(tk.Toplevel):
    def __init__(self, parent, current_user, messages):
        super().__init__(parent)
        self.title("聊天界面")
        self.geometry("500x400")
        
        self.current_user = current_user
        self.messages = messages
        
        self.create_widgets()
        self.load_messages()
    
    def create_widgets(self):
        self.message_box = tk.Text(self)
        self.message_box.pack(fill=tk.BOTH, expand=True)
        
        self.send_frame = tk.Frame(self)
        self.send_frame.pack(fill=tk.X)
        
        self.message_entry = tk.Entry(self.send_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.send_button = tk.Button(self.send_frame, text="发送消息", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        self.send_image_button = tk.Button(self.send_frame, text="发送图片", command=self.select_image)
        self.send_image_button.pack(side=tk.RIGHT, padx=5)
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.add_message(self.current_user, timestamp, message)
            self.message_entry.delete(0, tk.END)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.send_image(file_path)
    
    def send_image(self, file_path):
        # 在这里处理发送图片的逻辑，例如上传图片到服务器或发送给聊天对象等
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_message(self.current_user, timestamp, f"发送了图片: {file_path}")
    
    def add_message(self, username, timestamp, content):
        self.messages.append((username, timestamp, content))
        self.message_box.insert(tk.END, f"[{timestamp}] {username}: {content}\n")
    
    def load_messages(self):
        for message in self.messages:
            username, timestamp, content = message
            self.message_box.insert(tk.END, f"[{timestamp}] {username}: {content}\n")

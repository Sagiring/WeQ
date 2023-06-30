import tkinter as tk
from tkinter import messagebox
from ..login_friend_logic import *
from .chat_gui import ChatGUI
# from PIL import Image, ImageTk
from tkinter import filedialog
import socket
import json
from ..client import KeyDistribution,LSB
import threading
import time

class Friend:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.online = False
        self.latest_message = ""
        self.unread_messages = 0

class FriendListGUI:
    def __init__(self,pri_key):
        self.friends = []  # 存储好友信息的列表
        self.current_user = None  # 当前用户的用户名

        self.root = tk.Toplevel()
        self.root.title("好友列表")
        self.root.geometry("480x400")
        self.pri_key = pri_key
        self.friend_frame = tk.Frame(self.root)
        self.friend_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.friend_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.friend_listbox = tk.Listbox(
            self.friend_frame,
            yscrollcommand=self.scrollbar.set,
            width=70
        )
        self.friend_listbox.pack()

        self.scrollbar.config(command=self.friend_listbox.yview)

        self.add_friend_button = tk.Button(
            self.root,
            text="添加好友",
            width=10,
            command=self.open_add_friend_dialog
        )
        self.add_friend_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.remove_friend_button = tk.Button(
            self.root,
            text="删除好友",
            width=10,
            command=self.open_remove_friend_dialog
        )
        self.remove_friend_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.remove_friend_button = tk.Button(
            self.root,
            text="解密图片",
            width=10,
            command=self.Decrypt_images
        )
        self.remove_friend_button.pack(side=tk.RIGHT, padx=30, pady=10)

        self.add_friend_button = tk.Button(
            self.root,
            text="加密图片",
            width=10,
            command=self.Encrypt_images
        )
        self.add_friend_button.pack(side=tk.LEFT, padx=30, pady=10)

        
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        isRunning = threading.Event()
        isRunning.set()
        self.isRunning = isRunning
        key_threading = threading.Thread(target=self.key_server)
        key_threading.start()
        refresh = threading.Thread(target=self.auto_fresh)
        refresh.start()

    def close(self):
        result = close(self.current_user)
        self.isRunning.clear()
        self.root.destroy()
        exit(0)
        

    def auto_fresh(self):
        while self.isRunning.is_set():
            time.sleep(3)
            self.refresh_friends()
            
        

    def key_server(self):
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in [addr[4][0] for addr in addrs]:
            if item[:2] == '10':
                ip = item
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, 6666))
        server.listen(5)
        while self.isRunning.is_set():
            conn, addr = server.accept()
            data = json.loads(conn.recv(4096).decode('utf-8'))
            print('已收到密钥')
            if data['action'] == 'chat':
                print('存储密钥')
                self.session_key = KeyDistribution.get_session_key_from_peer(self.pri_key,data,addr)
                for item in self.friends:
                    # print(item.ip)
                    # print(addr[0])
                    if item.ip == addr[0]:
                        item.unread_messages += 1
                        print('更新请求连接')
                self.refresh_friends()

    #加密信息
    def Encrypt_images(self):
        # 创建弹出页面
        encrypt_window = tk.Toplevel(self.root)
        encrypt_window.title("加密图片")
        encrypt_window.geometry("500x300")

        # 输入框
        input_entry = tk.Entry(encrypt_window)
        input_entry.pack(side=tk.LEFT, padx=10, pady=10)



        def crypto_photo(old_img):
            msg = input_entry.get()
            if msg:
                tail = old_img[old_img.find('.'):]
                new_img = './img/Encrypto'+ tail
                lsb = LSB(raw_img=old_img,new_img=new_img)
                lsb.hide_data(msg)
                return True

            else:
                return False

        # 加号符号
        def open_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
            if file_path:
                return crypto_photo(file_path)
            # if file_path:
            #     image = Image.open(file_path)
            #     image.thumbnail((200, 200))  # 缩放图片大小为合适的尺寸
            #     image_tk = ImageTk.PhotoImage(image)
            #     image_label.configure(image=image_tk)
            #     image_label.image = image_tk  # 保存对图片对象的引用
            #     filepath['file_path'] = file_path
                
           
        
        plus_label = tk.Label(encrypt_window, text="加密图片", cursor="hand2")
        plus_label.pack(side=tk.LEFT, padx=10)
        plus_label.bind("<Button-1>", lambda event: open_image())  # 绑定点击事件，调用open_image函数

     
        # 图片框
        # image_frame = tk.Frame(encrypt_window)
        # image_frame.pack(side=tk.LEFT, padx=10)

        # image_label = tk.Label(image_frame)
        # image_label.pack()


    

            
        # # 等号符号
        # equal_label = tk.Label(encrypt_window, text="加密图片",cursor="hand2")
        # equal_label.pack(side=tk.LEFT, padx=10)
        # plus_label.bind("<Button-2>", lambda event: crypto_photo(filepath["file_path"]))#这里的event还没添加

 

    # 解密信息
    def Decrypt_images(self):
        decrypt_window = tk.Toplevel(self.root)
        decrypt_window.title("解密图片")
        decrypt_window.geometry("500x300")
        
        # 创建滚动条
        scrollbar = tk.Scrollbar(decrypt_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 图片框
        image_frame = tk.Frame(decrypt_window)
        image_frame.pack(side=tk.TOP, padx=10, pady=10)
        
        image_label = tk.Label(image_frame)
        image_label.pack()

        # 添加图片按钮

        
        # file_path = {'file_path':''}
        def add_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;")])
           
            return file_path
            # if file_path:
            #     image = Image.open(file_path)
            #     image.thumbnail((200, 200))  # 缩放图片大小为合适的尺寸
            #     image_tk = ImageTk.PhotoImage(image)
            #     image_label.configure(image=image_tk)
            #     image_label.image = image_tk  # 保存对图片对象的引用
                # file_path['file_path'] = file_path
        
        # add_image_button = tk.Button(decrypt_window, text="添加图片", command=add_image)
        # add_image_button.pack(side=tk.LEFT, padx=10, pady=10)

        def get_information():
            # 在这里编写获取信息的逻辑
            file_path = add_image()
            if file_path:
                lsb = LSB(new_img=file_path)
                information =  lsb.get_data()
                #TODO
                # information_text.delete()
                information_text.insert(tk.END, information + "\n")


        get_info_button = tk.Button(decrypt_window, text="获取信息", command=lambda: get_information())
        get_info_button.pack(side=tk.LEFT, padx=10, pady=10)

        # 文本框用于输出信息
        information_text = tk.Text(decrypt_window, height=5, width=30)
        information_text.pack(side=tk.LEFT, padx=10, pady=10)

        # # 将滚动条与文本框关联
        # scrollbar.config(command=information_text.yview)
        # information_text.config(yscrollcommand=scrollbar.set)
        # # # 创建滚动条
        # # scrollbar = tk.Scrollbar(decrypt_window)
        # # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # # 创建全局滚动条
        # main_scrollbar = tk.Scrollbar(decrypt_window)
        # main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # # 将滚动条与文本框关联
        # scrollbar.config(command=information_text.yview)
        # information_text.config(yscrollcommand=scrollbar.set)
        # # 创建一个框架，用于容纳所有部件
        # main_frame = tk.Frame(decrypt_window)
        # main_frame.pack(padx=10, pady=10)
        # # 将主框架与滚动条关联
        # main_scrollbar.config(command=main_frame.yview)
        # main_frame.config(yscrollcommand=main_scrollbar.set)

    def open_add_friend_dialog(self):
        # 创建添加好友对话框
        add_friend_dialog = tk.Toplevel(self.root)
        add_friend_dialog.title("添加好友")
        add_friend_dialog.geometry("200x150")

        username_label = tk.Label(add_friend_dialog, text="用户名:")
        username_label.pack()

        username_entry = tk.Entry(add_friend_dialog)
        username_entry.pack()

        ok_button = tk.Button(
            add_friend_dialog,
            text="OK",
            command=lambda: self.process_add_friend(username_entry.get(), add_friend_dialog)
        )
        ok_button.pack()

        cancel_button = tk.Button(
            add_friend_dialog,
            text="Cancel",
            command=add_friend_dialog.destroy
        )
        cancel_button.pack()

    def process_add_friend(self, username, dialog):
        if username == "":
            messagebox.showerror("错误", "用户名不能为空")
        elif username == self.current_user:
            messagebox.showerror("错误", "不能添加自己为好友")
        elif self.check_friend_exist(username):
            messagebox.showerror("错误", "好友已存在")
        else:
            # 检查好友是否存在
                result = addFriend(self.current_user,username)
                if result:
                    messagebox.showinfo("好友", "好友已添加")
                    dialog.destroy()
                else:
                    messagebox.showinfo("好友","添加失败")
        self.refresh_friends()
     
       

    def open_remove_friend_dialog(self):
        # 创建删除好友对话框
        remove_friend_dialog = tk.Toplevel(self.root)
        remove_friend_dialog.title("删除好友")
        remove_friend_dialog.geometry("200x150")

        username_label = tk.Label(remove_friend_dialog, text="用户名:")
        username_label.pack()

        username_entry = tk.Entry(remove_friend_dialog)
        username_entry.pack()

        ok_button = tk.Button(
            remove_friend_dialog,
            text="OK",
            command=lambda: self.process_remove_friend(username_entry.get(), remove_friend_dialog)
        )
        ok_button.pack()

        cancel_button = tk.Button(
            remove_friend_dialog,
            text="Cancel",
            command=remove_friend_dialog.destroy
        )
        cancel_button.pack()

    # 处理删除好友操作。检查输入的用户名是否合法，并进行相应的处理，如从列表中删除好友等。
    def process_remove_friend(self, username, dialog):
        if username == "":
            messagebox.showerror("错误", "用户名不能为空")
        elif username == self.current_user:
            messagebox.showerror("错误", "不能删除自己")
        else:
            # 检查好友是否存在
            if self.check_friend_exist(username):
                result = deleteFriend(self.current_user,username)
                if result:
                    messagebox.showinfo("好友", "好友已删除")
                    dialog.destroy()
                else:
                    messagebox.showinfo("好友","删除失败")
                        
            else:
                messagebox.showerror("错误", "好友不存在")
        self.refresh_friends()

    # 检查好友是否存在于好友列表中。
    def check_friend_exist(self, username):
        for friend in self.friends:
            if friend.username == username:
                return True
        return False

    # 刷新好友列表。
    def refresh_friends(self):
        
        #从服务器获取好友列表ip端口号与在线状态 
        unread_message_backup = {}
        friend_backup =  self.friends
        for item in friend_backup:
            if item.ip != 0:
                unread_message_backup[item.ip] = item.unread_messages
        
        self.friends =  []
        friend_list = getFriends(self.current_user)
        # print(friend_list)
        if friend_list:
            for item in friend_list:
                friend = Friend(item[0], item[1], item[2])
                if item[1] != '0':
                    friend.online = True
                self.friends.append(friend)
        else:
            return False
        
        for backup_ip in unread_message_backup.keys():
            for item in self.friends:
                if item.ip == backup_ip:
                    item.unread_messages = unread_message_backup[backup_ip]
           


        self.friends.sort(key=lambda friend: (friend.online, friend.unread_messages), reverse=True)
        # 清空好友列表
        self.friend_listbox.delete(0, tk.END)

        # 更新好友列表
        for friend in self.friends:
            status = "在线" if friend.online else "离线"
            # 截断最新消息长度并添加省略号
            latest_message = friend.latest_message[:10] + "..." if len(friend.latest_message) > 10 else friend.latest_message
            # 根据在线状态设置文本颜色
            if friend.unread_messages > 0:
                text_color = "red"
            else:
                text_color = "green" if friend.online else "black"
            friend_info = f"{friend.username}  IP: {friend.ip}  Port: {friend.port} [{status}] {latest_message} ({friend.unread_messages})"
            self.friend_listbox.insert(tk.END, friend_info)
            self.friend_listbox.itemconfig(tk.END, fg=text_color)

    # # 设置好友的在线状态。
    # def set_online_status(self, username, online):
    #     friend = next((f for f in self.friends if f.username == username), None)
    #     if friend:
    #         friend.online = online
    #         self.refresh_friends()

    # # 设置好友的最新消息。
    # def set_latest_message(self, username, message):
    #     for friend in self.friends:
    #         if friend.username == username:
    #             friend.latest_message = message
    #             friend.unread_messages += 1
    #             break


    def open_chat_window(self, event):
        selected_friend_index_tuple = event.widget.curselection()
        if selected_friend_index_tuple:
            selected_friend_index = selected_friend_index_tuple[0]
            selected_friend = self.friends[selected_friend_index]
            
            if selected_friend.online:
                messages = []  # 存储消息的列表
                chat_window = ChatGUI(self.root, self.current_user, messages,selected_friend,self.pri_key)
                chat_window.title(f"与 {selected_friend.username} 的聊天")

                # 设置好友的最新消息和未读消息数
                selected_friend.latest_message = ""
                selected_friend.unread_messages = 0
                self.refresh_friends()

                chat_window.mainloop()
            else:
                messagebox.showinfo("好友未在线", "好友未在线")
                self.friend_listbox.selection_clear(0, tk.END)  # 取消选中状态
        else:
            messagebox.showerror("错误", "请先选择一个好友")

    def run(self):
        self.refresh_friends()
        self.friend_listbox.bind("<Double-Button-1>",self.open_chat_window)
        self.root.mainloop()

    # def run(self):
    #     self.root.mainloop()

if __name__ == "__main__":
    friend_list_gui = FriendListGUI()
    # friend_list_gui.current_user = "Alice"  # 设置当前用户的用户名
    # friend_list_gui.friends = [
    #     Friend("Bob", "192.168.0.2", 5678),
    #     Friend("Charlie", "192.168.0.3", 9012),
    #     Friend("David", "192.168.0.4", 3456)
    # ]

    # # 模拟一些在线状态和最新消息的更新
    # friend_list_gui.set_online_status("Bob", True)
    # friend_list_gui.set_online_status("Charlie", True)
    # friend_list_gui.set_latest_message("Bob", "你好，Alice")
    # friend_list_gui.set_latest_message("Charlie", "今天天气不错")

    friend_list_gui.run()

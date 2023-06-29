import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from chat_gui2 import ChatGUI

class Friend:
    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.online = False
        self.latest_message = ""
        self.unread_messages = 0

class FriendListGUI:
    def __init__(self):
        self.friends = []  # 存储好友信息的列表
        self.current_user = None  # 当前用户的用户名

        self.root = tk.Tk()
        self.root.title("好友列表")
        self.root.geometry("400x300")

        self.friend_frame = tk.Frame(self.root)
        self.friend_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.friend_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.friend_listbox = tk.Listbox(
            self.friend_frame,
            yscrollcommand=self.scrollbar.set,
            width=50
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
            if self.check_friend_exist(username):
                friend = Friend(username, "192.168.0.1", 1234)  # 假设固定IP和端口号
                self.friends.append(friend)
                self.refresh_friends()
                messagebox.showinfo("添加好友", "好友请求已发送")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "用户名不存在")

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
                self.remove_friend_by_username(username)
                self.refresh_friends()
                messagebox.showinfo("删除好友", "成功删除好友")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "好友不存在")

    # 检查好友是否存在于好友列表中。
    def check_friend_exist(self, username):
        for friend in self.friends:
            if friend.username == username:
                return True
        return False
    
    # 根据用户名从好友列表中删除好友。
    def remove_friend_by_username(self, username):
        self.friends = [friend for friend in self.friends if friend.username != username]

    # 刷新好友列表。
    def refresh_friends(self):
        # 清空好友列表
        self.friend_listbox.delete(0, tk.END)

        # 按照在线状态和最近聊天将好友排序
        sorted_friends = sorted(
            self.friends,
            key=lambda friend: (not friend.online, friend.latest_message),
            reverse=True
        )

        # 将在线用户置顶
        online_friends = [friend for friend in sorted_friends if friend.online]
        offline_friends = [friend for friend in sorted_friends if not friend.online]
        sorted_friends = online_friends + offline_friends

        # 更新好友列表
        for friend in sorted_friends:
            status = "在线" if friend.online else "离线"
            # 截断最新消息长度并添加省略号
            latest_message = friend.latest_message[:10] + "..." if len(friend.latest_message) > 10 else friend.latest_message
            # 根据在线状态设置文本颜色
            text_color = "green" if friend.online else "black"
            friend_info = f"{friend.username} [{status}] {latest_message} ({friend.unread_messages})"
            self.friend_listbox.insert(tk.END, friend_info)
            self.friend_listbox.itemconfig(tk.END, fg=text_color)
            

    # 设置好友的在线状态。
    def set_online_status(self, username, is_online):
        for friend in self.friends:
            if friend.username == username:
                friend.online = is_online
                break

        self.refresh_friends()

    # 设置好友的最新消息。
    def set_latest_message(self, username, message):
        for friend in self.friends:
            if friend.username == username:
                friend.latest_message = message
                friend.unread_messages += 1
                break

        self.refresh_friends()

    # 打开聊天界面。
    def open_chat_window(self):
        selected_friend_index_tuple = self.friend_listbox.curselection()
        if selected_friend_index_tuple:
            selected_friend_index = selected_friend_index_tuple[0]
            selected_friend = self.friends[selected_friend_index]

            messages = []  # 存储消息的列表
            chat_window = ChatGUI(self.root, self.current_user, messages)
            chat_window.title(f"与 {selected_friend.username} 的聊天")
            chat_window.geometry("500x400")

            # 设置好友的最新消息和未读消息数
            selected_friend.latest_message = ""
            selected_friend.unread_messages = 0
            self.refresh_friends()

            chat_window.mainloop()
        else:
            messagebox.showerror("错误", "请先选择一个好友")

    # # 运行好友列表应用程序。
    # def run(self, current_user):
    #     self.current_user = current_user
    #     self.refresh_friends()
    #     self.friend_listbox.bind("<Double-Button-1>", lambda event: self.open_chat_window())
    #     self.root.mainloop()
    def run(self):
        self.refresh_friends()
        self.friend_listbox.bind("<Double-Button-1>", lambda event: self.open_chat_window())
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

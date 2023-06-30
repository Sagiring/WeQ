import tkinter as tk
from tkinter import messagebox
import Weq
from Weq import FriendListGUI
import os
class InstantMessengerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("欢迎使用WeQ!")
        self.geometry("300x200")
        
        self.login_frame = LoginPage(self, self.show_registration_page)
        self.registration_frame = RegistrationPage(self, self.show_login_page)
        
        self.show_login_page()

    def show_friend_list_page(self, username,pri_key):
        self.hide()
        friend_list = FriendListGUI(pri_key)
        friend_list.current_user = username
        friend_list.run()
        self.destroy()

    def show_login_page(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack()
        
    def show_registration_page(self):
        self.login_frame.pack_forget()
        self.registration_frame.pack()
        
        
    def hide(self):
        self.withdraw()
        
    def show(self):
        self.deiconify()


class LoginPage(tk.Frame):
    def __init__(self, master, show_registration_page, ):
        super().__init__(master)
        
        self.label_username = tk.Label(self, text="用户名:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()
        
        self.label_password = tk.Label(self, text="密码:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()
        
        self.btn_register = tk.Button(self, text="没有帐户，点击注册", command=show_registration_page, width=20, height=0)
        self.btn_register.pack()
        
        self.btn_login = tk.Button(self, text="登录", command=self.login)
        self.btn_login.pack()
        


    def login(self):

        username = self.entry_username.get()
        password = self.entry_password.get()
        result = Weq.login(username,password)
        if result:
            messagebox.showinfo("登录", "登录成功")
            pri_key = Weq.addPubkey(username)
            if pri_key:
                self.master.show_friend_list_page(username,pri_key)  # 修改这一行
        else:
            messagebox.showinfo("登录", "用户名或密码错误")


class RegistrationPage(tk.Frame):
    def __init__(self, master, show_login_page):
        super().__init__(master)
        
        self.label_email = tk.Label(self, text="邮箱:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()
        
        self.label_username = tk.Label(self, text="用户名:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()
        
        self.label_password = tk.Label(self, text="密码:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()
        
        self.btn_create_account = tk.Button(self, text="创建账户", command=self.create_account)
        self.btn_create_account.pack()

        self.btn_jump_to_login=tk.Button(self,text="已有帐户，直接登录",command=show_login_page)
        self.btn_jump_to_login.pack()
        
        self.show_login_page = show_login_page
        
    def create_account(self):
        email = self.entry_email.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        result = Weq.register(username,password,email)
        if  result:
            messagebox.showinfo("Registration", "注册成功")
            self.show_login_page()
        else:
            messagebox.showinfo("Registration", "用户名已被使用或密码为数字+字母")
        
        # 返回到登录界面
        


class SuccessPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label_success = tk.Label(self, text="登录成功！")
        self.label_success.pack()


if __name__ == "__main__":
    img_path = './img/'
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    app = InstantMessengerApp()
    app.mainloop()

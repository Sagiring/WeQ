import tkinter as tk
from tkinter import messagebox
import Weq
from Weq import FriendListGUI
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

class InstantMessengerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("欢迎使用WeQ!")
        self.geometry("500x300")
        style = Style()
        style = Style(theme='lumen')
        self = style.master
        
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
    def __init__(self, master, show_registration_page,):
        super().__init__(master)
        
       
        label_title=ttk.Label(self,text='WeQ',bootstyle=DANGER,font=('Times New Roman',20))
        label_title.grid(row=1,column=3,padx=5,pady=10,sticky='nsew')

        label_username = ttk.Label(self, text="用户名:",font=('楷体',13), bootstyle=PRIMARY)
        label_username.grid(row=2, column=2, padx=5, pady=20, sticky=tk.E)

        self.entry_username = ttk.Entry(self, bootstyle=SECONDARY)
        self.entry_username.grid(row=2, column=3, padx=5, pady=10)

        label_password = ttk.Label(self, text="密码:",font=('楷体',13), bootstyle=PRIMARY)
        label_password.grid(row=3, column=2, padx=5, pady=10, sticky=tk.E)

        self.entry_password = ttk.Entry(self, show="*", bootstyle=SECONDARY)
        self.entry_password.grid(row=3, column=3, padx=5, pady=10)

        btn_login = ttk.Button(self, text="登录",command=self.login, style=("WARNING.TButton"))
        btn_login.grid(row=4, column=3, columnspan=2, padx=5, pady=10)

        btn_register = ttk.Button(self, text="没有帐户，点击注册", command=show_registration_page, style=("PRIMARY.TButton", "outline-toolbutton"))
        btn_register.grid(row=5, column=3, columnspan=2, padx=5, pady=10)

        # self.login_callback = login_callback
        


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
        
        label_email = ttk.Label(self, text="邮箱:",font=('楷体',12),bootstyle=PRIMARY)
        label_email.grid(row=2,column=0,padx=5,pady=10)

        self.entry_email = ttk.Entry(self,bootstyle=SECONDARY)
        self.entry_email.grid(row=2,column=1,padx=5,pady=10)

        btn_login = ttk.Button(self, text="获取验证码", command=self.account_verification, style=("SUCCESS.TButton"))
        btn_login.grid(row=2, column=3,padx=5, pady=10)


        label_code=ttk.Label(self,text='验证码',font=('楷体',12),bootstyle=PRIMARY)
        label_code.grid(row=3,column=0,padx=5,pady=10)

        self.entry_code = ttk.Entry(self,bootstyle=SECONDARY)
        self.entry_code.grid(row=3,column=1,padx=5,pady=10)
      
        label_username = ttk.Label(self, text="用户名:",font=('楷体',12),bootstyle=PRIMARY)
        label_username.grid(row=4,column=0,padx=5,pady=10)
        self.entry_username = ttk.Entry(self,bootstyle=SECONDARY)
        self.entry_username.grid(row=4,column=1,padx=5,pady=10)

        label_password = ttk.Label(self, text="密码:",font=('楷体',12),bootstyle=PRIMARY)
        label_password.grid(row=5,column=0,padx=5,pady=10)
        self.entry_password = ttk.Entry(self, show="*",bootstyle=SECONDARY)
        self.entry_password.grid(row=5,column=1,padx=5,pady=10)
        
        btn_login = ttk.Button(self, text="创建账户", command=self.create_account, style=("WARNING.TButton","outline-toolbutton"))
        btn_login.grid(row=9, column=1, columnspan=2, padx=5, pady=10)

        btn_register = ttk.Button(self, text="已有帐户，直接登录", command=show_login_page, style=("SECONDARY.TButton"))
        btn_register.grid(row=10, column=1, columnspan=2, padx=5, pady=10)
        
        self.show_login_page = show_login_page

    def account_verification(self):
        send_again = 1
        # def send_again_fuc(send_again):
        #     send_again = 0 

        address=self.entry_email.get()
        result=Weq.checkemail(address)
        if result==2:
            messagebox.showerror("Registration","邮箱地址错误")
        
        if send_again:
            result=Weq.mailverification(address)
            if result:
                box = messagebox.showinfo("Registration","验证码已发送！")
                send_again = 0
                # self.after(60000, send_again_fuc,args=send_again)  # 2秒后关闭消息框
        else:
            messagebox.showerror("Registration","发送过于频繁，请稍后重试")
        


    def create_account(self):
        email = self.entry_email.get()
        code=self.entry_code.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        result = Weq.register(username,password,email,code)
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
    app = InstantMessengerApp()
    app.mainloop()

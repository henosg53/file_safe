import os
import tkinter as tk
from tkinter import messagebox
import bcrypt
import configparser


class XAuth:
    def __init__(self):
        self.data_dir = 'data'
        self.config_file_path = os.path.join(self.data_dir, 'config.ini')
        self.check_config()

        self.stored_password = self.fetch_config(section="Profile", key="password")
        self.stored_username = self.fetch_config(section="Profile", key="username")

        # print(f"username: {self.stored_username}, password: {self.stored_password}")

        self.root = tk.Tk()
        self.root.title("XCrypt")
        self.root.geometry("200x200")

        self.welcome_label = tk.Label(self.root, text=f"Welcome {self.stored_username}",
                                      font="forte 15 bold italic")
        self.welcome_label.pack(pady=10)
        self.passwd_label = tk.Label(self.root, text="Enter password", font="forte 10 bold")
        self.passwd_label.pack()
        self.passwd = tk.StringVar()
        self.passwd_entry = tk.Entry(self.root, textvariable=self.passwd, show="*", width=20)
        self.passwd_entry.pack(pady=5)

        self.login_btn = tk.Button(self.root, text="Login", bg="blue", fg="white",
                                   activebackground="darkblue",
                                   activeforeground="white",
                                   command=self.auth_pass)
        self.login_btn.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.mainloop()

    def exit(self):
        self.root.destroy()

    def check_config(self):
        if not os.path.exists(self.config_file_path):
            # XConfig()
            pass
        else:
            pass

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def auth_pass(self):
        if self.verify_password(self.passwd.get(), self.stored_password):
            self.root.withdraw()
            # XCryptUI()
        else:
            messagebox.showerror(title="Incorrect Password",
                                 message="Please re-enter the correct password")
            self.passwd_entry.delete(0, tk.END)
            return

    def fetch_config(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.config_file_path)
        return config.get(section, key)


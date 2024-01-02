import tkinter as tk
from tkinter import messagebox
import configparser
import bcrypt
import os


class ConfigView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.controller = None

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.username, self.password, self.update_btn = None, None, None
        self.message_box = messagebox
        self.create_components()

    def create_components(self):
        label = tk.Label(self, text="Configurations", font="forte 20 bold")
        label.pack()

        username_label = tk.Label(self, text="Username")
        username_label.pack()
        self.username = tk.Entry(self, textvariable=self.username_var)
        self.username.pack()

        password_label = tk.Label(self, text="Password")
        password_label.pack()
        self.password = tk.Entry(self, textvariable=self.password_var, show='*')
        self.password.pack()

        self.update_btn = tk.Button(self, text="Update Change", bg="blue", fg="white",
                                    command=self.update_conf)
        self.update_btn.pack()

    def update_conf(self):
        self.controller.update_config()

    def set_controller(self, controller):
        self.controller = controller

    @staticmethod
    def is_field_empty(field):
        if field is None or field == "":
            return True
        return False


# from view.x_auth import XAuth
def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


class XConfig:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Configuration")
        self.title_label = tk.Label(self.root, text="New User")
        self.title_label.pack()

        # self.first_name_label = tk.Label(self.root, text="Firstname: ")
        # self.first_name_label.pack()
        # self.first_name = tk.StringVar()
        # self.first_name_entry = tk.Entry(self.root, textvariable=self.first_name)
        # self.first_name_entry.pack()

        self.user_name_label = tk.Label(self.root, text="Username: ")
        self.user_name_label.pack()
        self.user_name = tk.StringVar()
        self.user_name_entry = tk.Entry(self.root, textvariable=self.user_name)
        self.user_name_entry.pack()

        self.passwd_label = tk.Label(self.root, text="Password: ")
        self.passwd_label.pack()
        self.passwd = tk.StringVar()
        self.passwd_entry = tk.Entry(self.root, textvariable=self.passwd, show='*')
        self.passwd_entry.pack()

        self.submit_btn = tk.Button(self.root, text="submit", command=self.submit_form)
        self.submit_btn.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.mainloop()

    @staticmethod
    def is_field_empty(field):
        if field is None or field == "":
            return True
        return False

    def submit_form(self):
        print(f"Name: {self.user_name.get()}")
        print(f"Password: {self.passwd.get()}")

        if self.is_field_empty(self.user_name.get()):
            messagebox.showerror(title="Error", message="Refill fields!")
            return

        elif self.is_field_empty(self.passwd.get()):
            messagebox.showerror(title="Error", message="Refill fields!")
            return

        else:
            config = configparser.ConfigParser()
            config["Profile"] = {
                'username': self.user_name.get(),
                'password': encrypt_password(self.passwd.get())
            }
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)
            config_file_path = os.path.join(data_dir, "config.ini")

            with open(config_file_path, "w") as config_file:
                config.write(config_file)

            messagebox.showinfo("Success", "Configuration saved!")

            self.root.withdraw()
            # XAuth()

    def exit(self):
        self.root.destroy()

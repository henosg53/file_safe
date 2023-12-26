import json
import os
from xcrypt import XCrypt
import tkinter as tk
from tkinter import messagebox, filedialog, Tk, simpledialog
import configparser


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

        self.root.mainloop()

    def submit_form(self):
        print(f"Name: {self.user_name.get()}")
        print(f"Password: {self.passwd.get()}")
        config = configparser.ConfigParser()
        config["Profile"] = {
            'username': self.user_name.get(),
            'password': self.passwd.get()

        }
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        config_file_path = os.path.join(data_dir, "config.ini")

        with open(config_file_path, "w") as config_file:
            config.write(config_file)

        messagebox.showinfo("Success", "Configuration saved!")

        self.root.withdraw()
        XAuth()


class XAuth:
    def __init__(self):
        self.data_dir = 'data'
        self.config_file_path = os.path.join(self.data_dir, 'config.ini')
        self.check_config()
        self.stored_password = "soul"

        self.root = tk.Tk()
        self.root.title("Login")
        self.title_label = tk.Label(self.root, text="Login")
        self.title_label.pack()
        self.passwd_label = tk.Label(self.root, text="password")
        self.passwd_label.pack()
        self.passwd = tk.StringVar()
        self.passwd_entry = tk.Entry(self.root, textvariable=self.passwd, show="*", width=20)
        self.passwd_entry.pack()

        self.login_btn = tk.Button(self.root, text="Login", bg="blue", fg="white",
                                   activebackground="darkblue",
                                   activeforeground="white",
                                   command=self.auth_pass)
        self.login_btn.pack()

        self.root.mainloop()

    def check_config(self):
        if not os.path.exists(self.config_file_path):
            XConfig()

        else:
            pass

    def auth_pass(self):
        if self.passwd.get() == self.stored_password:

            self.root.withdraw()
            XCryptUI()
        else:
            exit()


class XCryptUI:
    def __init__(self):
        # # password validation

        # self.validate_user()
        # auth = XAuth()

        self.root = tk.Tk()
        self.root.title("XCrypt")
        self.screen_height = 500
        self.screen_width = 500

        self.root.configure(bg="darkgray",
                            padx=5, pady=5,
                            height=self.screen_height, width=self.screen_width)

        # xcrypt conf
        self.crypt = XCrypt()
        self.encrypted_files_path = os.path.join(os.getcwd(), 'data/file_secure/encrypted_files')
        self.key_storage_path = os.path.join(os.getcwd(), 'data/file_secure/key_storage.json')
        self.create_secure_directory(self.encrypted_files_path)
        self.encrypted_files_path = os.path.join(os.getcwd(), 'data/file_secure/encrypted_files')

        # declare_components
        (self.title,
         self.files_frame,
         self.file_listbox,
         self.files_scrollbar,
         self.encrypt_button,
         self.buttons_frame,
         self.decrypt_button,
         self.delete_button) = None, None, None, None, None, None, None, None

        # create components
        self.create_components()

        self.root.mainloop()

    def create_components(self):
        self.title = tk.Label(self.root, text='XCrypt File Safe',
                              font="forte 20 bold",
                              fg="gray",
                              width=50)
        self.title.pack(padx=10, pady=10)

        self.encrypt_button = tk.Button(self.root, text="Import File", bg="blue", fg="white",
                                        activebackground="darkblue",
                                        activeforeground="white",
                                        command=self.encrypt)
        self.encrypt_button.pack(pady=5)

        self.files_frame = tk.Frame(self.root)
        self.files_frame.pack()

        self.files_scrollbar = tk.Scrollbar(self.files_frame)
        self.files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(self.files_frame,
                                       bg="gray",
                                       font="forte",
                                       selectbackground="black",
                                       selectforeground="white",
                                       yscrollcommand=self.files_scrollbar.set,
                                       # cursor="circle",
                                       width=50,
                                       height=10)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.files_scrollbar.config(command=self.file_listbox.yview)

        self.populate_file_listbox()

        self.buttons_frame = tk.Frame(self.root, bg="darkgray")
        self.buttons_frame.pack(pady=5)

        self.decrypt_button = tk.Button(self.buttons_frame, text="Decrypt File", bg="green", fg="white",
                                        activebackground="darkgreen",
                                        activeforeground="white",
                                        # relief="grooved",
                                        command=self.decrypt)
        self.decrypt_button.pack(padx=(5, 5), side=tk.LEFT)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete From Safe", bg="red", fg="white",
                                       activebackground="darkred",
                                       activeforeground="white",
                                       command=self.delete_file)
        self.delete_button.pack(padx=(5, 5), side=tk.RIGHT, fill=tk.BOTH)

    @staticmethod
    def validate_user():
        passwd = simpledialog.askstring(title="password", prompt="password", show=None)

        if passwd == "soul":
            return True
        else:
            exit()

    def create_secure_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            key = {}
            with open(self.key_storage_path, 'w') as file:
                json.dump(key, file)
            print("path and key storage file created")
        else:
            print("secure path exists! ")

    # file dialog box
    @staticmethod
    def select_file():
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    # populate listbox     
    def populate_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for filename in os.listdir(self.encrypted_files_path):
            file_path = os.path.join(self.encrypted_files_path, filename)
            if os.path.isfile(file_path):
                self.file_listbox.insert(tk.END, filename)

    # encrypt file
    def encrypt(self):
        file = self.select_file()
        if file:
            self.crypt.encrypt_file(file)
            messagebox.showinfo("Encryption Result", f"Encrypted file: {file}")
        else:
            messagebox.showwarning("Empty Input", "Please enter file to encrypt.")

        self.populate_file_listbox()

    # decrypt selected encrypted file
    def decrypt(self):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_file = self.file_listbox.get(selected_index)
            file_path = os.path.join(self.encrypted_files_path, selected_file)
            print(selected_file)
            decrypted_file_path = self.crypt.decrypt_file(file_path)
            messagebox.showinfo("Decryption Result",
                                f"File decrypted successfully. Decrypted file saved as: {decrypted_file_path}")

            self.file_listbox.delete(selected_index)  # Remove the decrypted file from the listbox
            self.populate_file_listbox()
        else:
            messagebox.showwarning("No File Selected", "Please select a file to decrypt.")

    # remove encrypted file from file safe
    def delete_file(self):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_file = self.file_listbox.get(selected_index)
            file_path = os.path.join(self.encrypted_files_path, selected_file)

            print(file_path)
            self.crypt.remove_file(file_path)
            messagebox.showinfo("File Deleted", f"The file '{selected_file}' has been deleted.")

            self.file_listbox.delete(selected_index)  # Remove the deleted file from the listbox
        else:
            messagebox.showwarning("No File Selected", "Please select a file to delete.")

        self.populate_file_listbox()

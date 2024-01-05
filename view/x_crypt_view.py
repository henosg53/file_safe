import tkinter as tk
import customtkinter as ctk
import os, datetime, stat, json
from model.xcrypt_model import XCrypt
from tkinter import filedialog, ttk, messagebox


class XCryptView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # # authenticate user
        # XAuth()
        self.parent = parent
        self.controller = None

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
         self.file_treeview,
         self.selected_file,
         self.files_scrollbar,
         self.encrypt_button,
         self.buttons_frame,
         self.decrypt_button,
         self.delete_button,
         self.message_box) = None, None, None, None, None, None, None, None, None, None, messagebox

        # create components
        self.create_components()

    def set_controller(self, controller):
        self.controller = controller

    def create_components(self):

        self.title = tk.Label(self, text='XCrypt File Safe',
                              font="forte 20 bold",
                              fg="gray",
                              width=50)
        self.title.pack(padx=10, pady=10)

        self.encrypt_button = tk.Button(self, text="Import File", bg="blue", fg="white",
                                        activebackground="darkblue",
                                        activeforeground="white",
                                        command=self.encrypt)
        self.encrypt_button.pack(pady=5)

        self.files_frame = tk.Frame(self)
        self.files_frame.pack()

        self.files_scrollbar = tk.Scrollbar(self.files_frame)
        self.files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ('size', 'modified', 'permissions')
        self.file_treeview = ttk.Treeview(self.files_frame, columns=columns)
        self.file_treeview.heading("#0", text="Name", anchor=tk.W)
        self.file_treeview.heading("size", text="Size", anchor=tk.W)
        self.file_treeview.heading("modified", text="Last Modified", anchor=tk.W)
        self.file_treeview.heading("permissions", text="Permissions", anchor=tk.W)

        self.file_treeview.column("#0", width=300)
        self.file_treeview.column("size", width=100)
        self.file_treeview.column("modified", width=150)
        self.file_treeview.pack(side=tk.LEFT, fill=tk.BOTH)
        self.file_treeview.configure(yscrollcommand=self.files_scrollbar.set)

        self.file_treeview.bind('<<TreeviewSelect>>', self.item_selected)

        self.files_scrollbar.config(command=self.file_treeview.yview)

        self.populate_file_listbox()

        self.buttons_frame = tk.Frame(self, bg="darkgray")
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

    def file_property(self, filename):
        file_path = os.path.join(self.encrypted_files_path, filename)
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size
        creation_time = file_stat.st_ctime
        modification_time = file_stat.st_mtime
        access_time = file_stat.st_atime
        permissions = file_stat.st_mode
        is_directory = stat.S_ISDIR(permissions)

        details = {
            'filename': filename,
            'size': file_size,
            'creation_time': datetime.datetime.fromtimestamp(creation_time),
            'modification_time': datetime.datetime.fromtimestamp(modification_time),
            'access_time': datetime.datetime.fromtimestamp(access_time),
            'permissions': stat.filemode(permissions),
            'is_directory': is_directory
        }
        return details

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
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    def item_selected(self, event):
        for selected_item in self.file_treeview.selection():
            item = self.file_treeview.item(selected_item)
            self.selected_file = item['text']
            return item['text']

    # populate listbox
    def populate_file_listbox(self):
        self.file_treeview.delete(*self.file_treeview.get_children())
        for filename in os.listdir(self.encrypted_files_path):
            file_path = os.path.join(self.encrypted_files_path, filename)
            details = self.file_property(file_path)
            if os.path.isfile(file_path):
                self.file_treeview.insert("", tk.END,
                                          text=filename,
                                          values=(details['size'],
                                                  details['modification_time'],
                                                  details['permissions']))

    def encrypt(self):
        self.controller.encrypt_file()

    def decrypt(self):
        self.controller.decrypt_file()

    def delete_file(self):
        self.controller.delete_file()

    def remove_grid(self):
        self.grid_remove()


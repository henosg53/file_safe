import json
import os
from xcrypt import XCrypt
import tkinter as tk
from tkinter import messagebox, filedialog, Tk

from controller.x_controller import XController, NavBarController
from model.xcrypt import XCrypt


class NavBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = None

        self.menu_bar = tk.Menu(self)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.do_nothing)
        file_menu.add_command(label="Open", command=self.do_nothing)
        file_menu.add_command(label="Save", command=self.do_nothing)
        file_menu.add_command(label="Save Us", command=self.do_nothing)

        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=parent.quit)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.do_nothing)
        edit_menu.add_command(label="Redo", command=self.do_nothing)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.do_nothing)
        edit_menu.add_command(label="Copy", command=self.do_nothing)
        edit_menu.add_command(label="Paste", command=self.do_nothing)
        edit_menu.add_command(label="Delete", command=self.do_nothing)
        edit_menu.add_command(label="Select All", command=self.do_nothing)

        self.menu_bar.add_cascade(label="View", menu=edit_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Index", command=self.do_nothing)
        help_menu.add_command(label="About", command=self.do_nothing)
        help_menu.add_command(label="Learn Features", command=self.do_nothing)

        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="Appearance", command=self.do_nothing)
        settings_menu.add_command(label="Configuration", command=self.configuration)

        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)

    def get_menu_bar(self):
        return self.menu_bar

    def set_controller(self, controller):
        self.controller = controller

    def get_controller(self):
        return self.controller

    def do_nothing(self):
        pass

    def configuration(self):
        self.controller.configuration_page()


class XCryptUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # authenticate user
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
         self.files_scrollbar,
         self.encrypt_button,
         self.buttons_frame,
         self.decrypt_button,
         self.delete_button,
         self.message_box) = None, None, None, None, None, None, None, None, messagebox

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

    def encrypt(self):
        self.controller.encrypt_file()

    def decrypt(self):
        self.controller.decrypt_file()

    def delete_file(self):
        self.controller.delete_file()


class XView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.navbar = None
        self.navbar_controller = None
        self.main_view = None
        self.main_view_controller = None
        self.main_view_model = None
        self.controller = None

        self.create_components()

    def create_components(self):
        self.navbar = NavBar(self)
        self.navbar_controller = NavBarController(model="", view=self.navbar)
        self.set_component_controller(component=self.navbar, controller=self.navbar_controller)

        self.parent.config(menu=self.navbar.get_menu_bar())

        self.main_view = XCryptUI(self)
        self.main_view_model = XCrypt()
        self.main_view_controller = XController(model=self.main_view_model, view=self.main_view)
        self.set_component_controller(component=self.main_view, controller=self.main_view_controller)

        self.main_view.grid()

    def set_controller(self, controller):
        self.controller = controller

    @staticmethod
    def set_component_controller(component, controller):
        component.set_controller(controller=controller)

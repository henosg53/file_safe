import platform
import subprocess

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import stat
import datetime
import customtkinter as ctk

from model.x_frame import XFrame
from model.xcrypt_model import XCrypt


class XSidebar(XFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent = master
        self.sidebar_content = None
        self.configure(width=200, fg_color="black", corner_radius=0)
        # self.pack(fill=tk.Y, expand=True)
        self.pack(fill=tk.BOTH, expand=True)
        # self.grid_rowconfigure(1, weight=1)

        self.places = ["Computer",
                       "Home",
                       "Desktop",
                       "Documents",
                       "Music",
                       "Pictures",
                       "Videos",
                       "Downloads"]
        self.devices = ["File System"]
        self.networks = ["Browse Network"]

        self.create_components()

    def create_components(self):
        self.sidebar_content = ctk.CTkScrollableFrame(self, width=150, fg_color="gray",
                                                      corner_radius=0)
        self.sidebar_content.pack(fill=tk.BOTH, expand=True)

        places_label = ctk.CTkLabel(self.sidebar_content, text="Bookmarks", font=ctk.CTkFont(size=15, weight="bold"))
        places_label.pack(padx=0, pady=(5, 5))

        for index, place in enumerate(self.places):
            # Create the directory item component
            places_frame = ttk.Frame(self.sidebar_content)
            item_label = ttk.Label(places_frame, text=place)
            item_label.bind("<Button-1>", lambda event, x_place=place: self.left_clicked(x_place))
            item_label.bind("<Button-3>", lambda event, x_place=place: self.right_clicked(x_place))
            item_label.pack(side=tk.LEFT)

            # Pack the directory item component
            places_frame.pack(fill=tk.X, padx=5, pady=5)

        separator = ttk.Separator(self.sidebar_content, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=5, pady=5)

        places_label = ctk.CTkLabel(self.sidebar_content, text="Devices", font=ctk.CTkFont(size=15, weight="bold"))
        places_label.pack(padx=0, pady=(5, 5))

        for index, device in enumerate(self.devices):
            devices_frame = ttk.Frame(self.sidebar_content)
            item_label = ttk.Label(devices_frame, text=device)
            item_label.bind("<Button-1>", lambda event, x_place=device: self.left_clicked(x_place))
            item_label.pack(side=tk.LEFT)

            # Pack the directory item component
            devices_frame.pack(fill=tk.X, padx=5, pady=5)

        separator = ttk.Separator(self.sidebar_content, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, padx=5, pady=5)

        places_label = ctk.CTkLabel(self.sidebar_content, text="Network", font=ctk.CTkFont(size=15, weight="bold"))
        places_label.pack(padx=0, pady=(5, 5))

        for index, network in enumerate(self.networks):
            networks_frame = ttk.Frame(self.sidebar_content)
            item_label = ttk.Label(networks_frame, text=network)
            item_label.pack(side=tk.LEFT)

            # Pack the directory item component
            networks_frame.pack(fill=tk.X, padx=5, pady=5)

    # @staticmethod
    def left_clicked(self, folder):
        if folder == 'Home':
            self.parent.go_home()
        elif folder == 'Computer':
            print(f"{folder} left clicked!")
        else:
            # self.parent.curr_dir = ""
            path = os.path.join(self.parent.home_path, folder)
            self.parent.clean_file_list()
            self.parent.populate_file_list_frame(path)
            self.parent.curr_dir = path
            print(f"{folder} left clicked!")

    @staticmethod
    def right_clicked(folder):
        print(f"{folder} right clicked!")


class XScrollableFrame(ctk.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas to hold the frame content
        self.canvas = tk.Canvas(self, yscrollcommand=scrollbar.set, height=470)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Associate the scrollbar with the canvas
        scrollbar.configure(command=self.canvas.yview)
        # Create a frame inside the canvas to hold the content
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Add the frame to the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        # Configure the canvas to scroll the frame
        self.scrollable_frame.bind("<Configure>",
                                   lambda event: self.canvas.configure(
                                       scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def create_components(self):
        pass


class XItemProperties:
    def __init__(self, master, file_details) -> None:
        self.parent = master
        self.file_details = file_details
        properties_toplevel = ctk.CTkToplevel(self.parent, height=500)
        properties_toplevel.title("Properties")
        properties_toplevel.geometry(f"{500}x{300}")

        for i, (key, value) in enumerate(self.file_details.items()):
            label = ctk.CTkLabel(properties_toplevel, text=f"{key}: {value}")
            label.pack(anchor=tk.W)


class XPlorerView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        # configuration
        self.parent = parent
        self.controller = None
        self.pack(fill=tk.BOTH, expand=True)

        # declare components
        (self.files_list_frame,
         self.path_text_box,
         self.go_up_btn,
         self.go_forward_btn,
         self.go_back_btn,
         self.go_home_btn,
         self.path_nav_frame,
         self.main_container,
         self.sidebar_content,
         self.logo_label,
         self.sidebar_frame,
         self.option_menu) = None, None, None, None, None, None, None, None, None, None, None, None,

        self.home_path = self.get_os_home_path()

        self.file_list = []
        self.curr_dir = self.home_path
        self.items_ref = []
        self.selected_item = None
        self.file_properties_values = ['Open', 'Open with', 'Copy', 'Cut', 'Delete', 'Add to safe', 'Properties']
        self.folder_properties_values = ['Open', 'Open with', 'Copy', 'Cut', 'Delete',
                                         'Add Folder to safe', 'Properties']

        self.create_components()

        self.populate_file_list_frame()

    def create_components(self):
        self.sidebar_frame = XSidebar(self)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # file container
        self.main_container = XFrame(self, width=300, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=(10, 0), pady=(20, 0), sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)

        self.path_nav_frame = XFrame(self.main_container, fg_color="gray")
        self.path_nav_frame.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.path_nav_frame.grid_columnconfigure(4, weight=1)

        self.go_back_btn = ctk.CTkButton(self.path_nav_frame, width=10, text="<-", command=self.smtn)
        self.go_back_btn.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))

        self.go_forward_btn = ctk.CTkButton(self.path_nav_frame, width=10, text="->", command=self.smtn)
        self.go_forward_btn.grid(row=0, column=1, padx=(0, 0), pady=(0, 0))

        self.go_up_btn = ctk.CTkButton(self.path_nav_frame, width=10, text="^", command=self.go_up)
        self.go_up_btn.grid(row=0, column=2, padx=(0, 0), pady=(0, 0))

        self.go_home_btn = ctk.CTkButton(self.path_nav_frame, width=10, text="Home", command=self.go_home)
        self.go_home_btn.grid(row=0, column=2, padx=(0, 0), pady=(0, 0))

        # path text entry
        self.path_text_box = ctk.CTkEntry(self.path_nav_frame, textvariable=tk.StringVar(value=self.curr_dir),
                                          width=500)
        self.path_text_box.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # files in dir
        self.files_list_frame = XScrollableFrame(self.main_container, width=200, height=700, fg_color="gray",
                                                 corner_radius=0)
        self.files_list_frame.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.files_list_frame.grid_columnconfigure(5, weight=0)

    def smtn(self):
        pass

    def go_up(self):
        parent_path = os.path.dirname(self.curr_dir)  # Get the parent directory path
        if os.path.isdir(parent_path):  # Check if the parent directory exists
            self.curr_dir = parent_path  # Update the current path to the parent directory
            self.clean_file_list()
            self.populate_file_list_frame(self.curr_dir)

    def go_home(self):
        self.curr_dir = self.home_path
        self.clean_file_list()
        self.populate_file_list_frame(self.curr_dir)

    def populate_file_list(self, path=None):
        if path is None:
            path = self.curr_dir

        for item in os.listdir(path):
            self.file_list.append(item)

    def clean_file_list(self):
        self.file_list = []

    def clear_items(self):
        for item in self.items_ref:
            item.pack_forget()
            item.destroy()

        self.items_ref = []

    def populate_file_list_frame(self, path=None):
        self.populate_file_list(path)
        self.clear_items()

        self.files_list_frame.scrollable_frame.update_idletasks()
        self.files_list_frame.pack_propagate(0)
        self.files_list_frame.scrollable_frame.update_idletasks()
        self.files_list_frame.canvas.yview_moveto(0)

        for index, item in enumerate(self.file_list):
            devices_frame = ctk.CTkFrame(self.files_list_frame.scrollable_frame)
            devices_frame.configure(bg_color="white")
            item_label = ctk.CTkLabel(devices_frame, text=f" {item} ")
            item_label.bind("<Button-1>", lambda event, x_item=item: self.select_item(x_item, event))
            item_label.bind("<Double-Button-1>", lambda event, x_item=item: self.open(x_item, event))
            item_label.bind("<Button-3>", lambda event, x_item=item: self.show_options(x_item, event))
            item_label.pack(side=tk.LEFT)

            # Pack the directory item component
            devices_frame.pack(fill=tk.X, padx=5, pady=5)
            self.items_ref.append(devices_frame)

    def show_options(self, item, event):
        print(self.curr_dir)
        print(f"{item} right clicked, event: {event}")

        if self.is_directory(os.path.join(self.curr_dir, item)):
            values = self.folder_properties_values
        else:
            values = self.file_properties_values

        self.option_menu = tk.Menu(self.files_list_frame, bg="black", fg="white", tearoff=0)
        self.option_menu.delete(0, tk.END)

        for x in values:
            self.option_menu.add_command(label=f" {x} ",
                                         command=lambda c=x:
                                         self.option_selected(x_item=item, action=c))

        self.option_menu.tk_popup(event.x_root, event.y_root)

    def option_selected(self, x_item, action):
        item_path = os.path.join(self.curr_dir, x_item)
        if action == "Open":
            if os.path.isdir(item_path):
                self.open_dir(x_item)
            else:
                self.open_file(x_item)
                print(f"open file {x_item}")
        elif action == "Open with":
            if os.path.isdir(item_path):
                self.open_dir(x_item)
            else:
                self.open_file_with(x_item)
            print(f"Open {x_item} with...")
        elif action == "Copy":
            print(f"copy {x_item}")
        elif action == "Cut":
            print(f"Delete {x_item}")
        elif action == "delete":
            print(f"delete {x_item}")
        elif action == 'Add to safe':
            self.add_to_xcrypt_safe(x_item)
        elif action == 'Properties':
            details = self.file_details(os.path.join(self.curr_dir, x_item))
            XItemProperties(self.master, file_details=details)
        else:
            print(f"item: {x_item}, option: {action}")

    def select_item(self, item, event=None):

        # Unselect the previously selected item
        if self.selected_item is not None:
            for frame in self.items_ref:
                frame.configure(bg_color="white")
                frame.update()
            self.selected_item = None

        # Set the background color of the selected item to blue
        selected_frame = event.widget.master
        selected_frame.configure(bg_color="blue")
        selected_frame.update_idletasks()

        # Set the selected item
        self.selected_item = item
        print(self.selected_item)

    def open_dir(self, item, event=None):
        print(f"{item} left clicked, event: {event}")

        self.curr_dir = os.path.join(self.curr_dir, item)
        print(self.curr_dir)
        self.clean_file_list()

        # print(f"items_list: {self.items_ref}")
        self.populate_file_list_frame(path=self.curr_dir)

    def open_file(self, item, event=None):
        file = os.path.join(self.curr_dir, item)
        if file:
            subprocess.run(['xdg-open', file])

    def open(self, item, event=None):
        item_path = os.path.join(self.curr_dir, item)
        if self.is_directory(item_path):
            self.open_dir(item)
        else:
            self.open_file(item)

    def open_file_with(self, item, event=None):
        initial_dir = ''
        file_path = os.path.join(self.curr_dir, item)
        system = platform.system()
        if system == 'Windows':
            initial_dir = 'C:/Program Files'
        elif system == 'Darwin':
            initial_dir = '/Applications'
        elif system == 'Linux':
            initial_dir = '/usr/bin'
        if file_path:
            app_path = filedialog.askopenfilename(initialdir=initial_dir)
            if app_path:
                subprocess.run([app_path, file_path])  # Open the file with the chosen application

    def add_to_xcrypt_safe(self, item, event=None):
        result = messagebox.askyesno("Confirm", f"Do you want to add {item} to safe?")
        if result:
            file = os.path.join(self.curr_dir, item)
            x = XCrypt()
            try:
                x.encrypt_file(file_path=file)
                messagebox.showinfo("XCrypted", "File is in secure safe")
            except IOError as err:
                print(err)

        else:
            return

    @staticmethod
    def get_os_home_path():
        system = platform.system()
        if system == 'Windows':
            home_path = os.path.expanduser("~")
        elif system == 'Linux' or system == 'Darwin':
            home_path = os.path.expanduser("~")
        else:
            home_path = None

        return home_path

    @staticmethod
    def file_details(filename):
        file_stat = os.stat(filename)
        file_size = file_stat.st_size
        creation_time = file_stat.st_ctime
        modification_time = file_stat.st_mtime
        access_time = file_stat.st_atime
        permissions = file_stat.st_mode
        is_directory = stat.S_ISDIR(permissions)

        mime = {
            'filename': filename,
            'size': file_size,
            'creation_time': datetime.datetime.fromtimestamp(creation_time),
            'modification_time': datetime.datetime.fromtimestamp(modification_time),
            'access_time': datetime.datetime.fromtimestamp(access_time),
            'permissions': permissions,
            'is_directory': is_directory
        }
        return mime

    def is_directory(self, filename):
        mime = self.file_details(filename=filename)
        return mime['is_directory']

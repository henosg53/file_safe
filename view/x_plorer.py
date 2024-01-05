import platform

import tkinter as tk
from tkinter import ttk
import os
import stat
import datetime
import customtkinter as ctk

from model.x_frame import XFrame


class XSidebar(XFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
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

        places_label = ctk.CTkLabel(self.sidebar_content, text="Places", font=ctk.CTkFont(size=15, weight="bold"))
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

    @staticmethod
    def left_clicked(folder):
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
         self.path_nav_frame,
         self.main_container,
         self.sidebar_content,
         self.logo_label,
         self.sidebar_frame,
         self.option_menu) = None, None, None, None, None, None, None, None, None, None, None,

        self.home_path = self.get_os_home_path()

        self.file_list = []
        self.curr_dir = self.home_path
        self.items_ref = []

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
            item_label = ctk.CTkLabel(devices_frame, text=item)
            item_label.bind("<Button-1>", lambda event, x_item=item: self.open_dir(x_item, event))
            item_label.bind("<Button-3>", lambda event, x_item=item: self.show_options(x_item, event))
            item_label.pack(side=tk.LEFT)

            # Pack the directory item component
            devices_frame.pack(fill=tk.X, padx=5, pady=5)
            self.items_ref.append(devices_frame)

    def show_options(self, item, event):
        print(self.curr_dir)
        print(f"{item} right clicked, event: {event}")
        op_var = tk.StringVar(value="op 2")
        values = ['op 1', 'op 2']
        self.option_menu = tk.Menu(self.files_list_frame, tearoff=0)
        self.option_menu.delete(0, tk.END)

        def option_selected(x_item, option):
            properties_toplevel = tk.Toplevel(self.master, height=500)
            properties_toplevel.title("Properties")
            properties_toplevel.geometry(f"{500}x{300}")
            details = self.file_details(self.curr_dir+f"/{item}")

            for i, (key, value) in enumerate(details.items()):
                label = tk.Label(properties_toplevel, text=f"{key}: {value}")
                label.pack(anchor=tk.W)

            print(f"item: {x_item}, option: {option}")

        for x in values:
            self.option_menu.add_command(label=f"{x} for {item}", command=lambda: option_selected(item, x))

        self.option_menu.tk_popup(event.x_root, event.y_root)

    def open_dir(self, item, event):
        print(f"{item} left clicked, event: {event}")

        self.curr_dir = os.path.join(self.curr_dir, item)
        print(self.curr_dir)
        self.clean_file_list()

        print(f"items_list: {self.items_ref}")

        self.populate_file_list_frame(path=self.curr_dir)

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

        details = {
            'filename': filename,
            'size': file_size,
            'creation_time': datetime.datetime.fromtimestamp(creation_time),
            'modification_time': datetime.datetime.fromtimestamp(modification_time),
            'access_time': datetime.datetime.fromtimestamp(access_time),
            'permissions': permissions,
            'is_directory': is_directory
        }
        return details



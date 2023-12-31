import tkinter as tk
from junk.main_controller import SideBarController


class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.label = tk.Label(self, text="Side bar")
        self.label.pack()
        self.check_btn = tk.Button(self, text="Click here", command=self.handle_click)
        self.check_btn.pack()

    def set_controller(self, controller):
        self.controller = controller

    def handle_click(self):
        self.controller.handle_button_click()

    def update_label(self, text):
        self.label.config(text=f"{text}")


class NavBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.menu_bar = tk.Menu(self)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.do_nothing)
        file_menu.add_command(label="Open", command=self.do_nothing)
        file_menu.add_command(label="Save", command=self.do_nothing)
        file_menu.add_command(label="Save Us", command=self.do_nothing)
        file_menu.add_command(label="Close", command=self.do_nothing)

        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=parent.quit)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.do_nothing)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.do_nothing)
        edit_menu.add_command(label="Copy", command=self.do_nothing)
        edit_menu.add_command(label="Paste", command=self.do_nothing)
        edit_menu.add_command(label="Delete", command=self.do_nothing)
        edit_menu.add_command(label="Select All", command=self.do_nothing)

        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index", command=self.do_nothing)
        help_menu.add_command(label="About", command=self.do_nothing)
        self.menu_bar.add_cascade(label="HSidebarelp", menu=help_menu)
        parent.config(menu=self.menu_bar)

    def set_controller(self, controller):
        self.controller = controller

    def do_nothing(self):
        pass


class MainFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.label = tk.Label(self, text="Hello click the button")
        self.label.pack()

        self.sidebar = NavBar(self)
        self.sidebar.pack()

        sidebar_controller = SideBarController(model="", view=self.sidebar)
        self.sidebar.set_controller(sidebar_controller)

        self.button = tk.Button(self, text="click me",
                                command=self.handle_button_click)
        self.button.pack(pady=5)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def update_counter_label(self, value):
        self.label.config(text=f"counter: {value}")

    def handle_button_click(self):
        self.controller.handle_button_click()

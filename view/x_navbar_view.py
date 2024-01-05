import tkinter as tk
from view.view import View


class NavBar(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = None

        self.menu_bar = tk.Menu(self)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="XCrypt Safe", command=self.home)
        file_menu.add_command(label="New Window", command=self.xplorer)
        file_menu.add_command(label="Create Folder", command=self.do_nothing)
        file_menu.add_command(label="Properties", command=self.do_nothing)

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

        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Icon View", command=self.do_nothing)
        view_menu.add_command(label="List View", command=self.do_nothing)
        view_menu.add_command(label="Compact View", command=self.do_nothing)

        self.menu_bar.add_cascade(label="View", menu=view_menu)

        go_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Go", menu=go_menu)

        bookmarks_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Bookmarks", menu=bookmarks_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Appearance", command=self.do_nothing)
        help_menu.add_command(label="About", command=self.about)
        help_menu.add_command(label="Configuration", command=self.configuration)

        self.menu_bar.add_cascade(label="Help", menu=help_menu)

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

    def about(self):
        self.controller.about_page()

    def home(self):
        self.controller.home_page()

    def xplorer(self):
        self.controller.xplorer_page()

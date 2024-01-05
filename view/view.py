import tkinter as tk


class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = None
        # self.create_components()

    def create_components(self):
        pass

    def set_controller(self, controller):
        self.controller = controller

    def get_controller(self):
        return self.controller

    def get_parent(self):
        return self.parent

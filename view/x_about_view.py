import tkinter as tk


class AboutView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = None
        self.create_components()

    def create_components(self):
        title = tk.Label(self, text="About XCrypt", font="forte 20 bold")
        title.pack()

import tkinter as tk
from view.x_view import XView
from controller.x_controller import XController
from model.xcrypt import XCrypt


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("XCrypt")
        self.screen_height = 500
        self.screen_width = 750
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        self.configure(bg="darkgray",
                       padx=5, pady=5,
                       height=self.screen_height, width=self.screen_width)

        model = XCrypt
        view = XView(self)
        controller = XController(model=model, view=view)

        view.set_controller(controller=controller)
        view.pack()

        self.protocol("WM_DELETE_WINDOW", self.destroy)


if __name__ == "__main__":
    app = App()
    app.mainloop()

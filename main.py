import customtkinter as ctk
from view.x_view import XView
from controller.x_controller import XController
from model.xcrypt_model import XCrypt


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_default_color_theme("dark-blue")
        self.title("XCrypt")
        self.screen_height = 550
        self.screen_width = 800
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

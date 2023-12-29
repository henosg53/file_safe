import tkinter as tk
from view.main_frame import MainFrame
from controller.main_controller import MainController
from model.data_model import DataModel


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("XCrypt")
        self.geometry(f"{700}x{400}")
        model = DataModel()
        main_frame = MainFrame(self)
        controller = MainController(model=model, view=main_frame)

        main_frame.set_controller(controller=controller)
        main_frame.grid()


if __name__ == "__main__":
    app = App()
    app.mainloop()

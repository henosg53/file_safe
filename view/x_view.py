import tkinter as tk

from controller.x_controller import XController
from controller.x_navbar_controller import NavBarController
from model.xcrypt_model import XCrypt
from view.x_crypt_view import XCryptView
from view.x_navbar_view import NavBar
from view.x_about_view import AboutView
from view.x_config_view import ConfigView


class XView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.controller = None
        self.navbar = None
        self.navbar_controller = None

        self.main_view, self.main_view_controller, self.main_view_model = None, None, None
        self.home_view, self.home_view_controller, self.home_view_model = None, None, None
        self.config_view, self.config_view_controller, self.config_view_model = None, None, None
        self.about_view, self.about_view_controller, self.about_view_model = None, None, None

        self.create_components()

    def create_components(self):
        self.navbar = NavBar(self)
        self.navbar_controller = NavBarController(model="", view=self.navbar)
        self.set_component_controller(component=self.navbar, controller=self.navbar_controller)

        self.parent.config(menu=self.navbar.get_menu_bar())

        self.home_view = XCryptView(self)
        self.home_view_model = XCrypt()
        self.home_view_controller = XController(model=self.home_view_model, view=self.home_view)

        self.main_view = self.home_view
        self.set_component_controller(component=self.home_view, controller=self.home_view_controller)

        self.main_view.grid()

        self.config_view = ConfigView(self)
        self.about_view = AboutView(self)

    def set_controller(self, controller):
        self.controller = controller

    @staticmethod
    def set_component_controller(component, controller):
        component.set_controller(controller=controller)

    def change_main_view(self, view, controller=None):
        if self.main_view is not None:
            self.main_view.grid_remove()
        self.main_view = view

        if self.main_view is not None:
            self.main_view.grid()

        if controller is not None:
            self.set_component_controller(self.main_view, controller=controller)

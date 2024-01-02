from controller.controller import Controller
from controller.x_config_controller import ConfigController


class NavBarController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

    def configuration_page(self):
        view_controller = ConfigController(model="", view=self.view.parent.config_view)
        self.view.parent.change_main_view(view=self.view.parent.config_view,
                                          controller=view_controller)

        print("Switched to config page")

    def about_page(self):
        self.view.parent.change_main_view(view=self.view.parent.about_view)
        print("Switched to about page")

    def home_page(self):
        self.view.parent.change_main_view(view=self.view.parent.home_view)
        print("Switched to Home page")

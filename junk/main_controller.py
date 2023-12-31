class SideBarController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_button_click(self):
        self.view.update_label("Updated")


class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_button_click(self):
        self.model.increment_counter()
        counter_value = self.model.get_counter_value()
        self.view.update_counter_label(counter_value)

    def update_view(self, counter_value):
        self.view.update_counter_label(counter_value)

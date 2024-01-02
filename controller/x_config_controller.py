import bcrypt
import configparser
import os

from controller.controller import Controller


class ConfigController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

    def update_config(self):
        def encrypt_password(passwd):
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(passwd.encode(), salt)
            return hashed_password.decode()

        username = self.view.username.get()
        password = self.view.password.get()
        print(f"Username: {username} \nPassword: {password}")

        if self.view.is_field_empty(username):
            self.view.message_box.showerror(title="Error", message="Refill fields!")
            return

        elif self.view.is_field_empty(password):
            self.view.message_box.showerror(title="Error", message="Refill fields!")
            return

        else:
            config = configparser.ConfigParser()
            config["Profile"] = {
                'username': username,
                'password': encrypt_password(password)
            }
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)
            config_file_path = os.path.join(data_dir, "config.ini")

            with open(config_file_path, "w") as config_file:
                config.write(config_file)

            self.view.message_box.showinfo("Success", "Configuration saved!")

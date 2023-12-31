import os
import configparser
import bcrypt
import os


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view


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


class XController(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)

    def encrypt_file(self):
        file = self.view.select_file()
        if file:
            self.model.encrypt_file(file)
            self.view.message_box.showinfo("Encryption result", f"Encrypted file: {file}")
        else:
            self.view.message_box.showwarning("Empty input", "Please select a file to encrypt")

        self.view.populate_file_listbox()

    def decrypt_file(self):
        if self.view.selected_file:

            file_path = os.path.join(self.view.encrypted_files_path, self.view.selected_file)
            print(self.view.selected_file)
            decrypted_file_path = self.model.decrypt_file(file_path)
            self.view.message_box.showinfo("Decryption Result",
                                           f"File decrypted successfully. Decrypted file saved as: {decrypted_file_path}")

            self.view.populate_file_listbox()
        else:
            self.view.message_box.showwarning("No File Selected", "Please select a file to decrypt.")

    def delete_file(self):
        print(f"file to be deleted: {self.view.selected_file}")
        if self.view.selected_file:
            file_path = os.path.join(self.view.encrypted_files_path, self.view.selected_file)
            print(file_path)
            self.model.remove_file(file_path)
            self.view.message_box.showinfo("File Deleted", f"The file '{self.view.selected_file}' has been deleted.")

        else:
            self.view.message_box.showwarning("No File Selected", "Please select a file to delete.")

        self.view.populate_file_listbox()

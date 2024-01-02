import os
from controller.controller import Controller


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

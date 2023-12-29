import os


class NavBarController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def configuration_page(self):
        self.view.parent.main_view.title.config(text="Hello")
        print("Configurations page")


class XController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def import_file(self):
        pass

    def encrypt_file(self):
        file = self.view.select_file()
        if file:
            self.model.encrypt_file(file)
            self.view.message_box.showinfo("Encryption result", f"Encrypted file: {file}")
        else:
            self.view.message_box.showwarning("Empty input", "Please select a file to encrypt")

        self.view.populate_file_listbox()

    def decrypt_file(self):
        selected_indices = self.view.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_file = self.view.file_listbox.get(selected_index)
            file_path = os.path.join(self.view.encrypted_files_path, selected_file)
            print(selected_file)
            decrypted_file_path = self.model.decrypt_file(file_path)
            self.view.message_box.showinfo("Decryption Result",
                                           f"File decrypted successfully. Decrypted file saved as: {decrypted_file_path}")

            self.view.file_listbox.delete(selected_index)  # Remove the decrypted file from the listbox
            self.view.populate_file_listbox()
        else:
            self.view.message_box.showwarning("No File Selected", "Please select a file to decrypt.")

    def delete_file(self):
        selected_indices = self.view.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_file = self.view.file_listbox.get(selected_index)
            file_path = os.path.join(self.view.encrypted_files_path, selected_file)

            print(file_path)
            self.model.remove_file(file_path)
            self.view.message_box.showinfo("File Deleted", f"The file '{selected_file}' has been deleted.")

            self.view.file_listbox.delete(selected_index)  # Remove the deleted file from the listbox
        else:
            self.view.message_box.showwarning("No File Selected", "Please select a file to delete.")

        self.view.populate_file_listbox()

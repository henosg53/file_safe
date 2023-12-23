import json
import os
from xcrypt import XCrypt 
import tkinter as tk
from tkinter import messagebox,filedialog,Tk,dialog


class XCryptUI:
    def __init__(self):
        # password validation
        self.validate_user()

        self.crypt = XCrypt()
        self.root = tk.Tk()
        self.root.title("Crypt")
        self.screen_height = 500
        self.screen_width = 700
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        # self.encrypted_files_path = '.'
        self.encrypted_files_path = os.path.join(os.getcwd(),'data/file_secure/encrypted_files')
        self.key_storage_path = os.path.join(os.getcwd(),'data/file_secure/key_storage.json')
        self.create_secure_directory(self.encrypted_files_path)

        self.text_entry = tk.Label(self.root, text='Crypt File Safe', width=50)
        self.text_entry.pack(padx=10, pady=10)

        # self.encrypted_files_path = '.'
        self.encrypted_files_path = os.path.join(os.getcwd(),'data/file_secure/encrypted_files')

        self.encrypt_button = tk.Button(self.root, text="Import File", command=self.encrypt)
        self.encrypt_button.pack(pady=5)

        self.file_listbox = tk.Listbox(self.root, width=50)
        self.file_listbox.pack(padx=10, pady=10)

        self.populate_file_listbox()
        
        
        self.decrypt_button = tk.Button(self.root, text="Decrypt File", command=self.decrypt)
        self.decrypt_button.pack(pady=5)
                
        self.delete_button = tk.Button(self.root, text="Delete From Safe", command=self.delete_file)
        self.delete_button.pack(pady=5)
        
        

        self.root.mainloop()

    def validate_user(self):
        passwd = input("please enter password: ")
        if passwd == "soul":
            return
        else:
            exit()

    def create_secure_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            
            key = {}

            with open(self.key_storage_path, 'w') as file:
                json.dump(key, file)

            print("path and key storage file created")
        else:
            print("secure path exists! ")

    # file dialog box
    def select_file(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    # populate listbox     
    def populate_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for filename in os.listdir(self.encrypted_files_path):
            file_path = os.path.join(self.encrypted_files_path, filename)
            if os.path.isfile(file_path):
                self.file_listbox.insert(tk.END, filename)

    # ecrypt file 
    def encrypt(self):
        file = self.select_file()
        if file:
            encrypted_file = self.crypt.encrypt_file(file)
            messagebox.showinfo("Encryption Result", f"Encrypted file: {encrypted_file}")
        else:
            messagebox.showwarning("Empty Input", "Please enter file to encrypt.")
        
        self.populate_file_listbox()
    
    # decrypt selected encrypted file
    def decrypt(self):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_file = self.file_listbox.get(selected_index)
            file_path = os.path.join(self.encrypted_files_path, selected_file)
            print(selected_file)
            decrypted_file_path = self.crypt.decrypt_file(file_path)
            messagebox.showinfo("Decryption Result", f"File decrypted successfully. Decrypted file saved as: {decrypted_file_path}")
            
            self.file_listbox.delete(selected_index)  # Remove the decrypted file from the listbox
            self.populate_file_listbox()
        else:
            messagebox.showwarning("No File Selected", "Please select a file to decrypt.")
        
        
    # remove encrypted file from file safe
    def delete_file(self):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_file = self.file_listbox.get(selected_index)
            file_path = os.path.join(self.encrypted_files_path, selected_file)
            
            print(file_path)
            os.remove(file_path)
            messagebox.showinfo("File Deleted", f"The file '{selected_file}' has been deleted.")
            
            self.file_listbox.delete(selected_index)  # Remove the deleted file from the listbox
        else:
            messagebox.showwarning("No File Selected", "Please select a file to delete.")
        
        self.populate_file_listbox()


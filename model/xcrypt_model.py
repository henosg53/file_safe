from cryptography.fernet import Fernet
import json
import os
import base64


class XCrypt:

    def __init__(self, file_safe_dir=None, key_storage_file=None) -> None:

        # key storage file location
        if file_safe_dir is None:
            self.file_safe_dir = 'data/file_secure/encrypted_files'
        else:
            self.file_safe_dir = file_safe_dir

        if key_storage_file is None:
            self.key_storage_file = 'data/file_secure/key_storage.json'
        else:
            self.key_storage_file = key_storage_file

        self.key_storage = {}

    # generate keys
    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    # encrypt file
    def encrypt_file(self, file_path, key=None):
        with open(file_path, 'rb') as file:
            data = file.read()

        if key is None:
            key = self.generate_key()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        encrypted_data = self.blob(encrypted_data)

        # Get the filename and extension
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]

        new_file_path = os.path.join(self.file_safe_dir, f"encrypted_{file_name}")

        with open(new_file_path, 'wb') as file:
            file.write(encrypted_data)

        # encrypted_data = Enc().file_to_blob(file_path=new_file_path,output_path=new_file_path+'.blob')

        # remove original file
        os.remove(file_path)

        # store encryption key
        self.store_key(filename=new_file_path, key=key)

    # decrypt file
    def decrypt_file(self, file_path, key=None):
        # Enc().blob_to_file(file_path=file_path,output_path=file_path[:5])
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        if key is None:
            relative_file_path = file_path.split("file_safe/")[1]
            print(relative_file_path)
            key = self.retrieve_key(relative_file_path)
            print(f"file: {relative_file_path} retrived:{key}")

        if key is None:
            raise ValueError("Key not found for the encrypted file.")

        fernet = Fernet(key)
        encrypted_data = self.unblob(encrypted_data)
        decrypted_data = fernet.decrypt(encrypted_data)

        original_filename = os.path.basename(file_path)[10:]  # Remove the 'encrypted_' prefix
        # print(original_filename)

        new_file_path = os.path.join(os.getcwd(), f"decrypted_{original_filename}")

        with open(new_file_path, 'wb') as file:
            file.write(decrypted_data)

        return new_file_path

    # store key to key storage json file    
    def store_key(self, filename, key):
        # Load existing keys from the JSON file
        if os.path.exists(self.key_storage_file):
            with open(self.key_storage_file, "r") as file:
                try:
                    self.key_storage = json.load(file)
                except json.JSONDecodeError:
                    self.key_storage = {}
        else:
            print('file doesnt exist')
            self.key_storage = {}

        # Store the new key in the dictionary
        key_str = key.decode("utf-8")
        self.key_storage[filename] = key_str

        # Write the updated key storage to the JSON file
        with open(self.key_storage_file, "w") as file:
            json.dump(self.key_storage, file)

    # fetch key if exists in key storage json file
    def retrieve_key(self, filename):
        # Load the keys from the JSON file
        if os.path.exists(self.key_storage_file):
            with open(self.key_storage_file, "r") as file:
                try:
                    self.key_storage = json.load(file)
                    key_str = self.key_storage.get(filename)
                    # print(key_str)
                    if key_str is not None:
                        # return key_str
                        # Convert the key back to bytes
                        key = key_str.encode("utf-8")
                        return key
                    else:
                        return None
                except json.decoder.JSONDecodeError:
                    return None
        else:
            return None

    def remove_key(self, filename):
        if os.path.exists(self.key_storage_file):
            with open(self.key_storage_file, "r") as file:
                try:
                    self.key_storage = json.load(file)
                    key_str = self.key_storage.get(filename)

                    if key_str is not None:
                        print(f"key string: {key_str} deleted")
                        self.key_storage.pop(filename, None)
                        with open(self.key_storage_file, 'w') as write_file:
                            json.dump(self.key_storage, write_file)

                        print(f"key storage: {self.key_storage} updated!")
                        # remove the key_str here...
                        key = key_str.encode("utf-8")
                        return key
                    else:
                        return None
                except json.decoder.JSONDecodeError:
                    return None
        else:
            return None

    def remove_file(self, filename):
        os.remove(filename)
        # modify the file path
        relative_path = os.path.relpath(filename, start='file_safe')
        if relative_path.startswith('..') or relative_path.startswith('home'):
            filename = relative_path[3:]

        print(f"file path: {filename}")
        # remove key from json file
        self.remove_key(filename)

    @staticmethod
    def blob(data):
        return base64.b64encode(data)

    @staticmethod
    def unblob(data):
        return base64.b64decode(data)

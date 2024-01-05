import base64
import stat
import datetime
import os
import gzip
import magic


class File:

    def __init__(self, filename=None):
        self.filename = filename
        self.content = None
        self.metadata = None

    def read(self):
        with open(self.filename, 'rb') as file:
            return file.read()

    def write(self, data):
        try:
            with open(self.filename, 'w') as f:
                f.write(data)
            print(f"Data written to file '{self.filename}' successfully.")
        except OSError as e:
            print(f"Error writing to file '{self.filename}': {e}")

    def compress(self):
        compressed_filename = self.filename + '.gz'
        with open(self.filename, 'rb') as file_in, gzip.open(compressed_filename, 'wb') as file_out:
            file_out.writelines(file_in)

    def decompress(self):
        decompressed_filename = self.filename[:-3]  # Remove '.gz' extension
        with gzip.open(self.filename, 'rb') as file_in, open(decompressed_filename, 'wb') as file_out:
            file_out.writelines(file_in)

    def file_details(self):
        file_stat = os.stat(self.filename)
        file_size = file_stat.st_size
        creation_time = file_stat.st_ctime
        modification_time = file_stat.st_mtime
        access_time = file_stat.st_atime
        permissions = file_stat.st_mode
        is_directory = stat.S_ISDIR(permissions)

        details = {
            'filename': self.filename,
            'size': file_size,
            'creation_time': datetime.datetime.fromtimestamp(creation_time),
            'modification_time': datetime.datetime.fromtimestamp(modification_time),
            'access_time': datetime.datetime.fromtimestamp(access_time),
            'permissions': permissions,
            'is_directory': is_directory
        }
        return details

    def to_blob(self, output_path):
        with open(self.filename, 'rb') as file:
            blob = base64.b64encode(file.read())
        with open(output_path, 'wb') as file:
            file.write(blob)

    @staticmethod
    def file_exists(file_path) -> bool:
        exists = os.path.exists(file_path)
        return exists
        # print(f"File '{file_path}' exists: {exists}")

    def get_dir(self):
        return os.getcwd()

    def set_permissions(self, permissions):
        try:
            os.chmod(self.filename, permissions)
            return permissions
        except OSError as e:
            return e

    def get_permissions(self):
        try:
            metadata = os.stat(self.filename)
            return stat.filemode(metadata.st_mode)
        except OSError as e:
            return e

    def get_metadata(self):

        # print(magic.from_file(self.filename, mime=True))
        try:
            metadata = os.stat(self.filename)
            print(f"Metadata for file '{self.filename}':")
            print(f"Size: {metadata.st_size} bytes")
            print(f"Encoding: {magic.from_file(self.filename)}")
            print(f"Modified Time: {datetime.datetime.fromtimestamp(metadata.st_mtime)}")
            # print(f"Modified Time: {datetime.datetime.fromtimestamp(metadata.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Mime: {magic.from_file(self.filename, mime=True)}")
            print(f"Permissions: {stat.filemode(metadata.st_mode)}")


        except OSError as e:
            print(f"Error getting metadata for file '{self.filename}': {e}")

    @staticmethod
    def is_image(file_path):
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type.startswith('image/')

    @staticmethod
    def is_video(file_path):
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type.startswith('video/')
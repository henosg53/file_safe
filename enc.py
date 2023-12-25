import sys
import base64
import subprocess
import os

from blob_video_format import BlobVideoPlayer


class Enc:
    def __init__(self) -> None:
        pass

    # change file to blob
    def file_to_blob(self, file_path, output_path):
        with open(file_path, 'rb') as file:
            blob = base64.b64encode(file.read())
        with open(output_path, 'wb') as file:
            file.write(blob)

    # change blob to file
    def blob_to_file(self, file_path, output_path):
        with open(file_path, 'rb') as file:
            blob = file.read()
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(blob))

    # download video from url
    def download_video(self, url, output_path):
        command = ['youtubedl-gui', url, '-o', output_path]
        subprocess.call(command)

    # delete file 
    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")

    # play blob
    def play_blob(self, blob_path):
        # Convert the blob back to a video
        # video = self.blob_to_video_format(blob_path)
        video = BlobVideoPlayer.get_clip_from_blob(blob_path=blob_path)

        # Play the video
        video.preview()

    def play_video(self, video_path):
        video = BlobVideoPlayer.get_clip_from_video(video_path=video_path)

        # solve size issue here
        video.start()

    # print help output
    def print_help(self):
        help_text = """
        -_-_-_-_-_-_-_-[ ENC ]-_-_-_-_-_-_-
        
        Usage: python enc.py [flag] [input_file_path] [output_file_path]

        Options:
        -h, --help              Show this help message and exit.
        -b, --blob              Convert file to blob.
        -bd, --blobwithdel      Convert file to blob and delete the original file.
        -f, --file              Convert blob to file.
        -fd, --filewithdel      Convert blob to file and delete the blob.
        -u, --url               Download a video with youtubedl-gui and convert it to a blob.
        -pb, --playblob         Play blob directly.

        """
        print(help_text)

    def __str__(self):
        self.print_help()


if __name__ == '__main__':
    enc = Enc()

    flag = None
    input_file_path = None
    output_file_path = None

    # print(len(sys.argv))
    if len(sys.argv) == 3 and sys.argv[1] == '-pb' or sys.argv[1] == '--playblob' or sys.argv[1] == '-pv' or sys.argv[
        1] == '--playvideo':
        flag = sys.argv[1]
        input_file_path = sys.argv[2]

    elif len(sys.argv) < 4 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        enc.print_help()
        sys.exit(1)
    else:
        flag = sys.argv[1]
        input_file_path = sys.argv[2]
        output_file_path = sys.argv[3]

    if flag == '-b' or flag == '--blob':
        enc.file_to_blob(input_file_path, output_file_path)
        print("File converted to blob successfully.")

    elif flag == '-f' or flag == '--file':
        enc.blob_to_file(input_file_path, output_file_path)
        print("Blob converted to file successfully.")

    elif flag == '-bd' or flag == '--blobwithdelete':
        enc.file_to_blob(input_file_path, output_file_path)
        print("File converted to blob successfully.")
        enc.delete_file(input_file_path)
        print('Original file deleted')

    elif flag == '-fd' or flag == '--filewithdelete':
        enc.blob_to_file(input_file_path, output_file_path)
        print("Blob converted to file successfully.")
        enc.delete_file(input_file_path)
        print('blob deleted')

    elif flag == '-u' or flag == '--url':
        enc.download_video(input_file_path, output_file_path)
        enc.file_to_blob(output_file_path, input_file_path + '.txt')
        print("Video downloaded and converted to blob successfully.")

    elif flag == '-pb' or flag == '--playblob':
        print("starting blob player...")
        enc.play_blob(input_file_path)

    elif flag == '-pv' or flag == '--playvideo':
        print("starting blob player...")
        enc.play_video(input_file_path)

    else:
        print("Invalid flags. Please use --help for documentation.")
        sys.exit(1)

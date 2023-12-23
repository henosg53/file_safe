import base64
import tempfile
from moviepy.editor import VideoFileClip

class BlobVideoPlayer():
    
    def __init__(self) -> None:
        pass
    
    def get_clip_from_blob(blob_path):
        with open(blob_path, 'rb') as file:
            blob = file.read()
        video_data = base64.b64decode(blob)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        temp_file.write(video_data)
        temp_file.close()
        
        return VideoFileClip(temp_file.name) 
    
    def get_clip_from_video(video_path):
        with open(video_path, 'rb') as file:
            video_data = file.read()

        temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        temp_file.write(video_data)
        temp_file.close()

        return VideoFileClip(filename=temp_file.name)



if __name__ == '__main__':
    blob_path = './blob.txt'
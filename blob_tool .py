# from modules.file_management.blob import Enc
from enc import *
import sys

def main():

    enc = Enc()
    
    flag = None
    input_file_path=None
    output_file_path=None

    if (
            len(sys.argv) == 3 and 
            sys.argv[1] == '-pb' or sys.argv[1] == '--playblob' or 
            sys.argv[1] == '-pv' or sys.argv[1] == '--playvideo' or 
            sys.argv[1] == '-dv' or sys.argv[1] == '--downloadvid' 
        ):
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

    elif flag == '-dv' or flag == '--downloadvid':
        enc.download_video(input_file_path)
        # enc.file_to_blob(output_file_path, input_file_path + '.txt')
        # print("Video downloaded and converted to blob successfully.")
    
    elif flag == '-pb' or flag == '--playblob':
        print("starting blob player...")
        enc.play_blob(input_file_path)
    
    elif flag == '-pv' or flag == '--playvideo':
        print("starting blob player...")
        enc.play_video(input_file_path)

    else:
        print("Invalid flags. Please use --help for documentation.")
        sys.exit(1)



if __name__ == '__main__':
    main()
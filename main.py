import argparse
import sys
import os
import audio_metadata
from audio_metadata.formats.mp3 import MP3
from audio_metadata.formats.wave import WAVE

demo_file = "/home/leonidas/Downloads/'[FREE] BABY KEEM TYPE BEAT 2023 - LORE.mp3'"

class FileChecker:
    def __init__(self, args,file=None, file_type=None):
        try:
            self.file = file
            self.args = args
            self.file_type = file_type 
            self.metadata = None 

            if file == None:
                raise Exception("File not specified")
            if file_type == None:
                raise Exception("File type not specified")
            if self.check_file_type():
                if self.fileExists() and self.isFile():
                    self.print_file()
        except Exception as e:
            print(f"Error: {e}")

    def check_file_type(self):
        mydef = sys._getframe().f_code.co_name
        if self.file_type == "mp3":
            if self.file.endswith(".mp3"):
                return True
            else:
                return False
        elif self.file_type == "wav":
            if self.file.endswith(".wav"):
                return True
            else:
                return False
        else:
            print(f"The file type is not supported: {self.file_type}")
    
    def print_file(self):
        mydef = sys._getframe().f_code.co_name
        print("=====================================")
        print(f"Function: {mydef}")
        print(f"Path: {self.file}")
        print(f"File: {self.file.split('/')[-1]}")
        print("=====================================")
        print("=====================================")
        print("Metadata:")
        print("=====================================")
        format_file = self.determine_file_type()
        print(f"Format: {format_file}")
        if self.file_type == "mp3" and format_file == MP3:
           
            mp3_file = self.read_file(self.file)
            print("Your file is an mp3")
            print(f"MP3-INFO: {mp3_file}") 
        elif self.file_type == "wav" and format_file == WAVE:
            wav_file = self.read_file(self.file)
            print("Your file is an mp3")
            print(f"WAV: {wav_file}")
        else:
            raise Exception(f"Your file is not the type specified: {self.file_type}")


    def fileExists(self):
        mydef = sys._getframe().f_code.co_name
        try:
            if os.path.exists(self.file):
                return True
            else:
                raise FileNotFoundError(f"File does not exist: {self.file}")
        except FileNotFoundError as e:
            print(f"Error in {mydef}: {e}")
            return False

    def isFile(self):
        mydef = sys._getframe().f_code.co_name
        try:
            if os.path.isfile(self.file):
                return True
            else:
                raise FileNotFoundError(f"File is not a file: {self.file}")
        except FileNotFoundError as e:
            print(f"Error in {mydef}: {e}")
            return False

    def read_file(self, file):
        mydef = sys._getframe().f_code.co_name
        try:
            return audio_metadata.load(file)
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False
    
    def determine_file_type(self):
        mydef = sys._getframe().f_code.co_name
        try:
            if self.file.endswith(".mp3"):
                data = audio_metadata.determine_format(self.file)
                return data
            elif self.file.endswith(".wav"):
                data = audio_metadata.determine_format(self.file)
                return data
            else:
                raise Exception(f"File type not supported: {self.file_type}")
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False

def main(file, file_type, args):
    try:
        FileChecker(args, file, file_type)
    except Exception as e:
        print(f"Error in main: {e}")
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="The path of the file to check")
    parser.add_argument("-t", "--type", help="The type of file to check")
    parser.add_argument("-z", "--zip", help="Compress all files in a zip")
    parser.add_argument("-r", "--rename", help="Rename all files in a directory with this pattern: 'Name - Date - BPM - Key'")
    args = parser.parse_args()
    main(args.file, args.type, args)
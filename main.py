import argparse
import sys
import os
import audio_metadata

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
                print(f"File is an mp3: {self.file.split('/')[-1]}")
                return True
            else:
                print(f"File is not an mp3: {self.file.split('/')[-1]}")
                return False
        elif self.file_type == "wav":
            if self.file.endswith(".wav"):
                print(f"File is an wav: {self.file.split('/')[-1]}")
                return True
            else:
                print(f"File is not an wav: {self.file.split('/')[-1]}")
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
        self.metadata = self.read_file(format_file=format_file)

    def fileExists(self):
        mydef = sys._getframe().f_code.co_name
        try:
            if os.path.exists(self.file):
                print(f"File exists: {self.file}")
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

    def read_file(self, format_file):
        mydef = sys._getframe().f_code.co_name
        try:
            data = audio_metadata.load(self.file)
            print({"File": format_file == data})
            if format_file == data:
                return data
            else:
                raise Exception(f"File type not supported: {self.file_type}")
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False
    
    def determine_file_type(self):
        mydef = sys._getframe().f_code.co_name
        try:
            if self.file.endswith(".mp3"):
                data = audio_metadata.determine_format(self.file)
                return data.parse(self.file)
            elif self.file.endswith(".wav"):
                data = audio_metadata.determine_format(self.file)
                print(data.parse(self.file))  
                return data.parse(self.file)
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
    parser.add_argument("-t", "--file_type", help="The type of file to check")
    args = parser.parse_args()
    main(args.file, args.file_type, args)
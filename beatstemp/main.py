#!/usr/bin/env python3
import argparse
import sys
import os
import datetime
from pathlib import Path
import time
import audio_metadata
from audio_metadata.formats.mp3 import MP3
from audio_metadata.formats.wave import WAVE
import essentia.standard as es
import essentia.streaming as ess
import essentia
import click
from rich.console import Console
from rich.table import Table
from rich.live import Live
from zipfile import ZipFile, ZIP_DEFLATED
from utils.utils import ask_files

console = Console()

table = Table(show_header=True, header_style="bold magenta")

class FileChecker:
    def __init__(self, args,files: list=None, files_type=None):
        try:
            self.files = [files]
            self.args = args
            self.files_type = files_type 
            self.results = []
            if files_type == None:
                raise Exception("File type not specified")
            if files_type not in ["mp3", "wav"]:
                raise Exception("File type not supported")
            if files == None:
                self.files = ask_files()

            for file in self.files:
                if self.fileExist(file) and self.isFile(file):
                    if self.check_files_type(file):                        
                        self.print_file(file=file)

            if len(self.results) > 0:
                file_found = False
                files_to_zip = []
                if click.confirm('Do you want to rename the file?', default=False):
                    self.rename_file(self.results)
                if click.confirm('Do you want to zip the files?', default=False):
                    zip_name = click.prompt("Enter the name of the zip file: ", default="results")
                    for result in self.results:
                        if self.fileExist(result.get("full_path")):
                            file_found = True
                            data = {"path": result.get("full_path"), "name": result.get('new_name')}
                            files_to_zip.append(data)
                        elif self.fileExist(result.get("new_path")):
                            file_found = True
                            data = {"path": result.get("new_path"), "name": result.get('new_name')}
                            files_to_zip.append(data)
                    if file_found:
                        self.zip_files(files_to_zip, zip_name)
                self.generate_table(self.results)
            
        except Exception as e:
            print(f"Error: {e}")

    def fileExist(self, file):
        mydef = sys._getframe().f_code.co_name
        if os.path.exists(file):
            return True
        else:
            return False

    def isFile(self, file):
        mydef = sys._getframe().f_code.co_name
        try:
            if os.path.isfile(file):
                return True
            else:
                raise FileNotFoundError(f"File is not a file: {self.files}")
        except FileNotFoundError as e:
            print(f"Error in {mydef}: {e}")
            return False
        
    def check_files_type(self, file):
        mydef = sys._getframe().f_code.co_name
        if self.files_type == "mp3":
            if file.endswith(".mp3"):
                return True
        elif self.files_type == "wav":
            if file.endswith(".wav"):
                return True
            else:
                raise Exception (f"{self.files.split('/')[-1]} is not a {self.files_type} file")
        
    def read_file(self, file):
        mydef = sys._getframe().f_code.co_name
        try:
            return audio_metadata.load(file)
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False
    
    def determine_files_type(self, file):
        mydef = sys._getframe().f_code.co_name
        try:
            if file.endswith(".mp3"):
                data = audio_metadata.determine_format(file)
                return data
            elif file.endswith(".wav"):
                data = audio_metadata.determine_format(file)
                return data
            else:
                raise Exception(f"File type not supported: {self.files_type}")
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False
        
    def extract_bpm(self, file):
        audio = es.MonoLoader(filename=file)()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
        return round(bpm)
    
    def extract_key(self, file):
        # Initialize algorithms we will use.
        loader = ess.MonoLoader(filename=file)
        framecutter = ess.FrameCutter(frameSize=4096, hopSize=2048, silentFrames='noise')
        windowing = ess.Windowing(type='blackmanharris62')
        spectrum = ess.Spectrum()
        spectralpeaks = ess.SpectralPeaks(orderBy='magnitude',
                                        magnitudeThreshold=0.00001,
                                        minFrequency=20,
                                        maxFrequency=3500, 
                                        maxPeaks=60)
        # Use default HPCP parameters for plots.
        # However we will need higher resolution and custom parameters for better Key estimation.
        hpcp = ess.HPCP()
        hpcp_key = ess.HPCP(size=36, # We will need higher resolution for Key estimation.
                            referenceFrequency=440, # Assume tuning frequency is 44100.
                            bandPreset=False,
                            minFrequency=20,
                            maxFrequency=3500,
                            weightType='cosine',
                            nonLinear=False,
                            windowSize=1.)

        key = ess.Key(profileType='edma', # Use profile for electronic music.
                    numHarmonics=4,
                    pcpSize=36,
                    slope=0.6,
                    usePolyphony=True,
                    useThreeChords=True)

        # Use pool to store data.
        pool = essentia.Pool() 

        # Connect streaming algorithms.
        loader.audio >> framecutter.signal
        framecutter.frame >> windowing.frame >> spectrum.frame
        spectrum.spectrum >> spectralpeaks.spectrum
        spectralpeaks.magnitudes >> hpcp.magnitudes
        spectralpeaks.frequencies >> hpcp.frequencies
        spectralpeaks.magnitudes >> hpcp_key.magnitudes
        spectralpeaks.frequencies >> hpcp_key.frequencies
        hpcp_key.hpcp >> key.pcp
        hpcp.hpcp >> (pool, 'tonal.hpcp')
        key.key >> (pool, 'tonal.key_key')
        key.scale >> (pool, 'tonal.key_scale')
        key.strength >> (pool, 'tonal.key_strength')
        # Run streaming network.
        essentia.run(loader)
        return pool['tonal.key_key'] , pool['tonal.key_scale']

    def get_creationtime_file(self, file):
        mydef = sys._getframe().f_code.co_name
        try:
            return os.path.getctime(file)
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False

    def rename_file (self, files_data):
        mydef = sys._getframe().f_code.co_name
        try:
            for file in files_data:
                formatted_name = f"{file.get('file').split('.')[0]}-{file.get('bpm')}BPM-{file.get('key')}-{file.get('date')}"
                parent_dir = os.path.dirname(file.get('full_path'))
                console.print(f"Your can find your file here: {os.path.join(parent_dir, formatted_name)}.mp3")
              
                if self.files_type == "mp3":
                    if file.get('file'):
                        os.rename(file.get('full_path'), f"{os.path.join(parent_dir, formatted_name)}.mp3")
                elif self.files_type == "wav":
                    if file.get('file'):
                        os.rename(file.get('full_path'), f"{os.path.join(parent_dir, formatted_name)}.wav")

                    else:
                        raise Exception(f"File type not supported: {self.files_type}")
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False

    def print_file(self, file):
        mydef = sys._getframe().f_code.co_name
        console.print("=====================================")
        console.print(f"Path: {file}")
        console.print("=====================================")
        format_file = self.determine_files_type(file)
        creation_time = self.get_creationtime_file(file)
        creation_time_format = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
        key, scale = self.extract_key(file)
        bpm = self.extract_bpm(file)
        song_key = f"{key}{scale.capitalize()}"
        if self.files_type == "mp3" and format_file == MP3:        
            mp3_file = self.read_file(file)
            name_format = f"{mp3_file['filepath'].split('/')[-1].split('.')[0]}-{bpm}BPM-{song_key}-{creation_time_format}"
            console.print(f"Your file will be renamed to: {name_format}.mp3")
            self.results.append({"file": mp3_file['filepath'].split('/')[-1], 
                        "bpm": str(bpm),
                        "key": str(song_key),
                        "date": str(creation_time_format),
                        "full_path": mp3_file['filepath'],
                        "new_path": f"{os.path.dirname(mp3_file['filepath'])}/{mp3_file['filepath'].split('/')[-1].split('.')[0]}-{bpm}BPM-{song_key}-{creation_time_format}.mp3",
                      "new_name": f"{name_format}.mp3"})
        elif self.files_type == "wav" and format_file == WAVE:
            wav_file = self.read_file(file)
            name_format = f"{wav_file['filepath']}-{bpm}BPM-{song_key}-{creation_time_format}"
            console.print(f"Your file will be renamed to: {name_format}.wav")
            self.results.append({"file": wav_file['filepath'].split('/')[-1], 
                        "bpm": str(bpm),
                        "key": str(song_key),
                        "date": str(creation_time_format),
                        "full_path": wav_file['filepath'],
                        "new_path": f"{os.path.dirname(wav_file['filepath'])}/{wav_file['filepath'].split('/')[-1].split('.')[0]}-{bpm}BPM-{song_key}-{creation_time_format}.wav",
                        "new_name": f"{name_format}.wav"})
                    
        else:
            raise Exception(f"Your file is not the type specified: {self.files_type}")
        
    def generate_table(self, files):
        mydef = sys._getframe().f_code.co_name
        try:
            table.add_column("File")
            table.add_column("BPM")
            table.add_column("KEY")
            table.add_column("Creation Time")
            for file in files:
                 table.add_row(file.get('file'), 
                        file.get('bpm'),
                        file.get('key'),
                        file.get('date'))
            console.print(table)
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False
        
    def zip_files(self, files, zip_name):
        mydef = sys._getframe().f_code.co_name
        try:
            parent_dir = os.path.dirname(files[0].get('path'))
            with ZipFile(f"{os.path.join(parent_dir, zip_name)}.zip", 'w') as zipObj:
                for file in files:
                    zipObj.write(file.get('path'), arcname=file.get('name'))
                    print(f"File {file.get('path')} added to zip")
        except Exception as e:
            print(f"Error in {mydef}: {e}")
            return False


def main(file, files_type, args):
    try:
        FileChecker(args, file, files_type)
    except Exception as e:
        print(f"Error in main: {e}")
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="The path of the file to check")
    parser.add_argument("-t", "--type", help="The type of file to check")
    args = parser.parse_args()
    start_time = time.time()
    main(args.file, args.type, args)
    print("--- %s seconds ---" % round((time.time() - start_time), 3))
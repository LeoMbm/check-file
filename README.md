# Tools 


> In progress

## What ?

 - Check if file is really MP3 or WAV.
 - Rename it with Name-Date-BPM-KEY.
 - If Multiple files zip them
 - Give a name to the zip

## Why Not ?
- Browse Folder
- Send by email/wetransfer directly ?

## Installation

> In progress
## Usage

```
python3 main.py -f <Your absolute path to your file> -t <mp3 or wav required>

It will return you something like that:

[   INFO   ] MusicExtractorSVM: no classifier models were configured by default
=====================================
Path: /your/path/to/[FREE] 404 Billy Type Beat  Klan.mp3
=====================================
Your file will be renamed to: [FREE] 404 Billy Type Beat  Klan-76BPM-BbMajor-2023-03-08.mp3
Do you want to rename the file? [y/N]: y
Your can find your file here: /your/path/to/[FREE] 404 Billy Type Beat  Klan-76BPM-BbMajor-2023-03-08.mp3
Do you want to zip the files? [y/N]: y
Enter the name of the zip file:  [results]: 
File [FREE] 404 Billy Type Beat  Klan.mp3 added to zip


Or

python3 main.py -t <mp3 or wav required>

a Window Dialog will be open

Just select your files


```

## Help


```
options:
  -h, --help, show this help message and exit
  -f, --file, The path of the file to check
  -t, --type, The type of file to check - REQUIRED
```



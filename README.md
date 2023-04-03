# BeatsTemp

*Slogan cool to come*
## Table of Contents

- [Description](#description)
- [Features](#features)
- [Base](#base)
- [Installation](#installation)
- [Usage](#usage)
- [Help](#help)

## Description

This application allows composers to easily manage their music files. With just a few clicks, it is possible to check that the files are in mp3 or wav format, rename the files according to a specific format (Name-Date-BPM-Key), and compress multiple files at once. In the future, it may be possible to directly send the compressed files by email or wetransfer via the platform.

## Features

- Verification of file format (mp3 or wav)
- Automatic renaming of files according to the Name-Date-BPM-Key format
- Compression of multiple files at once

## Base

The application is divided into two parts: an online part that can be used with a web application and an offline part that can be used from the terminal.


## Installation
> At this moment, the script only works on Linux and MacOs. Some dependencies is not available on Windows. I'm working on it.

To install the application, please run the `install.sh` script located in the root directory of the project. This script will install the necessary dependencies and set up the application for use.
 <!-- > Windows: Run the following command: `./install.sh` in the root directory of the project. -->

> Linux/MacOs: Run the following command: `./install.sh` in the root directory of the project.
<!-- ## Installation
To install the application, follow these steps:

1. Make sure you have Python 3 installed on your computer. You can download it from [Python's official website](https://www.python.org/downloads/).
2. Clone the repository or download the ZIP file and extract it.
3. Navigate to the `beatstemp` directory in your terminal.
4. Run the following command: `./install.sh`
5. Once the installation is complete, you can run the application using the following command: `beatstemp`
6. If you encounter any issues during the installation process, feel free to open an issue on our [GitHub page](https://github.com/LeoMbm/check-file/issues). -->
## Usage

```
beatstemp -f <Your absolute path to your file> -t <mp3 or wav required>

It will return you something like that:

[   INFO   ] MusicExtractorSVM: no classifier models were configured by default
=====================================
Path: /your/path/to/file.mp3
=====================================
Your file will be renamed to: file-76BPM-BbMajor-2023-03-08.mp3
Do you want to rename the file? [y/N]: y
Your can find your file here: /your/path/to/file-76BPM-BbMajor-2023-03-08.mp3
Do you want to zip the files? [y/N]: y
Enter the name of the zip file:  [results]: 
File file.mp3 added to zip


Or

beatstemp -t <mp3 or wav required>

a Window Dialog will be open

Just select your files
```

## Help

```
usage: beatstemp [-h] [-f FILE] -t TYPE

arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The path of the file to check OPTIONAL
  -t TYPE, --type TYPE  The type of file to check - REQUIRED
  ```
## Ideas

- [ ] Add a GUI
- [ ] Add a web application
- [ ] Add a function to send the compressed files by email or wetransfer via the platform
- [ ] Add tests
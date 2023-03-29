@echo off

REM Vérifie si Python 3.10 et pip sont installés, sinon les installe automatiquement
python --version > nul 2>&1
if %errorlevel% neq 0 (
  echo Python 3.10 n'est pas installé. Téléchargement...
  powershell -Command "Invoke-WebRequest -OutFile python310.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
  echo Installation de Python 3.10...
  start /wait python310.exe /quiet InstallAllUsers=1 PrependPath=1
  SETX PATH "%PATH%;%USERPROFILE%\AppData\Local\Programs\Python310\python.exe" /M
) else (
    echo Python 3.10 est déjà installé.
)

pip --version 2>nul
if %errorlevel% neq 0 (
    echo pip n'est pas installé. Installation en cours...
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
    echo pip installé avec succès.
) else (
    echo pip est déjà installé.
)

cd /d %~dp0..
REM Installe le fichier .tar.gz depuis le dossier dist
echo Installation de l'application en cours...
cd dist
pip install beatstemp-0.1.tar.gz
cd ..
echo Installation terminée.

pause



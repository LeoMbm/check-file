#!/bin/bash

# Détection du système d'exploitation
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Installation de Python si nécessaire
    if ! command -v python &> /dev/null; then
        sudo apt-get update
        sudo apt-get install python3 -y
    fi
    
    # Installation de pip si nécessaire
    if ! command -v pip &> /dev/null; then
        sudo apt-get install python3-pip -y
    fi
    
    # Installation du package
    if [[ -e "dist/beatstemp-0.1.tar.gz" ]]; then
        pip install dist/beatstemp-0.1.tar.gz
    else
        echo "Le fichier dist/beatstemp-0.1.tar.gz n'existe pas"
        exit 1
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Installation de Python si nécessaire
    if ! command -v python &> /dev/null; then
        brew install python
    fi
    
    # Installation de pip si nécessaire
    if ! command -v pip &> /dev/null; then
        sudo easy_install pip
    fi
    
    # Installation du package
    if [[ -e "dist/beatstemp-0.1.tar.gz" ]]; then
        pip install dist/beatstemp-0.1.tar.gz
    else
        echo "Le fichier dist/beatstemp-0.1.tar.gz n'existe pas"
        exit 1
    fi
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Installation de Python si nécessaire
    if ! command -v python &> /dev/null; then
        choco install python -y
    fi
    
    # Installation de pip si nécessaire
    if ! command -v pip &> /dev/null; then
        python -m ensurepip --default-pip
    fi

    # Installation du package
    if [[ -e "dist/beatstemp-0.1.tar.gz" ]]; then
        pip install dist/beatstemp-0.1.tar.gz
    else
        echo "Le fichier dist/beatstemp-0.1.tar.gz n'existe pas"
        exit 1
    fi
    
else
    echo "Système d'exploitation non pris en charge: $OSTYPE"
    exit 1
fi

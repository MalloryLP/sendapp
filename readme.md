> [Mallory Lehuault-Parc](https://https://github.com/MalloryLP) - FIPA SE 2023

# Introduction

SendApp est un application de messagerie instantannée qui permet d'entretenir des conversations chifrées de bout en bout entre tous les utilisateurs.

# Installation

Copie des fichiers sources depuis Github :
```
git clone https://github.com/MalloryLP/sendapp.git
```

Mise en place de l'environnement sur Windows:

```powershell
python -m venv .venv
. .venv/Scripts/activate.ps1
pip install -r requirements.txt
```


# Lancement

Sur windows dans deux shells distincs :
```powershell
cd sendapp
python ./manage.py runsslserver --certificate ./sendapp/certif.pem --key ./sendapp/code.pem 0.0.0.0:8000
```

```powershell
cd sendapp
$env:DJANGO_SETTINGS_MODULE = 'sendapp.settings'
daphne -e ssl:8001:privateKey=./sendapp/code.pem:certKey=./sendapp/certif.pem sendapp.asgi:application
```
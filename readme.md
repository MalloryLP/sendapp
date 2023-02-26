![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/MalloryLP/sendapp)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/MalloryLP/sendapp/django)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/MalloryLP/sendapp/channels)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/MalloryLP/sendapp/django-sslserver)

> [Mallory Lehuault-Parc](https://github.com/MalloryLP) - FIPA SE 2023

## Introduction

SendApp est un application de messagerie instantannée qui permet d'entretenir des conversations chiffrées de bout en bout entre tous les utilisateurs.  

Vous pourrez retrouver dans le répertoire [doc](https://github.com/MalloryLP/sendapp/tree/main/doc) toutes les informations et les recherches liées à ce projet. Dans le répertoire [sendapp](https://github.com/MalloryLP/sendapp/tree/main/sendapp) se trouve les codes faisant fonctionner la messagerie. 

## Installation

Le projet ce base sur [Django](https://www.djangoproject.com/) qui est un framework web open source en Python. L'application utlise le protocole Websocket, le serveur fonctionne de paire avec [Daphne](https://github.com/django/daphne) qui est un serveur qui gère ce type de protocoles.

Copie des fichiers sources depuis Github :
```
git clone https://github.com/MalloryLP/sendapp.git
```

Le projet fonctionne avec Python et dépend de ces paquets :
- django
- channels
- django-sslserver

Mise en place de l'environnement virtuel Python sur Linux :
```shell
export PIPENV_VENV_IN_PROJECT=1
pipenv install -r requirements.txt
```
Lancement de l'environnement pipenv : `pipenv shell`

Mise en place de l'environnement virtuel Python sur Windows:
```powershell
$env:PIPENV_VENV_IN_PROJECT=1
python -m pipenv install -r ./requirements.txt
```
Lancement de l'environnement pipenv : `python -m pipenv shell`

## Lancement

Sur Linux dans deux shells pipenv distincs :
```shell
cd sendapp
python manage.py migrate --run-syncdb
python manage.py runsslserver --certificate sendapp/certif.pem --key sendapp/code.pem 0.0.0.0:8000
```

```shell
cd sendapp
export DJANGO_SETTINGS_MODULE = 'sendapp.settings'
daphne -e ssl:8001:privateKey=sendapp/code.pem:certKey=sendapp/certif.pem sendapp.asgi:application
```

Sur windows dans deux shells pipenv distincs :
```powershell
cd ./sendapp
python ./manage.py migrate --run-syncdb
python ./manage.py runsslserver --certificate ./sendapp/certif.pem --key ./sendapp/code.pem 0.0.0.0:8000
```

```powershell
cd ./sendapp
$env:DJANGO_SETTINGS_MODULE = 'sendapp.settings'
daphne -e ssl:8001:privateKey=./sendapp/code.pem:certKey=./sendapp/certif.pem sendapp.asgi:application
```

## Potentiels problèmes

Si vous rencontrez un problème lié aux modèles de données :
- Supprimez la base de données `db.sqlite3`
- Lancez la commande : `python ./manage.py migrate --run-syncdb`

Si vous avez besoin de créer un compte administrateur :
```shell
python ./manage.py createsuperuser
```

## Let's chat !

Allez à l'url suivante dans votre navigateur internet préféré sur smartphone :

```url
https://[host_machine_ip]:8000/home
```

Connectez-vous ou créez un compte, discutez :smiley:

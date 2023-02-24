# Les solutions techniques - Les websockets

Maintenant que nous sommes capable de générer des clées de chiffrement, chiffrer et déchiffrer des messages, il s'agirait de pouvoir les transmette au destinaire !

On voit directement le problème qui va arriver : comment faire en sorte que quand les utilisateurs sont en train de s'envoyer des messages, ceux-ci s'affiche en temps réel ?

Deux solutions :
- Actualiser la page `/chat` à intervalle de temps constant
- Utiliser les websockets

La première solution me parait trop simple et pas très élégante. Tandis que la seconde est beaucoup plus interessante techniquement. J'ai donc décidé de mettre en place le protocole websocket dans ce projet.

## Qu'est-ce que ce protocole ?

Le protocole WebSocket est un protocole de communication réseau bi-directionnel, conçu pour permettre une communication en temps réel entre un client (comme un navigateur web) et un serveur via une connexion TCP unique.

Il permet aux applications web de communiquer de manière plus efficace et en temps réel avec le serveur en évitant les limites du protocole HTTP, qui est principalement conçu pour une communication client-serveur unidirectionnelle.

En utilisant WebSocket, les applications web peuvent établir une connexion permanente avec le serveur et envoyer et recevoir des données en temps réel sans avoir besoin de rafraîchir la page ou de réenvoyer la demande à chaque fois. Cela permet une communication bidirectionnelle en temps réel, ce qui est utile pour des applications telles que les jeux en ligne, les salles de chat, la surveillance de l'état en temps réel...

<p align="center" width="100%">
    <img src="images/websocket.png" width="70%">  
</p>



## Mise en place du protocole

### Définitions

Dans un environement non sécurisé, Django peut prendre en charge la gestion des websockets. La méthode de developpement est décrite dans la documentation dans notre cas, elle doit être adaptée.

Dans le fichier de configuration `settings.py`, il faut ajouter :

```python
ASGI_APPLICATION = 'sendapp.asgi.application'

# LEARN CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
```

Ce code est lié à la configuration de Django Channels, qui est un paquetage tiers qui étend Django pour prendre en charge les WebSockets et autres protocoles asynchrones. Plus précisément, le code définit les couches d'application et de canal ASGI à utiliser par Django Channels.

ASGI (Asynchronous Server Gateway Interface) est une spécification d'interface pour les serveurs Web qui permettent une gestion asynchrone des demandes HTTP/HTTPS et des connexions WebSocket. ASGI fournit une interface unifiée pour gérer à la fois les connexions HTTP/HTTPS et WebSocket, ainsi que d'autres protocoles asynchrones.

Le paramètre ASGI_APPLICATION spécifie l'application ASGI à utiliser. Cela signifie que les canaux Django utiliseront l'attribut application du module sendapp.asgi comme point d'entrée pour le traitement des demandes ASGI.

Le paramètre CHANNEL_LAYERS spécifie les couches à utiliser pour gérer les connexions WebSocket. Dans le code donné, une seule couche est définie, qui est une couche de canal en mémoire avec le backend channels.layers.InMemoryChannelLayer. Cela signifie que Django Channels une couche en mémoire pour gérer les connexions WebSocket.

Maintenant, il faut définir un point d'accès pour maintenir la connexion entre le client et le serveur (principe du websocket). Ce point d'accès est défini dans le fichier `rooting.py` (fichier à créer) :

```python
from chat.consumers import PersonalChatConsumer

# ws : websocket
# wss : secure websocket

ws_urlpatterns = {
    path('wss/<int:id>/', PersonalChatConsumer.as_asgi())
}
```

Toutes les requêtes qui pointerons vers `wss/<int:id>/` seront envoyées à la couche `PersonalChatConsumer` (une sorte de vue) qui est définie dans le fichier `consumers.py`. Le `<int:id>` correspond à l'id de l'amis auquel on veut envoyer un mesage.

### Problème !

La partie précédente correspond à ce qui est décrit dans le documentation Django. Or, les requêtes sont en HTTPS, donc chiffrées. Pour établir la liaison entre un client et le serveur, plusieurs trames sont envoyées en début de communication pour définir le protocole. Django ne peut donc pas savoir qu'il s'agit du protocole websocket car il ne pourra pas les interpréter...

Après pas mal de recherches, j'ai découvert [Daphne](https://github.com/django/daphne). C'est un serveur ASGI qui permet de gérer les connexions WebSocket, HTTP/HTTPS et d'autres protocoles asynchrones pour les applications Python. Il est conçu pour fonctionner avec Django et d'autres frameworks. Daphne est utilisé par Django Channels comme serveur pour gérer les connexions. Pour faire simple, toutes les requêtes relatives aux websockets passeront par le serveur Daphne. 

Pour l'installer :

```shell
pip install daphne
```

Pour lancer le serveur Daphne :

```shell
daphne -e ssl:8001:privateKey=./sendapp/code.pem:certKey=./sendapp/certif.pem sendapp.asgi:application
```

on remarque les références au certificat SSL et à `ASGI_APPLICATION` dans la ligne de commande.

### Fonctionnement

Tout commence par le client, c'est lui qui doit initier la connexion websocket.

```javascript
const socket = new WebSocket(
    'wss://'
    + localip
    + ':8001'
    + '/ws/'
    + friend_id
    + '/'
);
```

```javascript
socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
    document.querySelector('#connection_status').innerHTML = `Connection établie`;
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
    document.querySelector('#connection_status').innerHTML = `Connection perdue`;
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
    document.querySelector('#connection_status').innerHTML = `Une erreur est survenue`;
}
```

```javascript
//Envoyer un message
socket.send();

//Reception d'un message
socket.onmessage = function(e){
};
```
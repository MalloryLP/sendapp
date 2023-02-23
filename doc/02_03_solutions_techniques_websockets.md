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

### Le modèle d'implémentation commun

### Implémentation de Daphne
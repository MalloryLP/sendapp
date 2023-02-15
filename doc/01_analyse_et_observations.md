# Rappel des objectifs

Il s'agissait de créer un système léger et autonome capable de :
- Procurer un service de messagerie instantanée (type [Treebal](https://www.treebal.green/)) mais à l'échelle d'un foyer
- Servir au maximum 25 utilisateurs
- Stocker localement les informations, c'est à dire pas dans un cloud, mais sur le système
- Garantir la confidentialité des données en les chiffrant sur les supports (disques, mémoires)
- Garantir une intimité numérique sur les réseaux de tous les services en les chiffrant de bout en bout
- Se connecter sur un point d'accès internet de type fibre à la maison
- De proposer une interface simple de configuration (éventuellement textuelle)

La plateforme de developpement peut être un PC sur Windows ou Linux. Il faudra vérifier que le projet fonctionne sur une carte Raspberry.

On se sert tous les jours de tels services, tels que Facebook Messenger ou Whatsapp. Ces services sont indispensables aujourd'hui. Leurs fonctionnement semblent identiques mais en réalité, les conversations sur Menssenger ne sont pas chiffrées pour le moment tandis que sur Whatsapp, c'est le cas. Ils fonctionnent au travers d'une application et proposent aussi une interface web. Pour faire la liaison entre les clients, ces services possèdent des serveurs par lequels transitent les données, chiffrées ou non.  
On imagine facilement que le projet nécessite d'un serveur web ou d'une api, cela va dépendre de l'interface utilisateur. Dans un premier temps, j'ai décidé de réaliser une application web, pour m'affranchir du developpement d'une application Android. Cela ne veut pas dire que ça sera plus simple. Au lieu d'avoir deux projets (API et application), le tout sera regroupé dans un seul et unique projet, un serveur web. Pour stocker les données des utilisateurs, il faut une base de données. On verra par le suite quel type de base de données correspond le mieux au projet. Concernant l'aspect sécurité, les algorithmes de chiffrement par clés partagées (chiffrement symétrique ou asymétrique) me semble les plus adaptés au projet car ils seront en capacité de garantir la confidentialité et l'intégrité des données transmises entre les utilisateurs. 

# Quelques projets déjà existants

Dans un premier temps, il s'agissait d'aller voir ce qu'il se faisait déjà sur internet. On retrouve plusieurs projets qui proposent des messageries instantannées assez évoluées basées sur des infrastructures différentes. Ayant choisi de developper une solution basée sur un serveur web, je me suis renseigné sur les différents types de framework web. Un framework web est un ensemble de bibliothèques, de composants et de guidelines qui aident les développeurs à créer des applications web de manière plus efficace et plus rapide dans plusieurs langages. Il en existe de nombreux, open source ou non.  

J'ai choisi de privilégier un framework web libre d'utilisation car :
- ils sont gratuit en général.
- ils sont plus fléxible que des solutions payantes. Cela semble indispensable si je veux pouvoir implémenter une solution de chiffrement.
- ils ont très souvent une communauté qui soutient le projet. Je pourrais trouver de l'aide facilement en cas de problème (même chose pour les solutions propriétaires).  

Les framework web open source les plus populaires actuellement sont :
- [Ruby on Rails (RoR)](https://rubyonrails.org/)
- [Django](https://www.djangoproject.com/)
- [Express](https://expressjs.com/fr/)
- [Node.js](https://nodejs.org/en/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- ...  

Voici quelques projets de messageries disponibles sur Github avec les frameworks cités :

| Projet | Infrastructure | Sécurité | 
|---------------|----------------|----------|
| [django-chat-channels](https://github.com/narrowfail/django-channels-chat)  | Django | Aucune |
| [RoR-Messenger](https://github.com/essaji/RoR-Messenger)  | Ruby on Rails | Aucune |
| [django-private-chat](https://github.com/Bearle/django_private_chat2) | Django  | Aucune  | 
| [flask-chatroom](https://github.com/ppd0705/flask_chatroom)  | Flask  | Aucune  | 
| [node-chat](https://github.com/igorantun/node-chat)  | NodeJS  | Aucune  | 
| [chatroom](https://github.com/systenics/ChatRoom)  | Express  | Aucune  | 

De manière générale, on retrouve plusieurs dizaines de messageries basés sur ces frameworks. Je ne suis pas parvenu à trouver des projets qui fond référence à l'aspect sécurité de la messagerie. La grande majorité des projets disponibles sur internet sont des embryons de messagerie, des preuves de concept. Il y a donc quelque chose de nouveau à implémenter.  
## Rappel des objectifs

Il s'agissait de créer un système léger et autonome capable de :
- Procurer un service de messagerie instantanée (type Treebal) mais à l'échelle d'un foyer
- Servir au maximum 25 utilisateurs sur ce service uniquement
- Stocker localement les informations, c'est à dire pas dans un cloud, mais sur le système
- Garantir la confidentialité des données en les chiffrant sur les supports (disques, mémoires)
- Garantir une intimité numérique sur les réseaux de tous les services en les chiffrant de bout en bout
- Se connecter sur un point d'accès internet de type fibre à la maison
- De proposer une interface simple de configuration (éventuellement textuelle)

La plateforme de developpement peut être un PC sur Windows ou Linux. Il faudra vérifier que le projet fonctionne sur une carte Raspberry.

## Quelques projets déjà existants

Dans un premier temps, il s'agissait d'aller voir ce qu'il se faisait déjà sur internet. On retrouve plusieurs projets qui proposent des messageries instantannées assez évoluées basées sur des infrastructures différentes.

| Nom du projet | Infrastructure | Sécurité | 
|---------------|----------------|----------|
| [django-chat-channels](https://github.com/narrowfail/django-channels-chat)  | Django | Aucune | 
| [django-private-chat](https://github.com/Bearle/django_private_chat2) | Django  | Aucune  | 
| [flask-chatroom](https://github.com/ppd0705/flask_chatroom)  | Flask  | Aucune  | 
| [node-chat](https://github.com/igorantun/node-chat)  | NodeJS  | Aucune  | 
| [chatroom](https://github.com/systenics/ChatRoom)  | Express  | Aucune  | 

Je ne suis pas parvenu à trouver des projets qui fond référence à l'aspect sécurité de la messagerie. La grande majorité des projets disponibles sur internet sont des embryons de messagerie, des preuves de concept.
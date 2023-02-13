## Les solutions techniques - Le framework

Un framework web est un ensemble de bibliothèques, de composants et de guidelines qui aident les développeurs à créer des applications web de manière plus efficace et plus rapide. Il fournit une structure de base pour le développement d'applications web en gérant certaines tâches communes telles que la gestion de la sécurité, l'authentification, les requêtes HTTP, la gestion de la base de données ...  
Un framework web peut également inclure des modèles pour les interfaces utilisateur et la mise en page, ce qui permet aux développeurs de se concentrer sur les fonctionnalités spécifiques de leur application sans avoir à constamment réinventer la roue pour les tâches courantes.  
L'utilisation d'un framework web peut améliorer la qualité du code, accélérer le développement et faciliter la maintenance et l'évolution de l'application au fil du temps.  

Comme cités dans la partie précédente, on en retrouve plusieurs tels que :
- [Ruby on Rails (RoR)](https://rubyonrails.org/)
- [Django](https://www.djangoproject.com/)
- [Express](https://expressjs.com/fr/)
- [Node.js](https://nodejs.org/en/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- ...  

Parmi ces derniers, j'ai eu plusieurs expériences avec Flask, Node.js et une avec Django. Ils ont tous leurs avantages et inconvénients. Mon choix va se porter sur Django car j'avais été très satisfait lors de ma première expérience sur un projet minimaliste en entreprise. Ce projet me permet d'aller plus loin dans le fonctionnement de ce framework.  

Django est framework web haut niveau en python (version minimum : 2.7) dont le développement a débuté en 2003. Ce framework est libre d'utilisation. Il permet de créer des serveurs web léger. Autour de Django s’est construit une communauté très active, avec au moins deux conférences par an (DjangoCon). La documentation est très bien détaillée. Une nouvelle version du framework sort tous les 8 mois environ.

<img src="images/maj.png" width="500">

Quels sont ses avantages et inconvénients pour un tel projet ?

| Avantages | Commentaires | 
|-----------|--------------|
| Beaucoup de fonctionnalités built-in | Gestion des utilisateurs, interface d'administration ... |
| Protection contre les attaques par injection SQL et les attaques XSS | Interessant pour l'utilisation du Local Storage des navigateurs internet |
| Intégration facile avec d'autres technologies | Gestion des websockets pas exemple |
| Structure claire et organisée | Facile à débugger |

| Inconvénients | Commentaires | 
|-----------|--------------|
| Surdimensionné pour les petits projets | Django est utilisé par Facebook, Instagram ... |
| Lent si on ne respecte pas la structure de programmation | Il faut veiller à bien comprendre la méthodologie expliqué dans la documentation |
| Pas simple d'utilisation au départ | Nécéssite de lire la documentation |

Il s’articule complétement autour du pattern logiciel MVT (Model, Vue, Template). Cela permet de séparer le traitement des informations de l’affichage. La structure de code à l’avantage d’être claire, les applications utilisées par le serveur sont isolées dans leurs répertoires correspondants. Ci-dessous le répertoire du serveur [sendapp](https://github.com/MalloryLP/sendapp/tree/main/sendapp), dans lequel on retrouve les codes relatifs à la gestion des [comptes](https://github.com/MalloryLP/sendapp/tree/main/sendapp/accounts), aux [chats](https://github.com/MalloryLP/sendapp/tree/main/sendapp/chat), les [paramètres sur serveur](https://github.com/MalloryLP/sendapp/tree/main/sendapp/sendapp) et les répertoires liés au front-end, [static](https://github.com/MalloryLP/sendapp/tree/main/sendapp/static) et [template](https://github.com/MalloryLP/sendapp/tree/main/sendapp/templates).

<img src="images/root.jpg" width="550">  

# Les solutions techniques - Le framework

## Recherche du framework adéquat

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

Django est framework web haut niveau en python dont le développement a débuté en 2003. Ce framework est libre d'utilisation. Il permet de créer des serveurs web léger. Autour de Django s’est construit une communauté très active, avec au moins deux conférences par an (DjangoCon). La documentation est très bien détaillée. Une nouvelle version du framework sort tous les 8 mois environ.

<img src="images/maj.png" width="500">

Après plusieurs recherches sur internet et l'avis d'une connaissance, j'ai pu dresser des tableaux de ses avantages et inconvénients :

| Avantages | Commentaires | 
|-----------|--------------|
| Beaucoup de fonctionnalités built-in | Gestion des utilisateurs, de la base de données, l'interface d'administration |
| Protection contre les attaques par injection SQL et les attaques XSS | Interessant pour l'utilisation du Local Storage des navigateurs internet |
| Intégration facile avec d'autres technologies | Gestion des websockets pas exemple |
| Structure claire et organisée | S’articule complétement autour du pattern logiciel MVT (Model, Vue, Template). Cela permet de séparer le traitement des informations de l’affichage.  |

| Inconvénients | Commentaires | 
|-----------|--------------|
| Surdimensionné pour les petits projets | Django est utilisé par Facebook, Instagram ... |
| Lent si on ne respecte pas la structure de programmation | Il faut veiller à bien comprendre la méthodologie expliqué dans la documentation |
| Pas simple d'utilisation au départ | Nécéssite de lire la documentation |

## Mise en place du projet

La structure de code à l’avantage d’être claire, les applications utilisées par le serveur sont isolées dans leurs répertoires correspondants. Ci-dessous le répertoire du serveur [sendapp](https://github.com/MalloryLP/sendapp/tree/main/sendapp), dans lequel on retrouve les codes relatifs à la gestion des [comptes](https://github.com/MalloryLP/sendapp/tree/main/sendapp/accounts), aux [chats](https://github.com/MalloryLP/sendapp/tree/main/sendapp/chat), les [paramètres sur serveur](https://github.com/MalloryLP/sendapp/tree/main/sendapp/sendapp) et les répertoires liés au front-end, [static](https://github.com/MalloryLP/sendapp/tree/main/sendapp/static) et [template](https://github.com/MalloryLP/sendapp/tree/main/sendapp/templates). Le serveur est livré avec une base de données relationnelles sqlite3.

<img src="images/root.jpg" width="600">  

J'ai voulu quelque chose de simple pour l'application avec une page d'accueil, de connexion, de création de compte et le chat. Le diagramme fonctionnel ce-dessous représente la structure du site :

<img src="images/structure.jpg" width="600">

L'utilisateur demande à accéder à la page principale. Il n'est pas connecté. S'offre à lui deux choix : se connecter ou s'enregistrer. Une fois qu'il aura complété le formulaire, il sera connecté et redirigé vers la page /home. Celle-ci propose plusieurs options comme : se déconnecter, aller dans les paramètres du compte utilisateur et accéder à la messagerie.  
En parallèle, l'administrateur du site peut demander la page /admin pour administer le site et sa base de données. Cette interface est implémenté directement à la création du serveur et peut être modifiée. 

```python
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('gen/', views.KeyGen.as_view(), name='gen'),
    path('api/', views.EncryptionKey.as_view(), name='api'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

```python
urlpatterns = [
    path('chat/', views.Home.as_view(), name='chat'),
    path('chat/<str:username>/', views.Chat.as_view(), name='friendchat')
]
```

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', Home.as_view(), name='home'),
    path('params/', Params.as_view(), name='params'),
    path('', include('accounts.urls')),
    path('', include('chat.urls')),
]
```
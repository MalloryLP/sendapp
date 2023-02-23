# Solutions techniques - Quelques informations supplémentaires

## Génération du certificat SSL

Un certificat SSL (Secure Sockets Layer) est un certificat numérique qui est utilisé pour sécuriser les connexions entre un serveur et un client. Il permet de chiffrer les données échangées entre les deux parties (même si nos messages transmis sont chiffrés), empêchant ainsi toute interception ou modification non autorisée. Sans ce certificat, il est impossible de mettre une place le protocole HTTPS. Il faut donc pouvoir en générer un.

Les certificats SSL sont délivrés par des autorités de certification (CA - Certificate Authorities), qui sont des organisations qui vérifient l'identité et l'authenticité des propriétaires de sites web.

Il existe de nombreuses autorités de certification reconnues à l'échelle mondiale, telles que Comodo, Symantec, DigiCert, GlobalSign, Let's Encrypt... Les navigateurs web tels que Chrome, Firefox, Safari, Edge... ont des listes pré-installées de CA de confiance. Lorsqu'un propriétaire de site web souhaite obtenir un certificat SSL pour son site, il doit généralement fournir des informations d'identification à l'autorité de certification, telles que son nom de domaine, son adresse postale, son adresse e-mail et des informations d'entreprise. L'autorité de certification vérifie ensuite ces informations avant d'émettre le certificat SSL.

Dans notre cas, le site ne sera pas déployé et donc restera en réseau local. Un vrai "faux" certificat SSL pourra satisfaire le besoin. Il faut trouver un service qui va nous donner un vrai certificat SSL mais qui ne sera pas validé par les autorités compétentes.

J'ai utilisé le site [Rakko Tools](https://fr.rakko.tools/tools/46/) pour cela :

<p align="center" width="100%">
    <img src="images/ssl.png" width="70%">  
</p>

En 5 lignes et un clic, j'ai pu obtenir un certificat au format PEM. La clé privée est enregistrée dans le fichier `code.pem` et le certificat dans `certif.pem`. Au lancement du serveur Django, il faut simplement spécifier le chemin vers ces fichiers : 

```shell
python ./manage.py runsslserver --certificate ./sendapp/certif.pem --key ./sendapp/code.pem 0.0.0.0:8000
```

Le certificat n'étant pas reconnu par le navigateur, à chaque connexions au site, on va avoir un message d'avertissement disant qu'il n'est pas sécurisé sur le navigateur. Pas d'inquiétude, poursuivez.

On peut maintenant utiliser la librairie `crypto.subtle`.

## Transmission des images

## Sauvegarde des messages dans la base de données
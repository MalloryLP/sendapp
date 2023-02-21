# Les solutions techniques - Le chiffrement

La sécurité des données est un enjeu crucial pour toute application qui traite des informations sensibles, notamment les messageries instantanées. Pour garantir la confidentialité des échanges, il est souvent recommandé de mettre en place un chiffrement de bout en bout.

## Quel chiffrement appliquer ?

Un algorithme de chiffrement est une méthode mathématique utilisée pour transformer un texte clair en un texte chiffré, afin de garantir la confidentialité et la sécurité des données lorsqu'elles sont transmises ou stockées.

Il existe deux types d'algorithmes de chiffrement : 
- symétrique
- asymétrique

Les algorithmes de chiffrement symétrique, tels que l'Advanced Encryption Standard (AES), utilisent une même clé pour chiffrer et déchiffrer les données. Les algorithmes de chiffrement asymétrique, tels que le Rivest-Shamir-Adleman (RSA), utilisent deux clés distinctes : 
- une clé publique pour chiffrer les données
- une clé privée pour les déchiffrer

L'AES est un algorithme de chiffrement symétrique qui est généralement utilisé pour chiffrer les données. L'avantage principal de l'AES est sa vitesse de traitement élevée, qui permet de chiffrer rapidement de grandes quantités de données. En outre, l'AES est considéré comme sûr et fiable, car il a été largement étudié et testé par la communauté de la sécurité informatique.

L'avantage principal du RSA est sa sécurité, car il est basé sur la difficulté de factoriser de grands nombres premiers (clés robustes). Le RSA est également largement utilisé dans les systèmes de signature numérique, où il est utilisé pour garantir l'authenticité et l'intégrité des données.

En rédigant ce rapport, j'ai appris que dans plusieurs cas d'applications, on peut utiliser un chiffrement hybride, qui combine les avantages de l'AES et du RSA. Dans un chiffrement hybride, les données sont d'abord chiffrées avec une clé AES unique pour chaque message, puis la clé AES est elle-même chiffrée avec la clé publique RSA du destinataire avant d'être envoyée. Le destinataire peut ensuite utiliser sa clé privée pour déchiffrer la clé AES, puis utiliser cette clé pour déchiffrer le message.

Avec toutes ces informations, j'ai décidé d'implémenter un algorithme de type RSA à deux clés pour cette messagerie. Dans une premier temps, je voulais montrer qu'il était possible d'implémenter un tel algorithme pour cette messagerie et mettre l'aspect sécurité de coté (en début de projet) en suivant ce schéma :

<p align="center" width="100%">
    <img src="images/key_gen.png" width="70%">  
</p>

Cette implémentation n'est pas du tout sécurisé et présente plusieurs failles comme le fait que la clé privée doit être connue que par son propriétaire (même le serveur soit l'ignorer). Le fait de la transmettre du serveur au propriétaire via une requête HTTP fait que le chiffrement est vulnérable. J'explique quelles solutions pourraient être mises en oeuvre pour contrer ces problèmes dans la partie [04_les_ameliorations](https://github.com/MalloryLP/sendapp/tree/main/doc/04_les_ameliorations.md).

## Mise en place du chiffrement

### Génération des clés de chiffrement

En partant du principe que le serveur ne doit pas connaitre la clé privée, je décide que la génération des clées se fait chez le client. Le code générateur est transmit au client lors de la requête GET vers `/gen`.

L'ensemble du code générateur de clées est contenu dans le Javascript de la page html `key_gen.html`. Ce code se base sur `crypto.subtle` de l'API Javascript qui permet de réaliser des opérations de chiffrement au sein d'un navigateur web.  
Elle est disponible dans les navigateurs modernes, tels que Google Chrome, Mozilla Firefox, Safari, Microsoft Edge, etc. Cette API fournit des fonctions pour la génération de clés, le chiffrement et le déchiffrement de données, la création de signatures numériques, et d'autres opérations.  
Parmi les algorithmes de chiffrement disponibles dans la librairie crypto.subtle, on peut citer le chiffrement symétrique (AES, DES, etc.), le chiffrement asymétrique (RSA, ECDSA, etc.), et les fonctions de hachage (SHA-1, SHA-256, etc.).

Au chargement de la page, est directement appelé la fonction `generateKey`. Cette fonction va générer une paire de clées (clé publique et privée).

```javascript
function generateKey(alg, scope) {
    return new Promise(function(resolve) {
        var genkey = crypto.subtle.generateKey(alg, true, scope)
        genkey.then(function (pair) {
            resolve(pair)
        })
    })
}

[...]

var encryptAlgorithm = {
    name: "RSA-OAEP",
    modulusLength: 2048,
    publicExponent: new Uint8Array([1, 0, 1]),
    extractable: false,
    hash: {
        name: "SHA-256"
    }
}

var scopeEncrypt = ["encrypt", "decrypt"]

var keys = await generateKey(encryptAlgorithm, scopeEncrypt).then(function(keys){
    return keys
})
```

Le type de clés générées est défini dans `encryptAlgorithm` :

- `name`, le nom de l'agorithme de chiffrement.
- `modulusLength`, la longueur en bits du modulus, qui est de 2048 bits dans ce cas. Le modulus est le produit des deux nombres premiers p et q utilisés dans le chiffrement RSA. Une longueur de 2048 bits est généralement considérée comme sûre pour les applications de sécurité à long terme.
- `publicExponent`, est l'exposant public utilisé dans le chiffrement RSA. Dans ce cas, il est défini comme un tableau d'octets Uint8Array([1, 0, 1]). C'est un paramètre qui est utilisé pour chiffré les données couramment.
- `extractable`, est un booléen qui indique si la clé générée peut être extraite de la mémoire ou non. Dans ce cas, elle est définie comme false.
- `hash`, défini les paramètres du hachage à utiliser avec l'algorithme de chiffrement RSA-OAEP. Dans ce cas, le hachage est SHA-256, qui est une fonction de hachage cryptographique sécurisée.

Dès que les clés sont générées, elles sont directement testés sur une chaine de caractère. Si l'algorithme de chiffrement/déchiffrement permet de retrouver la chaine de caractère originelle, les clées sont transmissent au serveur. Sinon, `no_key` est transmit au serveur, cela pourra être traité par la suite.

```javascript
var message = "Quelle est la reponse de la vie ? 42."
var vector = crypto.getRandomValues(new Uint8Array(16))

var encryptedData = await encryptData(vector, keys.publicKey, message).then(function(encryptedData){
    console.log(arrayBufferToBase64(encryptedData))
    return encryptedData
})

var result = await decryptData(vector, keys.privateKey, encryptedData).then(function(result){
    console.log(arrayBufferToText(result))
    return result
})

[...]

if(arrayBufferToText(result) == "Quelle est la reponse de la vie ? 42."){
    window.onload = sendInfos(exportedPublicKey, exportedPrivateKey);
}else{
    window.onload = sendInfos("no_key", "no_key");
}
```

<<<<<<< HEAD
On peut remarquer que ce ne sont pas les clés qui sont transmissent directement mais leur équivalent exporté. C'est à dire qu'on transmet au serveur une version des clées en chaine de caractère. Les clées transmissent sont de la forme ci-dessous.
=======
La variable `vector` représente un vecteur d'initialisation généré de manière aléatoire et utilisé dans le chiffrement/déchiffrement du message. Ce vecteur est une valeur aléatoire de taille fixe qui est utilisée pour garantir l'unicité des données cryptées.

On peut remarquer que ce ne sont pas les clés qui sont transmissent directement mais leur équivalent exporté standardisé ([format PEM](https://www.cryptosys.net/pki/rsakeyformats.html)). C'est à dire qu'on transmet au serveur une version des clées en chaine de caractère.
>>>>>>> 6498f1b94db119a6585d22c6920d373031fea580

```text
-----BEGIN RSA PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArskTtxcaCUeTpddgR62w
E3ePjQziGWcTNtvXvCTiP65012DcXdZycBGBNt0fsC0PPzU5B1fZIgixeMjOdrEl
XehLRE3NU7Rx9Km4qKC732f7xc7vR4WzxUMFN/DS6uM7vc3BvRHZ+Ci34MScCPGK
9UXlC9wbirfB9fXiQPtuyMPBwjtLRcupDD7WCMfdRuwVh0CiK147bGUcoKiviEnB
euVl3/QPSiOb7OA2CzaPQsVZBob5YvvdjpaxPIvMNDEfNX18wBeAjZdoSLaz9Pze
DnoVinvMjcrRaF17VyFyM+/flp8ChkjEhrFVgfgvfo/JjCXozf2WEZbM15AA5y5G
jwIDAQAB
-----END RSA PUBLIC KEY-----
```


```text
-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCuyRO3FxoJR5Ol
12BHrbATd4+NDOIZZxM229e8JOI/rnTXYNxd1nJwEYE23R+wLQ8/NTkHV9kiCLF4
yM52sSVd6EtETc1TtHH0qbiooLvfZ/vFzu9HhbPFQwU38NLq4zu9zcG9Edn4KLfg

[...]

3KE3YA7xrXwubRtsoVZWsAImzCAvozNw3rtkbwSvAoGAPkD/jLRWu5xfjtAkTBDb
uQO3F1TxVl03fKqrtS5G3nOw2jubUCXYlpt2/I93FlfcjtocMhN/b3QclGPWnQxS
jrag/Eao9NFQglzH8fIAZ+MrivNY5lKf/KHaZ+UYdDTHAvkVM5h/rwvyLFzjx30O
9BjWIwUSF6aAKNg9qO/ncVc=
-----END RSA PRIVATE KEY-----
```

Il n'existe pas de fonction capable de réaliser une telle transformation. Cela doit se faire manuellement avec une boucle dans le fonction `convertBinaryToPem`.

```javascript
function convertBinaryToPem(binaryData, label) {
    var base64Cert = arrayBufferToBase64String(binaryData)
    var pemCert = "-----BEGIN " + label + "-----\r\n"
    var nextIndex = 0
    var lineLength
    while (nextIndex < base64Cert.length) {
        if (nextIndex + 64 <= base64Cert.length) {
        pemCert += base64Cert.substr(nextIndex, 64) + "\r\n"
        } else {
        pemCert += base64Cert.substr(nextIndex) + "\r\n"
        }
        nextIndex += 64
    }
    pemCert += "-----END " + label + "-----\r\n"
    return pemCert
}

function exportPublicKey(keys) {
    return new Promise(function(resolve) {
        window.crypto.subtle.exportKey('spki', keys.publicKey).
        then(function(spki) {
        resolve(convertBinaryToPem(spki, "RSA PUBLIC KEY"))
        })
    })
}

function exportPrivateKey(keys) {
    return new Promise(function(resolve) {
        var expK = window.crypto.subtle.exportKey('pkcs8', keys.privateKey)
        expK.then(function(pkcs8) {
        resolve(convertBinaryToPem(pkcs8, "RSA PRIVATE KEY"))
        })
    })
}
```

Il ne reste plus qu'à transmettre les clées de chiffrement au serveur avec la fonction `sendInfos`. Cette fonction reste assez simple, elle crée une instance `XMLHttpRequest` et l'envoie au serveur. Cette requête est dirigé vers l'url `/api` en charge des clées de chiffrement d'après la définition dans `urls.py` : `path('api/', views.EncryptionKey.as_view(), name='api')`. Sécurité oblige, doit être transmit dans le header au serveur le `crsftoken` sinon la requête n'est pas traitée. Dans le corps de la requête, on transmet le nom du propriétaire des clées et leurs valeurs.

```javascript
function sendInfos(f_exportedPublicKey, f_exportedPrivateKey){
    var crsftoken = '{{ csrf_token }}'
    const requestObj = new XMLHttpRequest()
    requestObj.open('POST', "{% url 'api' %}")
    requestObj.setRequestHeader("X-CSRFToken", crsftoken)
    requestObj.send(JSON.stringify({
        "user": '{{ user.username }}',
        "publicKey": f_exportedPublicKey,
        "privateKey": f_exportedPrivateKey
    }))
}
```

Quand on regarde de plus près le vue associé à l'url `/api`, on peut voir qu'à chaque requête POST, le corps est analysé pour recupérer les clés de chiffrement et le nom du propriétaire des clées. Si ce nom est déjà associé à une clé de chiffrement, on met à jour la clé (impossible pour le moment mais implémenté en backend), sinon on la sauvegarde dans la base de données.

```python
class EncryptionKey(View):

    def get(self, request):

    [...]

    def post(self, request):

        body = json.loads(request.body.decode('utf-8'))
        owner = body["user"]
        pub = body["publicKey"]
        pri = body["privateKey"]

        if PublicKey.objects.filter(owner=owner).exists():
            print("Public key updated !")
            obj, created = PublicKey.objects.update_or_create(owner = owner, defaults={"pub": pub})
        else:
            print("Public key created !")
            publicKey = PublicKey()
            
            publicKey.owner = owner
            publicKey.pub = pub
            publicKey.save()

        if PrivateKey.objects.filter(owner=owner).exists():
            print("Private key updated !")
            obj, created = PrivateKey.objects.update_or_create(owner = owner, defaults={"pri": pri})
        else:
            print("Private key created !")
            privatekey = PrivateKey()
            
            privatekey.owner = owner
            privatekey.pri = pri
            privatekey.save()

        return render(request, 'chat/friendsnav.html')
```

Comme pour la classe `ChatModel` qui sert à enregistrer chaque message dans la base de données, sont crées deux classes `PublicKey` et `PrivateKey` pour les sauvegarder et charger correctement. Dans le code précédent, `.save()` sauvegarde la clé dans la base de données.

```python
class PublicKey(models.Model):
    owner = models.TextField()
    pub = models.TextField()

class PrivateKey(models.Model):
    owner = models.TextField()
    pri = models.TextField()
```
### Chiffrement des messages
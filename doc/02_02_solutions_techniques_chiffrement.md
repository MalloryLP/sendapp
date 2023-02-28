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

En rédigeant ce rapport, j'ai appris que dans plusieurs cas d'applications, on peut utiliser un chiffrement hybride, qui combine les avantages de l'AES et du RSA. Dans un chiffrement hybride, les données sont d'abord chiffrées avec une clé AES unique pour chaque message, puis la clé AES est elle-même chiffrée avec la clé publique RSA du destinataire avant d'être envoyée. Le destinataire peut ensuite utiliser sa clé privée pour déchiffrer la clé AES, puis utiliser cette clé pour déchiffrer le message.

Avec toutes ces informations, j'ai décidé d'implémenter un algorithme de type RSA à deux clés pour cette messagerie. Dans un premier temps, je voulais montrer qu'il était possible d'implémenter un tel algorithme pour cette messagerie et de mettre l'aspect sécurité de côté (en début de projet) en suivant ce schéma :

<p align="center" width="100%">
    <img src="images/key_gen.png" width="70%">  
</p>

Cette implémentation n'est pas du tout sécurisé et présente plusieurs failles comme le fait que la clé privée doit être connue que par son propriétaire (même le serveur soit l'ignorer). Le fait de la transmettre du serveur au propriétaire via une requête HTTP fait que le chiffrement est vulnérable. J'explique quelles solutions pourraient être mises en oeuvre pour contrer ces problèmes dans la partie [04_les_ameliorations](https://github.com/MalloryLP/sendapp/doc/04_les_ameliorations.md).

## Mise en place du chiffrement

### Génération des clés de chiffrement

En partant du principe que le serveur ne doit pas connaître la clé privée, je décide que la génération des clés se fait chez le client. Le code générateur est transmit au client lors de la requête GET vers `/gen`.

L'ensemble du code générateur de clés est contenu dans le Javascript de la page html `key_gen.html`. Ce code se base sur `crypto.subtle` de l'API Javascript qui permet de réaliser des opérations de chiffrement au sein d'un navigateur web.  
Elle est disponible dans les navigateurs modernes, tels que Google Chrome, Mozilla Firefox, Safari, Microsoft Edge, etc. Cette API fournit des fonctions pour la génération de clés, le chiffrement et le déchiffrement de données, la création de signatures numériques, et d'autres opérations.  
Parmi les algorithmes de chiffrement disponibles dans la librairie crypto.subtle, on peut citer le chiffrement symétrique (AES, DES, etc.), le chiffrement asymétrique (RSA, ECDSA, etc.), et les fonctions de hachage (SHA-1, SHA-256, etc.).

Au chargement de la page, est directement appelée la fonction `generateKey`. Cette fonction va générer une paire de clés (clé publique et privée).

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

- `name`, le nom de l'algorithme de chiffrement.
- `modulusLength`, la longueur en bits du modulus, qui est de 2048 bits dans ce cas. Le modulus est le produit des deux nombres premiers p et q utilisés dans le chiffrement RSA. Une longueur de 2048 bits est généralement considérée comme sûre pour les applications de sécurité à long terme.
- `publicExponent`, est l'exposant public utilisé dans le chiffrement RSA. Dans ce cas, il est défini comme un tableau d'octets Uint8Array([1, 0, 1]). C'est un paramètre qui est utilisé pour chiffrer les données couramment.
- `extractable`, est un booléen qui indique si la clé générée peut être extraite de la mémoire ou non. Dans ce cas, elle est définie comme false.
- `hash`, défini les paramètres du hachage à utiliser avec l'algorithme de chiffrement RSA-OAEP. Dans ce cas, le hachage est SHA-256, qui est une fonction de hachage cryptographique sécurisée.

Dès que les clés sont générées, elles sont directement testées sur une chaîne de caractère. Si l'algorithme de chiffrement/déchiffrement permet de retrouver la chaine de caractère originelle, les clés sont transmissent au serveur. Sinon, `no_key` est transmit au serveur, cela pourra être traité par la suite.

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

La variable `vector` représente un vecteur d'initialisation généré de manière aléatoire et utilisé dans le chiffrement/déchiffrement du message. Ce vecteur est une valeur aléatoire de taille fixe qui est utilisée pour garantir l'unicité des données chiffrées.

On peut remarquer que ce ne sont pas les clés qui sont transmissent directement, mais leur équivalent exporté standardisé ([format PEM](https://www.cryptosys.net/pki/rsakeyformats.html)). C'est-à-dire qu'on transmet au serveur une version des clés en chaîne de caractère.

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

Il ne reste plus qu'à transmettre les clés de chiffrement au serveur avec la fonction `sendInfos`. Cette fonction reste assez simple, elle crée une instance `XMLHttpRequest` et l'envoie au serveur. Cette requête est dirigée vers l'url `/api` en charge des clés de chiffrement d'après la définition dans `urls.py` : `path('api/', views.EncryptionKey.as_view(), name='api')`. Sécurité oblige, doit être transmis dans le header au serveur le `crsftoken` sinon la requête n'est pas traitée. Dans le corps de la requête, on transmet le nom du propriétaire des clés et leurs valeurs.

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

Quand on regarde de plus près la vue associée à l'url `/api`, on peut voir qu'à chaque requête POST, le corps de la requête est analysé pour récupérer les clés de chiffrement et le nom du propriétaire des clés. Si ce nom est déjà associé à une clé de chiffrement, on met à jour la clé (impossible pour le moment, mais implémenté en backend), sinon on la sauvegarde dans la base de données.

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

Comme pour la classe `ChatModel` qui sert à enregistrer chaque message dans la base de données, sont crées deux classes `PublicKey` et `PrivateKey` (utilisées dans le code précédent) pour les sauvegarder et charger correctement. Dans le code précédent, `.save()` sauvegarde la clé dans la base de données.

```python
class PublicKey(models.Model):
    owner = models.TextField()
    pub = models.TextField()

class PrivateKey(models.Model):
    owner = models.TextField()
    pri = models.TextField()
```
### Chiffrement des messages

Il s'agit maintenant de chiffrer les messages. Il faut récupérer les clés de chiffrement qui sont stockées sur le serveur d'après le schéma.

Tout d'abord, il faut mettre en place le html de la page `/chat` contenu dans `chat.html`.

```html
<div class="chatcontainer">
    <div id="chat-body" style="width: 100%;">
    </div>
</div>

<div class="usercontainer">
    <input class="message_input" type="text" id="message_input" placeholder="Ecrire un message...">
    <input class="file_input" type="file" id="chat-image-submit" name="image" accept="image/png, image/jpeg">
    <button class="submit-btn" id="chat-message-submit">Envoyer</button>
</div>
```
Les messages seront affichés dans la division `chat-body`. Pour les interactions avec l'utilisateur, on retrouve un champ d'entrées `message_input`, un bouton pour uploader des images `file_input` et un bouton `submit-btn` pour envoyer le message.

Il faut maintenant faire une requête GET vers l'API du serveur pour récupérer les clés une fois que la page est chargée.

```javascript
<script>

fetch("{% url 'api' %}", options).then(response => response.json()).then(json => {

    console.log(json);

    [...]

};

</script>
```
Seront contenues dans `json`, au format JSON les clés. 

```json
{
    "user": {
        "name": "alice.azerty",
        "UserPublicKey": "-----BEGIN RSA PUBLIC KEY-----\r\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqkoSI4NJAopDvYHKxzT+\r\n/JtYXeLuAh1D9mHWcE2ERPxdr0lWUgTeQQzDdA+g8IOgkhEtI4FWjBLi5b+ojnwM\r\nW0Iedqsy7zNsvr1oW4M8SU13vkDRcgcH4rKQ4pj168nSlEd5uvBsfHxNGoMJuyRc\r\nwIA0Nawa/tr3wdgsEs1JZKRNSnDnFnkhC9IfPqoPDlTAMy71lFp//dt1zwsQ81xw\r\natq6B0dK47NvcZ2Dkj2vTLFiJ4GW6m7Aeryy/qVcQsH9nPUMTpSOVbjjT67/rFOD\r\nM5ryWJ1RAS9OojB5OSd5Xjw2/bKDtoOWQWYAAzOAdERvZ0bjKdQjpIsBR4S8p4hY\r\n8QIDAQAB\r\n-----END RSA PUBLIC KEY-----\r\n",
        "UserPrivateKey": "-----BEGIN RSA PRIVATE KEY-----\r\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqShIjg0kCikO9\r\ngcrHNP78m1hd4u4CHUP2YdZwTYRE/F2vSVZSBN5BDMN0D6Dwg6CSES0jgVaMEuLl\r\nv6iOfAxbQh52qzLvM2y+vWhbgzxJTXe+QNFyBwfispDimPXrydKUR3m68Gx8fE0a\r\ngwm7JFzAgDQ1rBr+2vfB2CwSzUlkpE1KcOcWeSEL0h8+qg8OVMAzLvWUWn/923XP\r\nCxDzXHBq2roHR0rjs29xnYOSPa9MsWIngZbqbsB6vLL+pVxCwf2c9QxOlI5VuONP\r\nrv+sU4MzmvJYnVEBL06iMHk5J3lePDb9soO2g5ZBZgADM4B0RG9nRuMp1COkiwFH\r\nhLyniFjxAgMBAAECggEAD1o7NWluKST3A3xSoFAWVwbYWiqN47HowStD7n8GmEOa\r\nXKXDewSGVx4D9xA7pcNwNAsJY0STXXCMdUMouqPTZ1zYK0G3B1q/CJlB8dIsmr05\r\nuPTWDS42F0mbB1rb/QSGkCi7gE+RsE1ylBvRQkZ+eDp2uooIKwbpxFetbYqFfeWu\r\nfCrsnNcb3hrQlyNFvyrCOLKMS4qA5juygHH6dHXcFGDlgnvs1HeMVjrQfNJlBZzn\r\n5lnC9puk9cULHzl1oBcwif0hurOXj5aJwyz5vwHyq/MFbGoec2yLKdNA3rdd5Ol2\r\nGIEU0gJTbNrVcSEmBIUaGJTg0lZ4mhsAWQHA2xH8+QKBgQDeAjXE9hLzZbZwkFTd\r\nh30ySA3cnFi2A6GOMtNUI5hVrLnMJRdRANRJZ3DpEybCPmT+JEXJH+1Ov/sWACOF\r\nR08+vqTaPaiRBbUM3wyR/PT029gOk7plNMEwK3HYSiBA/JQuf472P68MjY1C1mZX\r\nd4oapLJ1AG2j2rGxPPIT26cYFQKBgQDEXK96F2YrV99iQOTJFrBTg9jDQ2fIxpNj\r\nJvP0xYbyMxeNvsUjh03x/dHCF3+yzURf4qqDcmUKSf8fB5/DjDaO5bF0xp+BWFRe\r\nPZAVKvlbanhqWMheAfuqddwrY0PwVmtPOemF69np0QnARkYlQPadvLXGY31g76A7\r\nF5ahOMS4bQKBgQCZqknxZKnFUxeuXhh/pXJgxULi+kzk3yqJtGBWErU0R/Pqe5nh\r\n9YL6s+CRUzI2rN1Wk2DCT5kAMx3mIn5zl+If+fE9JgRxLNQebpzSx5X9jdXEcThJ\r\nKPS3FLseDGC62pjuflhD1dyiAbBPHPuFezZaLrlfBsbc7Vik5xxf5l+H6QKBgQCm\r\nelo/rdTuTGrUd2ZA4p6Nv8uoCN7Vxx2wQ5czX8CAWTbP8vxamd1InEQZRSj747Hj\r\nhV3BYdwuM/w7R5B5Dsg2sKCZ+8fBtqyY1aLxf2S3z3XV2/3MTewbYh9PHbK88de6\r\n7MOCyioPZS3aOPpBnWk45IRMdY8X/zEeyGnpuCJ4pQKBgEvtwbaINOrevZJWeqDe\r\nFIU7/BOf+mU9eB7eAT4nU6ibsp9WwGMy9ha4cwUMaPgOEcsuWWhNz+QH7PrBJ6RF\r\npS1fScNpXrvQp71cifHQ+X3y+phZ669UdR4caj3tz82LyTu9FRwwlG1GVHZOKnlx\r\nvTFKIVGS0on/9PGNupnwm1DG\r\n-----END RSA PRIVATE KEY-----\r\n"
    },
    "friend": {
        "name": "bob.qwerty",
        "FriendPublicKey": "-----BEGIN RSA PUBLIC KEY-----\r\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqu4yedpNZdlCLJTyaJES\r\nx8t97ndPHreueOy1dSofad64PQQmfW+DJYCj/nevbOMV1qGzOWYmGPSMkvM3sO0G\r\nI1tRMLITcn5I/z1SIUnidO8bv+x+sARkk5cwG2MNlEx5L3lH0e2ujWRdorXukx2D\r\nP9iP5WIYpxLczZLbkpIjSQNQD8B4IUawllle0PXr3UKncVYZQJrT4akJLtyYWL91\r\ns2XePsuOPy2adn6VdYKCz2nyU7e1HYQWMLUMdoRa1U2iCnskbqyfgqPRc9EnDjoE\r\nfIusbX931JPall0RhTqGWXeC2Cq1hm0eLYSwLVf65yj3KfwZTXt/Pm6apKFhqDRg\r\ngwIDAQAB\r\n-----END RSA PUBLIC KEY-----\r\n",
        "FriendPrivateKey": "-----BEGIN RSA PRIVATE KEY-----\r\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCq7jJ52k1l2UIs\r\nlPJokRLHy33ud08et6547LV1Kh9p3rg9BCZ9b4MlgKP+d69s4xXWobM5ZiYY9IyS\r\n8zew7QYjW1EwshNyfkj/PVIhSeJ07xu/7H6wBGSTlzAbYw2UTHkveUfR7a6NZF2i\r\nte6THYM/2I/lYhinEtzNktuSkiNJA1APwHghRrCWWV7Q9evdQqdxVhlAmtPhqQku\r\n3JhYv3WzZd4+y44/LZp2fpV1goLPafJTt7UdhBYwtQx2hFrVTaIKeyRurJ+Co9Fz\r\n0ScOOgR8i6xtf3fUk9qWXRGFOoZZd4LYKrWGbR4thLAtV/rnKPcp/BlNe38+bpqk\r\noWGoNGCDAgMBAAECggEAPFnw+YQiCsFsc3g9pL0AQAnx01ZN2b8p+6k8Inu2breE\r\nHosOGgDa8c1bWdghWNVPGyKpuKz/65TA44u7kJ0Hq0ktP//IDQdYt8ILcxR2wCnC\r\nhv+19Wj/p/rcMfdFzqQ3r5LnUFBW7rZOt0n8S/ZCJrNMj0WVBbyLuIvPOg+eJMNR\r\n1m35HGq8eW2rjepK8ALvKhcyrk5dZflfslF95MY6Yra2qPaPPAUQOaksZV38Wb7v\r\nGPT6ape9bADyT9GfEknxfQHa3qOs/23IBM3okuqicDwSqId+pgLD8rtLWeVTog0l\r\n+RWUEqwnL8yL5RvltaC2C4QU4ZlkVP8N5EzyhE8yCQKBgQDlLBRCLRAIERSAHxp+\r\nSmj2R6+AxJwSDoMmcwSM01n420BLIsRMVdbLHXbEUNEFag2oSk1Qhut2iPAOtVek\r\nIMAu1YcscwhKuOFngkpJKq6IRMBdoKYWKTxLon1DkwAQM8Qdvwo2gzHMAgpb1lyw\r\nWAFAlZEvnKsyG8a1ZZxHec/K+wKBgQC+8LUYGzaklIjqRYbUDjJmxFyoCKjNx8+D\r\nKTmayzioQ1UxUC2wdgGPCL1Q26Yi7bJDnDVmpS/ezVpkfFsevBvPV8P4xilIhfRn\r\ncp7A+3eOZX27n6BGsmPsETS7MoEd/vhvdNX7nFLZRS+7l5aW2gbxExo6pnBT4TTX\r\n9fFfcidKGQKBgG2ebAJLc8OoB9pRBmcqSJKlL3m0kcLBVlJp6d9CqWKz3UkTVDn/\r\nRULa0RiOX6zrUaUSBXFjV/XXApzGeSl00PiWApZsX6b+UDMmy0m8NMfRuwIN+ePX\r\nzZOQIcLU6c7WNBTWcJgqoQMoZrQPET74mYC/CjdwBSNuzdmuxNYbmh1JAoGAEnZx\r\n/Fe9S+K07no0lFKfGwLHttPHhsZYUWVuFYKrAtIn7bHECTkP44XD0Iq8oMn9H75+\r\nB2PXoiKXJ/pCUVF9Gupwn6CBo2qYfFw/74chQ1qa8sZ3l/5t3Qi44ZT7mSvrV9Oj\r\nUUYHWMzw1aHNxN5mJ29ibONlHyc6ldtJMKJ4HBkCgYEArPQVchFoyb9P9Z87FAQc\r\nGIU7A/pkLTTgiCrkPs5kbI7+vqHU7qi27w0vvYzxZ2/yLssJh4aJfGkhE7+7BAwA\r\nRr6gARB2jS550Pi6C2vGxEyqhiojg0sQ0qdmaVHd3G+Xg2wiKJNPJdn2filgKyUl\r\nkqNkr1qBWZ3kvaS0viMda3I=\r\n-----END RSA PRIVATE KEY-----\r\n"
    }
}
```

Elles sont retournées par la vue `EncryptionKey`. La méthode `get` vérifie si les utilisateurs courant de la conversation ont des clés existantes puis les retournent sous la forme d'une classe `JsonResponse`.

```python
class EncryptionKey(View):

    [...]

    def get(self, request):

        if PublicKey.objects.filter(owner=request.headers["User"]).exists():
                obj1 = PublicKey.objects.get(owner = request.headers["User"])
                if PrivateKey.objects.filter(owner=request.headers["User"]).exists():
                    obj2 = PrivateKey.objects.get(owner = request.headers["User"])
                    if PublicKey.objects.filter(owner=request.headers["Referer"].split("/")[-2]).exists():
                        obj3 = PublicKey.objects.get(owner = request.headers["Referer"].split("/")[-2])
                        if PrivateKey.objects.filter(owner=request.headers["Referer"].split("/")[-2]).exists():
                            obj4 = PrivateKey.objects.get(owner = request.headers["Referer"].split("/")[-2])

                            return JsonResponse(
                                {"user": {
                                    "name": obj1.owner,
                                    "UserPublicKey": obj1.pub,
                                    "UserPrivateKey": obj2.pri
                                }, "friend": {
                                    "name": obj3.owner,
                                    "FriendPublicKey": obj3.pub,
                                    "FriendPrivateKey": obj4.pri
                                }})
                                
        return JsonResponse({'publicKey': None, 'privateKey': None})
```
Les clés récupérées doivent être converties au format binaire originel de `crypto.subtle` à l'aide de la fonction `convertPemBinary`. Ainsi, on pourra correctement l'importer avec la fonction `crypto.subtle.importKey`. Divers paramètres y sont spécifiés comme le type de clé `name: 'RSA-OAEP'`.

```javascript
function convertPemToBinary(pem){
    var lines = pem.split('\n')
    var encoded = ''
    for(var i = 0;i < lines.length;i++){
        if (lines[i].trim().length > 0 &&
            lines[i].indexOf('-BEGIN RSA PRIVATE KEY-') < 0 &&
            lines[i].indexOf('-BEGIN RSA PUBLIC KEY-') < 0 &&
            lines[i].indexOf('-END RSA PRIVATE KEY-') < 0 &&
            lines[i].indexOf('-END RSA PUBLIC KEY-') < 0) {
        encoded += lines[i].trim()
        }
    }
    return base64StringToArrayBuffer(encoded)
}

[...]

fetch("{% url 'api' %}", options).then(response => response.json()).then(json => {
const algorithm = {
    name: 'RSA-OAEP',
    hash: 'SHA-256',
};

    crypto.subtle.importKey(
        'spki',
        convertPemToBinary(json.friend.FriendPublicKey),
        algorithm,
        false,
        ['encrypt']
    ).then(function(friendpublicKey){

        //Zone de chiffrement des messages

        [...]

    };

    crypto.subtle.importKey(
        'pkcs8',
        convertPemToBinary(json.user.UserPrivateKey),
        algorithm,
        false,
        ['decrypt']
    ).then(function(userprivateKey){

        //Zone de déchiffrement des messages

        [...]

    };
};

```

Maintenant, on peut directement utiliser la clé publique `friendpublicKey` de l'ami auquel on veut envoyer un message pour le chiffrer et déchiffrer le message reçu avec sa clé privée `friendprivateKey`. 

Le chiffrement se passe de cette manière : dès que l'utilisateur appuie sur le bouton `chat-message-submit`, on récupère le contenu du message `message_input`. On chiffre le message avec la méthode `crypto.subtle.encrypt` et on le récupère dans la variable `ciphertext`.

```javascript
crypto.subtle.importKey(
    'spki',
    convertPemToBinary(json.friend.FriendPublicKey),
    algorithm,
    false,
    ['encrypt']
).then(function(friendpublicKey){

    //Zone de chiffrement des messages

    document.querySelector('#chat-message-submit').onclick = function(e){

        const message_input = document.querySelector('#message_input');
        const message = message_input.value;

        crypto.subtle.encrypt(
            {
                name: 'RSA-OAEP',
            },
            friendpublicKey,
            textToArrayBuffer(message)
        ).then(function(ciphertext){

            console.log(ciphertext);

            //Zone d'envoie du message au destinataire

            [...]

        });
    };
};
```

Le `ciphertext` obtenu est alors un `Uint8Array` qui sera transmis.

```shell
100,219,184,42,65,209,122,184,206,45,224,31,234,214,171,236,20,97,103,90,73,63,147,121,43,42,116,99,33,205,170,250,184,67,173,188,111,39,127,102,78,209,202,115,167,131,120,133,228,93,237,159,170,232,23,157,243,40,148,69,28,191,171,247,106,110,22,99,81,7,138,85,121,164,169,92,197,195,199,137,80,35,133,75,241,184,49,133,19,16,221,21,124,108,141,206,226,246,131,251,131,80,156,82,122,154,91,218,120,45,35,246,255,62,172,239,15,144,80,209,80,153,200,13,27,35,68,200,80,38,214,186,216,60,177,140,229,249,163,214,208,42,58,121,64,223,159,95,30,175,45,26,53,56,79,57,159,68,231,76,188,195,93,177,173,159,238,2,236,237,62,120,58,163,169,190,117,69,25,34,54,45,132,86,60,155,60,27,5,137,106,36,187,14,207,131,33,116,68,98,57,75,230,232,137,224,12,47,27,16,91,28,128,42,192,185,175,183,78,171,29,30,45,0,148,199,176,201,16,196,35,63,139,96,15,72,230,246,69,198,60,198,32,203,150,195,184,88,207,141,136,224,33,66,107,38
```

On peut noter que pour un même message, la version chiffré sera toujours différente.

### Déchiffrement des messages

Il ne reste plus qu'à faire l'opération inverse chez le destinataire. Ce dernier va utiliser sa clé privée pour déchiffrer le message reçu directement dans le code contenu dans la page HTML. A chaque message reçu (au travers de `
socket.onmessage`, une partie du rapport y est dédiée pour les explications), le code vérifie si le message reçu est bien pour l'amis auquel le message a été envoyé puis la trame chiffrée est analysée pour récupérer les entiers contenus correspondant au message. `crypto.subtle.decrypt` se charge de rendre l'array d'entier `message` en texte clair déchiffré. La phase finale consiste à ajouter le message déchiffré à la division `chat-body`. Certains éléments de codes laissent penser que le projet prend en charge le chiffrement des images, plus d'informations dans [02_04_solutions_techniques_quelques_informations](https://github.com/MalloryLP/sendapp/blob/main/doc/02_02_solutions_techniques_quelques_informations_supplémentaires.md).

```Javascript
crypto.subtle.importKey(
    'pkcs8',
    convertPemToBinary(json.user.UserPrivateKey),
    algorithm,
    false,
    ['decrypt']
).then(function(userprivateKey){

    //Zone de déchiffrement des messages

    socket.onmessage = function(e){
        const data = JSON.parse(e.data);
        if(data.username != username){

            const values = data.message.split(",");
            const numbers = values.map(value => parseInt(value, 10));
            const message = Uint8Array.from(numbers);

            if(data.type == "text"){

                crypto.subtle.decrypt(
                    {
                        name: "RSA-OAEP",
                    },
                    userprivateKey,
                    message
                ).then(function(message){
                    const uncrypted_message = arrayBufferToText(message)
                    document.querySelector('#chat-body').innerHTML += `<div class="message" style="background-color: #b6b6b6;margin:10px;">${data.username} : ${uncrypted_message}<\div>`;
                })

            }else{

                //Réception des images !

                [...]
            }  
        }
    }
});
```

## Problème !

Pour utiliser les méthodes `crypto.subtle` de l'api Javascript, il faut être dans un environnement "sécurisé". Or, lorsqu'on commence à développer un serveur basé sur Django, toutes les requêtes se font en HTTP. Il faut pouvoir faire en sorte que les requêtes soient en HTTPS.

<p align="center" width="100%">
    <img src="images/cryptosubtle.png" width="70%">  
</p>

<p align="center" width="100%">
    <img src="images/cryptosubtle2.png" width="70%">  
</p>

Dans la [documentation Django](https://docs.djangoproject.com/fr/4.1/topics/security/), les étapes pour déployer le site vers le HTTPS sont assez bien décrites.

Cela impose plusieurs choses :
- Changement des paramètres initiaux du serveur dans `settings.py`
- [Création d'un certificat SSL](https://github.com/MalloryLP/sendapp/blob/main/doc/02_02_solutions_techniques_quelques_informations_supplémentaires.md) pour le serveur (non décrit dans la documentation et impératif pour bénéficier du protocole HTTPS)
- Ne plus suivre la documentation de Django pour implémenter les websockets (le plus inquiétant), ce que fournit Django ne fonctionne pas dans un contexte sécurisé
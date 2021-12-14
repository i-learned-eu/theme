Author: Eban
Date: 2021/12/14
Keywords: Décentralisation
Slug: ipfs
Summary: Aujourd'hui la tendance est de plus en plus à la décentralisation, dans ce mouvement, a été créé le protocole IPFS (Interplanetary File System, rien que ça oui). C'est un protocole qui a pour objectif de stocker des fichiers de n'importe quel type (image, vidéo, document texte, site web...) de façon décentralisée.
Title: Comment fonctionne IPFS ?

Aujourd'hui la tendance est de plus en plus à la [décentralisation](https://ilearned.eu.org/decentralisation.html), dans ce mouvement, a été créé le protocole IPFS (Interplanetary File System, rien que ça oui). C'est un protocole qui a pour objectif de stocker des fichiers de n'importe quel type (image, vidéo, document texte, site web...) de façon décentralisée.

Ce protocole fonctionne en paire à paire (P2P) afin de garantir une plus grande accessibilité des fichiers hébergés. 

# Un changement de paradigme

Aujourd'hui sur le web, quand on fait la requête HTTP `GET https://ilearned.eu/static/img/favicon.png` on va demander au serveur à l'adresse ilearned.eu le fichier contenu dans le chemin `/static/img/favicon.png`. Le serveur pourrait alors nous renvoyer le favicon que nous cherchons, ou n'importe quoi d'autre, comme une photo de chaton.

> Avec HTTP, on demande le contenu à un emplacement, pas un fichier spécifique directement.
> 

Avec IPFS c'est tout à fait différent, plutôt que d'aller demander le fichier contenu à l'emplacement `/static/img/favicon.png`, on va demander le hash du fichier que nous souhaitons consulter. 

Si je souhaite consulter le favicon d'I Learned, je vais demander le hash (appelé CID) `QmfJpxjQezydRAswGezKs9qqqM1fFAjEZRgA4VdwwCNUsw`. Je suis alors sûr de recevoir l'image que j'ai demandé, et pas une photo de chaton qui aurait un CID (hash) différent (ici, `QmYKfEPmNbuN9mYYmPENvpNpQ6yQQ3d1EfynYNA6qPGjTA`).

# Comment accéder aux fichiers ?

Savoir représenter des fichiers, c'est bien beau, mais encore faut-il pouvoir y accéder 😅. Avec IPFS, chaque nœud du réseau ont une paire de clé qui leur permet d'échanger des informations de façon chiffrée, mais aussi d'être identifié. Tous les nœuds du réseau stockent une DHT (Distributed Hash Table, table de condensats distribuée) cette table met en relation les différents nœuds du réseau et les données qu'ils partagent, mais aussi leur multiadresse. Une multiadresse, c'est une chaine de caractère qui permet de renseigner directement comment contacter un nœud, par exemple `/ip4/89.234.156.60/udp/1234` indique de contacter l'adresse IPv4 89.234.156.60 en utilisant le protocole UDP sur le port 1234.

![Le client demande d'abord à la DHT, puis va se connecter aux pairs](/static/img/ipfs/IPFS(1).png)

# IPNS

Du fait de son fonctionnement basé sur des hash au lieu de la localisation d'un fichier, IPFS souffre d'un problème majeur. Si vous souhaitez partager avec une amie un document texte, vous devriez donner à cette amie un nouveau lien à chaque fois que le fichier change, ne serait-ce que d'un caractère. Afin de répondre à cette problématique, IPNS (InterPlanetary Name System) a été créé.

Comme nous l'avons vu plus tôt, chaque nœud du réseau a une paire de clés qui lui est propre. Vous pouvez publier un fichier spécifique à l'emplacement `/ipns/cléPublique` grâce à l'outil de ligne de commande de IPFS. Il est possible de générer plusieurs clés afin d'avoir plusieurs "noms de domaines".

Vous pouvez donc maintenant simplement partager votre clé publique avec votre amie, et celle-ci pourra accéder au fichier texte que vous souhaitiez partager !

Il existe aussi la possibilité d'utiliser le système de DNS "classique" en ajoutant un record TXT à l'emplacement `_dnslink.YOURNDD` avec pour contenu `dnslink=/ipfs/CID`. Ainsi, [ipfs.eban.eu.org](http://ipfs.eban.eu.org) est accessible depuis IPFS à partir de l'adresse `/ipns/ipfs.eban.eu.org` car il contient le record suivant :

```bash
_dnslink.ipfs.eban.eu.org. 1555	IN	TXT	"dnslink=/ipfs/QmQS9TDSi8RmLzM6QFaRcCkdnqUbGpXsFDG1iuyXnx9brm"
```

J'espère que cet article sur IPFS vous aura plu, c'est un protocole que je trouve, à titre personnel, très intéressant et prometteur à beaucoup d'égards. Il est par exemple utilisé pour stocker un clone de Wikipédia de façon décentralisée afin d'assurer que tout le monde puisse y accéder n'importe quand. Ce genre d'initiative va dans le sens d'un internet plus décentralisé, et donc moins dépendant des grosses sociétés tech (les GAFAM).
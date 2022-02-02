Title: Gemini, une alternative viable à HTTP ?
Keywords: gemini, privacy, http
Date: 2021-05-06
author: Eban
summary: Hey 👋, aujourd'hui on parle du protocole Gemini, un protocole alternatif à HTTP ;)
Slug: gemini

Hey 👋, aujourd'hui on parle du protocole Gemini, Gemini est un protocole alternatif à HTTP ou Gopher pour ne citer qu'eux, créé en Juin 2019 avec pour objectif d'être beaucoup plus léger qu'HTTP, et de mieux respecter la vie privée des utilisateurs, en effet, avec Gemini, pas de JS, de cookies ou de eTag, le tracking des utilisateurs est quasi impossible. Gemini n'a pas été créé pour concurrencer HTTP mais bien pour offrir une alternative plus légère et sécurisée aux utilisateurs. Ce protocole embarque d'office le protocole TLS, il n'y a donc contrairement à HTTP pas la possibilité d'avoir des communications en clair. Ce protocole est basé en partie sur HTTP 0.9 et essentiellement textuel, mais des images peuvent aussi être intégré. 

Une requête Gemini est très simple, le client demande un fichier sur le serveur cible, le serveur répond avec un code d'erreur (ici, 20 = OK), le type de fichier, le plus souvent `text/gemini` et pour finir envoie le fichier. C'est plus simple que TCP avant-hier n'est-ce pas ? 😅 Voici donc une requête standard sur Gemini. C représente le client et S le serveur.

```
C: gemini://gemini.circumlunar.space/docs/faq.gmi
S: 20 text/gemini
S: # Hey !
S: This is a website running under Gemini :D
```

J'ai volontairement omis toute la partie correspondant à TLS dans l'exemple de requête ci-dessus car TLS fera l'objet d'un article plus complet dans peu de temps.

Afin de se rendre indépendant de CA externes qui, [comme on l'a vu](https://ilearned.eu/dane.html) sont un SPOF (single point of failure, point unique de défaillance) qui, si il se trouve compromit, pourrait délivrer des certificats frauduleux Gemini s'appuie sur le principe de TOFU, Trust on first use, c'est un méchanisme aussi utilisé par SSH par exemple, pour faire confiance à un certificat, le logiciel s'appuie simplement sur le certificat qu'il a croisé pour la première fois sur ce site. Cette façon de fonctionner est décriée par certains préférant un fonctionnement avec CA. Cependant, des mécanismes comme [DANE](https://ilearned.eu/dane.html) couplé à [DNSSEC](https://ilearned.eu/dnssec.html) existent et permettent de rendre relativement sécurisé Gemini.

À l'occasion de ce post, j'ai rendu mon blog accessible sur Gemini, je vous invite à faire un tour dessus à l'adresse `gemini://eban.bzh` vous trouverez [ici](https://gemini.circumlunar.space/clients.html) une liste de clients Gemini.

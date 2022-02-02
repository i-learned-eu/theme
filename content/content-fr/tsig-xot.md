Title: Sécuriser la connexion entre Master et Slave
Keywords: DNS, Domain Name System, NS, xfr, zone transfer, tsig, xot
Summary: Dans cet article, on parle des différents moyens de sécuriser les échanges entre Master et Slave
Date: 2021-04-27
Category: Today I Learned
Author: Eban
Slug: tsig-xot

Comme nous l'avons vu [hier](https://google.com/), la communication entre `master` et `slave` est faite en claire ce qui peut représenter une problème de sécurité, plusieurs systèmes ont donc été mit en place afin de sécuriser ce système.

# Le filtrage par IP

Le moyen le plus courant pour filtrer les demandes de transfert de zone est le filtrage par IP, mais il présente deux inconvénients principaux, ce filtrage par IP peut poser problème dans le cas où le slave aurait un IP dynamique et pose aussi un problème de sécurité dû au fait qu'une IP puisse être "[spoofé](https://en.wikipedia.org/wiki/IP_address_spoofing)" (= usurpée), ce type d'attaque fera très probablement l'objet d'un article dans un futur proche 😉.

# Le protocole TSIG

Le protocole `TSIG`, introduit en Mai 2000 par la [RFC 2845](https://tools.ietf.org/html/rfc2845) (pour info, une RFC, requests for comments, est un documents qui détaille le fonctionnement d'Internet ou de différents matériels informatique) permet d'authentifier un `slave` grâce à un secret partagé, le `slave` envoie un premier paquet contenant un [condensat](https://en.wikipedia.org/wiki/Cryptographic_hash_function) (hash) de la clé, le master compare alors ce hash avec celui qu'il génère aussi de son côté à partir de cette même clé, s'ils correspondent et que les `id` (= nom de la clé) sont identiques le slave est authentifié, pour résumer cela, voici un schéma.

![https://i.postimg.cc/0yhhnRjL/Frame-4.webp](/static/img/tsig-xot/Frame_4.webp)

![Se%CC%81curiser%20la%20connexion%20entre%20Master%20et%20Slave%206ab075baba074e2a967914523258907d/Frame_5.webp](/static/img/tsig-xot/Frame_5.webp)

Ce protocole a cependant deux tares, premièrement, la clé doit être partagée pour la première fois de façon sécurisée, ce qui n'est pas toujours chose facile, deuxième tare, l'authentification est bien sécurisée, mais c'est moins le cas pour les requêtes [AXFR/IXFR](https://google.com) qui sont seulement signée, ainsi, l'intégrité de la réponse peut être assurée mais son contenu transite en clair sur internet, il existe cependant un autre projet de protocole qui pourrais permettre de sécuriser ces échanges.

# XFR over TLS

Le protocole [XoT](https://tools.ietf.org/html/draft-ietf-dprive-xfr-over-tls-11) (XFR over TLS) est encore à l'état de "draft" (brouillon) mais il permettrait de pallier à ce problème en chiffrant les requêtes grâce au protocole TLS. Il existe malgré tout une implémentation expérimentale de XoT dans le logiciel [Bind](https://gitlab.isc.org/isc-projects/bind9), XoT est donc un protocole très prometteur afin de garantir la confidentialité des transferts de zone.

Merci d'avoir lu cet article, on se retrouve demain pour parler de l'allocation des adresses IP sur
internet🙂.

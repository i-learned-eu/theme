Author: Eban 
Date: 2021/05/30
Keywords: réseau, sécurité, tls
Slug: tls
Summary: TLS est un protocole que nous utilisons quotidiennement, il est notamment utilisé dans HTTPS pour sécuriser la connexion, explorons ensemble le fonctionnement de ce protocole.
Title: Comment fonctionne le protocole TLS

TLS est un protocole que nous utilisons quotidiennement, il est notamment utilisé dans `HTTPS` pour sécuriser la connexion. TLS est le successeur de SSL, nous verrons prochainement pourquoi SSL a été abandonné au profit de TLS. Dans cet article, nous étudierons TLS1.3 qui est la dernière version du protocole sortie en 2018. TLS se base à la fois sur le chiffrement asymétrique et le chiffrement symétrique. Un échange de clé (appelé handshake ou poignée de main) a lieu au début de la connexion, une clé secrète est échangée de façon asymétrique, cette clé est ensuite utilisée pour chiffrer les données (du chiffrement symétrique donc). Voyons donc plus en détail comment se passe un handshake avec TLS1.3. 

![Schémas d'un handshake TLS1.3](/static/img/tls/handshake.png)

Le client envoie donc dans un premier temps un `**Client Hello**` qui contient entre autre :

- Les différents protocoles cryptographiques (pour le chiffrement asymétrique et symétrique) qu'il supporte.
- `Key Share` qui correspond a la clé publique du client, vous vous demanderez surement comment le client peut bien envoyer sa clé publique s'il ne sait pas les protocoles que le serveur supporte, c'est une différence majeur par rapport à TLS 1.2, avec TLS 1.3 le client part du principe que le serveur supporte un certain nombre de protocoles et envoie sa clé publique pour un de ces protocoles, s'il s'avère que ce n'est pas le cas, le serveur va renvoyer un `HelloRetryRequest` ainsi que les protocoles qu'il supporte.

Le serveur répond ensuite avec un `**Server Hello**` qui contient entre autre :

- Le Certificat TLS qui permet d'assurer l'authenticité du serveur.
- Le `Certificate Verify` qui correspond à la signature du handshake, il est utilisé pour s'assurer que  le hanshake n'a pas été modifié en cours de cours (dans le cas d'un attaque [Man In The Middle](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) par exemple).
- `Change Cipher Spec` indique à l'autre participant le passage à un mode de chiffrement symétrique.
- Dans `Key Share` le serveur indique sa clé publique
- `Finished` indique enfin la fin du handshake pour le client.

Le client envoie enfin pour terminer un `Change Cipher Spec` et `Finished`. Vous trouverez [ici 📎](/static/misc/tls/tls_1_3.pcapng) un pcap d'un requête avec TLS 1.3.

En parcourant vous verrez que la version de TLS affichée est TLS 1.2, *it's not a bug, it's a feature* c'est en fait pour éviter que certaines middlebox <s>de merde 😡</s>, utilisées notamment en entreprise pour espionner le trafic, bloquent le trafic pour des version de TLS au dessus de TLS 1.2.

Des paires de clés publique/privée sont dérivées un clé secrète afin de chiffrer de façon symétrique les échanges. Nous détaillerons bientôt plus en détail ce fonctionnement au travers d'ECDH.

Vous l'aurez sûrement remarqué, le nom de domaine est en clair dans les requêtes, à la base une fonctionnalité appelée ESNI (Encrypted Server Name Indication) qui permet de chiffrer le nom de domaine dans les requêtes aurait dû être implémentée dans TLS 1.3 mais ce n'est pas encore le cas, ESNI n'est qu'à l'état de [draft](https://www.ietf.org/archive/id/draft-ietf-tls-esni-10.html)... 😕

Une autre fonctionnalité importante dans TLS 1.3 est le 0 RTT, c'est une fonctionnalité très controversée car elle ne respecte pas le principe de `forward-secrecy`, si un attaquant arrive à trouver la clé utilisée pour le chiffrement symétrique, il pourra déchiffrer toutes les prochaines requêtes. Elle consiste, pour faire simple, à garder une même clé symétrique pour plusieurs échanges afin de reprendre un échange sans avoir à faire de handshake, mais cette fonctionnalité est une fausse bonne idée...

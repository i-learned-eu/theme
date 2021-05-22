title: Sécuriser NTP, à quoi bon ?
Keywords: ntp, time, nts, autokey
Date: 2021-05-15
author: Eban
summary: Nous avons vu jeudi comment fonctionne le protocole NTP mais il reste un dernier point à aborder, comment assurer l'intégrité des données transmises via NTP ? C'est ce que nous allons voir dans cet article :).
Slug: securiser_ntp
Category: Today I Learned

Nous avons vu jeudi comment fonctionne le protocole NTP mais il reste un dernier point à aborder, comment assurer l'intégrité des données transmises via NTP ? Vous vous demanderez sûrement, à quoi bon sécuriser le protocole NTP, alors qu'il ne transmet que le temps 🤔. Le temps est une donnée très importante en informatique, plus qu'on ne pourrait le penser de prime abord, il est utilisé dans de nombreux protocoles cryptographiques, comme par exemple dans `TLS` ou [`DNSSEC`](https://blog.eban.bzh/today-i-learned/dnssec.html) avec le système de TTL (time to live). Pour sécuriser NTP de nombreux protocoles ont été proposés et mis en place, nous en citerons ici trois.

## Le chiffrement symétrique

Dans NTP3 est ajouté le système d'authentification par clés symétriques, un secret partagé est échangé la première fois entre le client et le serveur et c'est ce secret qui est ensuite utilisé pour sécuriser la connexion. Mais cette méthode pose un gros problème, il est nécessaire d'échanger une clé secrète la première fois, elle est donc très difficilement automatisable et impossible à déployer à grand échelle.

## Autokey

Une autre approche a été `autokey`, ce système utilisé du [chiffrement asymétrique](https://fr.wikipedia.org/wiki/Cryptographie_asym%C3%A9trique) et résous donc les problèmes qui se posaient avec le chiffrement symétrique, en partie seulement, car le protocole `autokey` a de grosses lacunes en terme de sécurité, un comble, effet la taille du cookie utilisé pour s'authentifier avec autokey est de seulement 32 bits, ce qui le rend très vulnérable, mais ce n'est pas le seul problème d'autokey, le client n'est identifié que par son IP, un attaquant pourrait donc se faire passer pour le client et dérober le cookie.

## Network Time Security (NTS)

Pour pallier aux faiblesses de ces deux protocoles, un nouveau protocole est un cours de création, NTS (standardisé dans la [RFC 8915](https://datatracker.ietf.org/doc/rfc8915/) il se base sur le principe du chiffrement asymétrique sans les problèmes d'autokey. Ce protocole se base en partie sur TLS pour l'échange de clés, il utilise ensuite les parties des headers spécifiques à NTP pour sécuriser le reste de la connexion. C'est un protocole prometteur mais qui n'est malheureusement pas encore assez implémenté.

lang: fr
Title: Fonctionnement de DNSSEC
Keywords: DNSSEC, DNS, sécurité, DS, NSEC, RSSIG, KSK, ZSK
Date: 2021-04-29
author: Ramle
summary: Aujourd'hui, on va parler du fonctionnement de DNSSEC et voir les différents risques encourus que ce mécanisme résout ou non.
slug: dnssec
Category: Réseau/DNS

Petit rappel: ce blog a un [flux RSS](https://ilearned.eu/rss.xml), n'hésitez pas à l'ajouter à votre lecteur de flux RSS favori :)

Hier nous avons vu comment sécuriser la connexion entre un serveur slave et un serveur master, mais le problème d'authenticité des réponses se pose encore, pour commencer le trafic entre le serveur autoritaire et résolveur n'est pas chiffré, n'importe quel attaquant qui pratique une attaque type [`MITM`](https://fr.wikipedia.org/wiki/Attaque_de_l%27homme_du_milieu) peut donc modifier les réponses. Le canal n'est pas le seul problème, surtout qu'il est déjà possible de sécuriser le canal entre résolveur et autoritaire, et entre le résolveur et le client via `DoT` (DNS over TLS) et `DoH` (DNS over HTTPS), nous en parlerons plus largement demain ;). Sécuriser le canal si le serveur est corrompu ne sert pas à grand chose, c'est la raison pour laquelle `DNSSEC` (`RFC 4033`) a été inventé.

![Schéma sur les risques sans DNSSEC](/static/img/dns/schema_risques_dnssec.webp)

`DNSSEC` est une manière de signer de façon cryptographique une zone DNS sur base d'un système de clés asymétriques, un système de clés asymétriques repose sur 2 clés, une privée qui est gardée précieusement et qui sert à signer ou déchiffrer des données et une publique qui sert à vérifier ou chiffrer des données. Dans le cadre du DNSSEC le chiffrement ne sert pas, la clé privée sert donc uniquement à signer.

Pour procéder on utilise en général deux pairs de clés : la `KSK` (key-signing key) et la `ZSK` (zone-signing key). La clé KSK est seulement là pour la signature de la ZSK, on lui donne une durée de vie plus grande que la ZSK et elle peut être stockée et générée hors ligne pour accroitre la sécurités de celle ci, l'avantage de ce système est de pouvoir garder plus longtemps la même clé sans rajouter trop de risque de fuite vu que stockée hors ligne, dans un lieu sécurisé. La ZSK quand à elle est sert à signer la zone, elle doit donc être présente sur la machine qui génère la zone, on la change plus souvent pour éviter les risques de fuites. Les serveurs esclaves n'ont besoin d'aucune des 2 clés, ils reçoivent directement la zone signée, la modification de la zone de leur part n'est donc plus possible si le résolveur vérifie avec DNSSEC.

DNSSEC ne signe pas la zone de manière entière, mais signe chaque enregistrement indépendamment, la signature est contenue dans le record de type `RSSIG`. Ce fonctionnement pose un soucis si il permet de signer une entrée DNS, comment prouve t'on inexistante d'un enregistrement ? Pour résoudre cette problématique l’enregistrement de type `NSEC` existe.

NSEC est un moyen de prouver l’inexistence (symbolisé par le code de retour `NXDOMAIN`) d'un record en donnant le prochain (par ordre alphabétique) enregistrement de la zone, un problème de confidentialité se pose avec cet méthode, il est en effet très simple d'énumérer la liste d'enregistrement. Pour empêcher ce type d'attaque NSEC3 est né, au lieu de donner le FQDN on ne retourne que le condensat, l'énumération devient donc impossible.

Une dernière problématique, et pas des moindres existe, comment s'échanger de manière fiable les clés à grande échelle ? On ne peut pas se les donner de personne à personne, c'est ingérable au vu du nombre de zones présentes sur internet. Pour résoudre cette problématique deux enregistrements existent : DS et DNSKEY.

Commençons pas DNSKEY, il permet d'enregistrer la clé publique qui signe la zone, cette enregistrement est stocké dans la zone elle même.

Avec uniquement DNSKEY on ne peut pas valider correctement la zone, la fiabilité de la chaine n'est pas garantie, il slave pourrait modifier ce record pour modifier la zone à sa guise, pour vérifier il existe donc un enregistrement DS qui se situe dans la zone parente et permet de faire une référence à la clé publique utilisée pour signer la zone du FQDN, c'est le registrar qui s'occupe de faire placer cet enregistrement. Pour ce qui est de la zone `.` il est impossible de définir un record DS au dessus, car c'est la zone la plus basse, l'IANA donne donc la clé utilisée et c'est disponible ici : [https://www.iana.org/dnssec/files](https://www.iana.org/dnssec/files).

![Schéma fonctionnement DNSSEC](/static/img/dns/schema_dnssec.webp)

C'est tout pour cet article, j'espère que ça vous aura plus. Si vous avez des remarques ou questions n'hésitez pas en commentaire. On se retrouve demain pour parler de **DNS over TLS et DNS over HTTPS** :)

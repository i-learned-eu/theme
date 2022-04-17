lang: fr
Title: Les bases du DNS
Keywords: DNS, Domain Name System, NS, knot, bind, apprendre, bases DNS, DNS simple
Summary: Pour ce premier post dans la catégorie Today I Learned, on repart des bases, aujourd'hui on parle de DNS 😄.
Date: 2021-04-24
Author: Eban
Category: Réseau/DNS

Pour ce premier post dans la catégorie *Today I Learned*, on repart des bases, aujourd'hui on parle de DNS 😄. Pour les lecteurs les plus expérimentés connaissant déjà bien les bases du système de DNS, rendez-vous demain 😉. Les prérequis pour aborder cet article sont : des **petites bases de réseau**, la notion d'IP, de nom de domaine, et ça devrait suffire :) Vous trouverez à chaque fois en début d'article une petite "carte mentale" représentant les sujets que nous aurons déjà abordé en lien avec cet article, afin que vous puissiez avoir un accès plus facile aux pré-requis il suffit de cliquer sur le nom de l'article ou de la notion dans le schéma pour avoir le lien.

Le DNS (Domain Name System) est un protocole permettant de "traduire" un [nom de domaine](https://www.wikipedia.com/wiki/Domain_name) en une [adresse IP](https://www.wikipedia.com/wiki/IP_address). Il existe deux types de serveurs DNS, les serveurs DNS résolveur, aussi appelés récurseurs (comme 1.1.1.1 ou 80.67.169.40 par exemple) servent à "traduire" un nom de domaine en adresse IP, et les serveurs DNS autoritaires, ce type de serveur DNS "fait autorité" sur une zone DNS (une zone DNS c'est l'ensemble des enregistrement DNS, une sorte de base de donnée qui fait la relation entre nom de domaine et IP), c'est à lui que vont se référer les serveurs DNS résolveurs pour associer nom de domaine et IP. Ça fait beaucoup de termes d'un coup 😅 pour rendre ça plus clair voici un petit schéma et les définitions.

- DNS

    Domain Name Système, protocole servant à traduire un nom de domaine en une adresse IP

- Zone DNS

    Ensemble des enregistrement DNS, sorte de base de donnée qui fait la relation etre nom de domaine et IP

- Serveur DNS récurseur

    Serveur DNS "intermédiaire" qui fait office de passerelle etre les serveurs DNS autoritaires et l'utilisateur

- Serveur DNS autoritaire

    Contient tout les enregistrement DNS d'une zone.

![Frame 1](/static/img/les-bases-des-dns/schema4.webp)

Vous l'imaginez bien, les informations ne sont pas stockées tel-quel sur les serveurs DNS, ils sont stocké sous forme d'enregistrement DNS, en voici un exemple commenté tout droit tiré de mon propre serveur DNS autoritaire.

```
eban.bzh.	1800 IN A 89.234.156.60
```

`eban.bzh.` correspond au domaine que nous avons demandé, vous vous demanderez sûrement, mais pourquoi y a-t-il un . à la fin ? *Comment ça vous ne vous êtes pas posé la question ? 😛* En fait, la résolution des DNS fonctionne sous forme de couches, voici un petit schéma qui explique tout ça

![Frame 2](/static/img/les-bases-des-dns/schema2.webp)

Les serveurs DNS "root" correspondent à la première couche, ils contiennent les records DNS pour tous les `TLD` *Un TLD ? Quèsaco ?* Un TLD (Top level domain name) c'est en fait tout les `.` quelque chose que vous rencontrez au quotidien, `bzh` , `fr`, `com`, `be` en sont quelques exemples. Les serveurs DNS root contiennent donc les record correspondants aux TLD.

Les TLD, `bzh.` dans notre exemple, contient quant à lui les informations sur les domaines de sa zone, `*.bzh.`.

`eban.bzh.` pour finir contient tout les records pour `eban.bzh.` et tout ses sous-domaines (`git.eban.bzh.`, `blog.eban.bzh.`...) cette "couche" est appelée `FQDN` (Fully Qualified Domain Name). Pour rendre tout ça plus simple voici (à nouveau :p) un petit schéma.

![Frame 3](/static/img/les-bases-des-dns/schema3.webp)

Et voilà le schéma corrigé d'une requête DNS.

![Frame 4](/static/img/les-bases-des-dns/schema1.webp)

Ces petites explications faites, continuons avec notre record `eban.bzh.	1800 IN A 89.234.156.60`.

`1800` correspond au [TTL](https://www.wikiwand.com/fr/Time_to_Live) (Time to Live) de ce record, c'est le temps en secondes après lequel le serveur DNS résolveur devra réinterroger le serveur DNS autoritaire afin de mettre à jour son cache. Le serveur DNS résolveur gardera donc ce record en cache pendant `1800 secondes` puis réinterrogera le serveur DNS autoritaire à la prochaine requête si ce temps est passé.

`IN A` correspond au type du record, ici `A` qui correspond à un record qui renvoie une adresse IPv4, il existe de nombreux autres types de records, vous trouverez ci-dessous une liste des plus courants.

`89.234.156.60` enfin correspond à l'adresse IP qui nous est renvoyée.

|Type |Définition                                                                                                                                                                                                                                                                                                                                                                                             |Exemple                                                                             |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
|A    |Renvoie une Ipv4                                                                                                                                                                                                                                                                                                                                                                                       |`eban.bzh. 1800 IN A 89.234.156.60`                                                   |
|AAAA |Renvoie une Ipv6                                                                                                                                                                                                                                                                                                                                                                                       |`eban.bzh. 1800 IN AAAA 2a03:7220:8083:3c00::1`                                       |
|CNAME|Renvoie vers un autre record                                                                                                                                                                                                                                                                                                                                                                           |`blog.eban.bzh. 1800 IN CNAME veil.eban.bzh.`                                         |
|NS   |Spécifie les NS d'une zone                                                                                                                                                                                                                                                                                                                                                                             |`eban.bzh. 1800 IN NS ns1.eban.bzh.`                                                  |
|MX   |Indique les serveurs [SMTP](https://www.wikiwand.com/fr/Simple_Mail_Transfer_Protocol) (mail) à utiliser                                                                                                                                                                                                                                                                                                       |`eban.bzh. 1800 IN MX 10 spool.mail.gandi.net.`                                       |
|SOA  |Contient les informations suivantes, dans l'ordre : <br>  `Serveur DNS autoritaire principal` <br> `Email de contact`, le @ est remplacé par un point, l'adresse ici est donc ns@eban.bzh <br> `Serial` "version" de la zone <br> `Refresh` délai en secondes entre demandes d'update des slaves <br> `Retry` délai en secondes entre demandes d'update lors d'un fail <br> `Expire` expiration de la zone <br> `Minimum TTL` TTL pour les records inexistants|`eban.bzh. 86400 IN SOA ns1.eban.bzh. ns.eban.bzh. 1618240745 10800 3600 604800 10800`|

Si vous voulez essayer d'interroger les serveurs DNS à la main, `dig(1)` est un bon outil, il existe aussi la commande `nslookup` pour les <s>hérétiques</s> personnes sous Windows.

Pour les plus curieux, voici un petit bonus :) Nous allons analyser ce qui se passe concrètement sur un réseau local lors d'un requête DNS vers un serveur DNS résolveur.
Cette petite analyse est faite sur un système basé sur `linux` mais est aussi valable pour Windows. J'ai donc capturé le trafic sortant de ma machine avec un outil nommé `tcpdump(8)`. Et voici ce que l'on obtient

```
10:31:13.272734 IP 10.2.0.2.60081 > 10.0.0.1.53: proto UDP A? eban.bzh. (37)
10:31:13.309725 IP 10.0.0.1.53 > 10.2.0.2.60081: proto UDP A 89.234.156.60 (53)
```

On voit donc que l'ordinateur va interroger le serveur DNS (ici sur `10.0.0.1`) sur le port 53 qui est le port par défaut du protocole DNS pour lui demander un record `A` pour la zone `eban.bzh.`. On remarque aussi que ce protocole est basé sur le protocole `UDP` que nous étudierons sûrement d'ici peu longtemps ;). Le serveur DNS répond ensuite à la demande en renvoyant le type de record (ici `A`) et l'adresse IP demandée.

Voilà, c'en est finit pour ce premier post de la catégorie Today I Learned, demain nous nous intéresserons au fonctionnement à la fonction d'un **`registrar`** ainsi qu'au fonctionnement des serveurs DNS autoritaires sur le principe de **`slave/master`**.

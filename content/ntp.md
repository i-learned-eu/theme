Title: NTP, comment ça marche ?
Keywords: ntp, time
Date: 2021-05-13
Author: Eban
Summary: Depuis la démocratisation d'internet et de l'informatique en général, une question s'est posée, comment faire en sorte que les horloges de tous les ordinateurs soient coordonnées ? Aujourd'hui, regardons de plus près le protocole NTP qui répond à cette problématique.
Slug: ntp

Depuis la démocratisation d'internet et de l'informatique en général, une question s'est posée, comment faire en sorte que les horloges de tous les ordinateurs soient coordonnées ? En septembre 1985 une première version du protocole NTP (Network Time Protocol) est publiée dans la [RFC 958](https://datatracker.ietf.org/doc/html/rfc958), ce protocole se base sur [UDP](https://blog.eban.bzh/today-i-learned/udp.html) pour sa légèreté. NTP fonctionne sur une typologie de réseau dite *mesh*, elle est découpée en strates afin de délivrer un temps équivalent partout et d'assurer une redondance. 

![L'architecture de NTP](/static/img/ntp/schema_archi.png)

Les serveurs de strate 1 sont les horloges principales, le temps qu'elles donne peut provenir de différentes sources comme le [GPS](https://en.wikipedia.org/wiki/Global_Positioning_System) ou une [horloge atomique](https://fr.wikipedia.org/wiki/Horloge_atomique). Les serveurs des strates plus basse s'échangent entre eux leur temps afin de vérifier qu'il correspond bien. Quand nous, utilisateurs, accédons à un serveur NTP, on accède bien souvent à un serveur de strate 2 ou 3.

Voici à quoi ressemble une requête NTP : 

![Les headers d'une requête NTP](/static/img/ntp/schema_headers.png)

Ça fait pas mal de parties 😄. Nous ne commenterons ici que les plus importantes.

LI, Leap Indicator indique une [seconde intercalaire](https://fr.m.wikipedia.org/wiki/Seconde_intercalaire) imminente. Une seconde intercalaire correspond, pour faire simple, à une seconde ajoutée sur toutes les horloges occasionnellement afin de synchroniser le temps universel coordonné (UTC) avec le temps solaire. 

VN, Version Number indique simplement la version de NTP utilisée.

Mode, indique le mode dans lequel est l'émetteur, client, serveur etc.

Poll correspond à l'intervalle à laquelle le client doit reinterroger le serveur NTP.

Root delay correspond au temps pour faire un aller-retour vers un serveur de strate 1. Et root dispersion est une estimation de la marge d'erreur du serveur de strate 1.

Reference ID correspond au type d'outil utilisé par le serveur root (strate 1) comme par exemple le GPS ou une horloge atomique.

Reference Timestamp est le temps de la dernière mise à jour via NTP. 

Les trois autres timestamps sont décris ci-dessous 

![Schéma représentant les différents timestamp](/static/img/ntp/schema_timestamps.png)

Le `destination timestamp` n'est logiquement pas inclut dans les headers, il est dans ce schéma à titre informatif.

Ça fait beaucoup de paramètres 😅 Mais grâce à toutes ces informations on peut avoir une précision de l'ordre de quelques nanosecondes en soustrayant le temps de transfert !

Un dernier problème se pose, comment assurer le fait que le serveur NTP ne se fasse pas usurper ? Nous avons déjà étudié dans d'autres articles des moyens de signature cryptographique, NTP implémente aussi une solution de ce type que nous étudierons très prochainement :). 

Merci d'avoir lu cet article, j'espère qu'il vous a plu 😄.

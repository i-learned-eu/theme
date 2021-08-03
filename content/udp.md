Title: Comprendre le protocole UDP
Keywords: udp, réseau, networking, ip
Date: 2021-05-12
Author: Ramle
Summary: Nous avions récemment vu TCP, ce protocole essaye d'avoir la meilleur fiabilité possible pour la transmission, mais un certain nombre d'échanges sont requis pour vérifier l’intégrité du flux ce qui rajoute de la latence qui dans certains cas, est problématique. UDP est un protocole qui tente de résoudre ce problème.
Slug: udp
Category: Today I Learned

Nous avions récemment vu le fonctionnement de [TCP](https://blog.eban.bzh/today-i-learned/tcp.html), ce protocole essaye d'avoir la meilleur fiabilité possible pour la transmission, mais un certain nombre d'échanges sont requis pour vérifier l’intégrité du flux ce qui rajoute de la latence qui dans certains cas, est problématique. UDP est un protocole qui tente de résoudre ce problème.

UDP est l'acronyme de User Datagram Protocol (traduit par protocole de datagramme utilisateur), ce protocole se base sur IP et fait partie de la couche transport du [modèle OSI](https://fr.wikipedia.org/wiki/Mod%C3%A8le_OSI). Contrairement à TCP il ne fait pas de "poignée de main" (ou handshake en anglais) et ne nécessite pas d'accusé de réception (ACK), cette manière de fonctionner le rend plus tolérant à un réseau défectueux et lui permet un latence plus faible. Il n'est utile que dans des cas où une perte de paquet ne pose pas un soucis important. UDP est utilisé dans certains protocole très utilisé comme NTP, DNS, ou plus généralement les applications qui ont besoins de temps réel comme les jeux vidéo ou certains services de streaming.

Comme je l'ai dis plus haut UDP ne vérifie pas la bonne réception d'un paquet (contrairement à TCP avec son système d'ACK), la machine envoie donc le paquet sans forcément attendre un retour. Ce protocole est bien plus simple que TCP dans sa conception. Un paquet UDP se compose tel que décrit sur ce schéma :

![Schéma d'une trame UDP](/static/img/udp/schema_trame.png)

Comme on peut le voir, il y a un minimum d'information comparé à TCP, le port source qui permet si besoin de répondre, le port de destination, la longueur totale du segment UDP (données comprises), une somme de contrôle (hash) et les données en elle même, chaque entrée de l'en-tête fait 16 bits ce qui au total fait 64 bits pour la partie header contre 192 avec TCP ! La partie données a une longueur variable.

Comme à notre habitude, regardons une capture réseau :
![Capture d'une requête DNS](/static/img/dns/dns_capture.png)
On remarque directement la simplicité, 2 requêtes seulement pour un aller retour, chaque paquet est aussi assez léger, moins de 100 octets à chaque fois, pour ce qui est des nombres "0.000000" et 0.000093" il s'agit du temps où ont été capturés chaque paquet. Si vous voulez regarder plus en profondeur la capture réseau, je vous laisse le fichier disponible [ici](/static/misc/dns.pcap).

C'est tout pour cet article sur UDP, j'espère que vous l'aurez apprécié. On se retrouve demain pour parler de **NTP** :).

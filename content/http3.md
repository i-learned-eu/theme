Author: Ramle 
Date: 2021-05-18
Keywords: HTTP, http3, QUIC
Slug: http3
Title: Comment fonctionne HTTP/3 ?
Summary: Dans l'article du jour nous allons voir comment fonctionne HTTP/3 et QUIC.

Il n'y a pas longtemps nous avions découvert le fonctionnement d'[HTTP](https://blog.eban.bzh/today-i-learned/http.html), et différentes versions de ce protocoles, mais l'une d'elle n'a pas été vue : HTTP/3, cette version apporte un changement sur la méthode de transport en se basant sur QUIC qui lui même utilise [UDP](https://blog.eban.bzh/today-i-learned/udp.html) au lieu de [TCP](https://blog.eban.bzh/today-i-learned/tcp.html).

Pour commencer, regardons de plus près QUIC, il existe pour le moment deux versions de ce protocole, une faite par Google qui n'a pas été standardisée, et une qui est en cours de rédaction pour être publiée sous forme d'une RFC à l'IETF (l'organe qui s'occupe de la publication des RFC). La version de Google se concentre sur HTTP/3, contrairement à la version de l'IETF qui veut faire de QUIC un protocole de transport servant pour d'autres usages que [HTTP](https://blog.eban.bzh/today-i-learned/http.html), pour le [DNS](https://blog.eban.bzh/today-i-learned/les-bases-du-dns.html) par exemple.

Pour le moment l'IETF (qui se base en partie sur les travaux de Google) est encore au stade de rédaction de la norme et se concentre sur HTTP/3 comme usage pour la première version. Cet article se basera sur les travaux de l'IETF et non ceux de Google.

Pour commencer, QUIC se base sur [UDP](https://blog.eban.bzh/today-i-learned/udp.html) et veut résoudre certains problème de [TCP](https://blog.eban.bzh/today-i-learned/tcp.html), avec HTTP/2 par exemple, plusieurs transferts sont effectués sur un seul flux [TCP](https://blog.eban.bzh/today-i-learned/tcp.html), je vous renvoie vers l'article sur [HTTP](https://blog.eban.bzh/today-i-learned/http.html) qui explique en détail ce concept, avec [TCP](https://blog.eban.bzh/today-i-learned/tcp.html) si dans la liste des paquets en attente un paquet se perd tous les paquets avant celui perdu devront attendre le renvoi. On peut faire un parallèle avec un embouteillage de voiture, si une voiture bloque la route, celles qui précèdent la voiture devront attendre son passage.

![Congestion des paquets](/static/img/congestion_http.png)

TCP rajoute aussi une latence importante due aux différents handshakes, [UDP](https://blog.eban.bzh/today-i-learned/udp.html) n'utilise pas de séquence de handshake. QUIC en rajoute pour assurer un minimum de fiabilité. On compte au total 4 aller-retours pour récupérer une page (ou un code d'erreur) contre 6 dans les versions d'HTTP basée sur [TCP](https://blog.eban.bzh/today-i-learned/tcp.html). Le client commence par l'envoi d'un "hello" pour donner différents paramètres sur lui, ensuite le serveur répond en envoyant directement le certificat et les informations pour commencer l'échange de donnée, le client envoie ensuite sa requête avec la méthode. Le client finit par y répondre par le code de retour ou la page demandée.

![Comparaison handshake HTTP vs HTTP/3](/static/img/http_handshake_vs.png)

QUIC fonctionne sur [UDP](https://blog.eban.bzh/today-i-learned/udp.html) comme dit plus haut, il force un certain niveau de sécurité en imposant TLS en version 1.3, pour les communications. Il offre aussi une certaine fiabilité qu'UDP ne possède pas, rappelez-vous, [UDP](https://blog.eban.bzh/today-i-learned/udp.html) ne vérifie rien. QUIC résout ce problème en ajoutant une couche qui permet de gérer une retransmission de paquet au cas où celui-ci se perdrait en chemin, il permet aussi un contrôle de la congestion, la congestion en réseau c'est la saturation du réseau en lui même, cela cause un ralentissement ou une perte de paquet dans les cas extrêmes, le protocole est donc pas loin de [TCP](https://blog.eban.bzh/today-i-learned/tcp.html) sur la fiabilité.

Sur un seul canal [UDP](https://blog.eban.bzh/today-i-learned/udp.html), QUIC permet de faire placer plusieurs flux en simultané.

![Canal QUIC](/static/img/quic.png)

Pour le moment, nous avons vu principalement QUIC, la raison est que HTTP/3 n'apporte pas grand chose, c'est HTTP/2 adapté pour passer au dessus de QUIC, il y a quelques différences mineures comme la compression des en-têtes qui est adapté au protocole, mais les modifications sont mineure et viennent surtout adapté [HTTP](https://blog.eban.bzh/today-i-learned/http.html) pour QUIC. Le rapprochement avec HTTP/2 est plutôt logique d'ailleurs si on regarde la chronologie le travail sur HTTP/3 à commencé dans la même période.

![Couche HTTP/3](/static/img/couche_http3.png)

Un point utile à aborder est de savoir comment le client sait si il doit communiqué en HTTP/3 ou non. En effet, les anciennes version d'HTTP utilise [TCP](https://blog.eban.bzh/today-i-learned/tcp.html) contrairement à HTTP/3 qui utilise [UDP](https://blog.eban.bzh/today-i-learned/udp.html). Pour informer le navigateur de la présence d'HTTP/3 l'en-tête `Alt-Svc` à été crée, elle indique le port [UDP](https://blog.eban.bzh/today-i-learned/udp.html) sur le quel le client doit aller voir, on peut aussi via l'en-tête indiquer un domaine différent.

L'amélioration qu'apporte HTTP/3 est relativement mineure mais se révèle assez utile, sur une connexion stable avec peu de perte de paquet la différence n'est pas forcément visible, mais sur un réseau saturé avec un grand nombre de perte ne pas renvoyer toute la queue à chaque perte est un gain non négligeable. Une observation faite par certains est que HTTP/3 demande plus de CPU pour le serveur, ça peut être un frein pour le déploiement. Il faut aussi gardé en tête que QUIC est assez nouveau, les implémentations ne sont pas encore parfaite, le temps dira si ce protocole vaut le coup ou non.

Niveau performance, HTTP/3 apporte un gain au niveau de la latence grâce à la poignée de main réduite, pour ce qui est de la vitesse de chargement, la prioritisation des flux, et la possibilité d'envoyer sur plusieurs flux en simultané permet de gagner un peu. Selon [Cloudflare](https://blog.cloudflare.com/http-3-vs-http-2/) HTTP/3 améliore le temps d'établissement de la première connexion de 12,4%, pour ce qui est du chargement d'une page, ici leur propre blog, le temps diminue entre 1 et 4%, c'est au final assez peu, mais sur une connexions assez lente quelques pour-cent n'est pas négligeable.

Si vous regardez un peu en détail votre navigateur vous remarquerez qu'HTTP/3 n'est pas encore activé par défaut, en effet ce protocole bien que prometteur n'est pas encore standardisé et est très minoritaire. Si par curiosité vous voulez tout de même activé dans `about:config` sur votre firefox vous pouvez changez la configuration `network.http.http3.enabled` vers `true`. Sachez toutefois que des sites comme celui de Cloudflare où de Google intègrent déjà HTTP/3 ! 

J'espère que cet article vous aura plus :), on se retrouve demain pour parler de **radius.**

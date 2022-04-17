lang: fr
Title: Comprendre le protocole TCP
Keywords: tcp, udp, réseau, networking, tcp/ip, ip
Date: 2021-05-04
Author: Eban
Summary: Aujourd'hui on s'attaque à un gros morceau, le protocole `TCP`, vous êtes prêt·e·s ? C'est partit ! ;)
Slug: tcp
Category: Réseau

Aujourd'hui on s'attaque à un gros morceau, le protocole `TCP`, vous êtes prêt·e·s ? C'est partit ! ;) TCP (= Transmission Control Protocol) est le protocole de [couche 4](https://fr.wikipedia.org/wiki/Couche_transport) le plus utilisé et il fait partie intégrante de nos vies sans que nous ne nous en rendions compte. TCP a été créé afin de répondre à une problématique simple, permettre la communication de façon fiable entre deux machines. TCP est basé, comme de nombreux protocoles, sur une architecture `client-serveur`. Les données sont découpées en blocs appelés segments.

La communication s'effectue en trois parties : l'établissement de la connexion, le transfert des données, la fin de la connexion. Commençons donc par l'établissement de la connexion, il est fait grâce à un [handshake en trois étapes](https://fr.wikipedia.org/wiki/Three-way_handshake) (Three-way handshake), la première étape est nommée `SYN` (synchronized), le client va donc envoyer un paquet `SYN` au serveur avec lequel il souhaite entamer la communication, il génère aussi aléatoirement un numéro de séquence qui est transmit dans ce paquet. Le serveur répond ensuite avec un paquet `SYN-ACK` (synchronize, acknowledge), littéralement *accusé de réception de la demande de synchronisation*, le numéro de séquence du serveur est généré aléatoirement, le numéro d'acquittement correspond au numéro de séquence du client incrémenté d'un. Pour finir, le client envoie un dernier paquet `ACK` au serveur pour confirmer qu'il a bien reçu le paquet `SYN-ACK`, le numéro de séquence de ce paquet est égal à celui généré par le client plus tôt + un, le numéro d'acquittement quant a lui est égal au numéro de séquence du serveur augmenté de 1.

Ne vous en faites pas, nous allons voir plus précisément à quoi correspondent les numéros d'acquittement et de séquence ;).

![Comprendre%20le%20protocole%20TCP%20c2ad32e581ef4daebd3dee3d401ad213/Frame_25.webp](/static/img/tcp/Frame_25.webp)

Une fois cette initialisation faite, la communication peut commencer, regardons donc de plus près le contenu d'un paquet TCP, accrochez vous il y a pas mal de contenu 😄. Cette partie s'appuie en grand partie sur [l'article wikipedia de TCP](https://fr.wikipedia.org/wiki/Transmission_Control_Protocol#D%C3%A9veloppement_de_TCP). Nous ne détaillerons pas l'utilité de chacune de ces informations, seulement des plus importantes à nos yeux.

![Comprendre%20le%20protocole%20TCP%20c2ad32e581ef4daebd3dee3d401ad213/Frame_26.webp](/static/img/tcp/Frame_26.webp)

Les numéros d'acquittement et de séquence sont deux valeurs aléatoires que l'on incrémente avec le nombre de données reçues afin de vérifier que tout les paquets sont bien arrivées dans l'ordre. Les numéros d'acquittement et de séquence initiaux sont générés aléatoirement durant la séquence d'initialisation de la connexion que nous avons vu plus tôt, le three way handshaking.

Le partie "Somme de contrôle" est en fait un condensat des données transmises qui est calculé par le serveur et vérifié par le client afin de garantir l'intégrité des paquets. Si les hash correspondent on considère alors que le paquet a été transmit sans erreur.

![Comprendre%20le%20protocole%20TCP%20c2ad32e581ef4daebd3dee3d401ad213/Frame_27.webp](/static/img/tcp/Frame_27.webp)

Le flag `PSH` (push) indique l'envoie de données.

Le flag `URG` indique la présence de données urgentes.

Le flag `ECN/NS` sert quant à lui à signaler la présence de congestion sur le réseau.

Dans la partie `Options` on pourrait par exemple citer la MSS (Maximum Segment Size) qui correspond à la taille maximale de la partie data.

Nous avons vu les parties les plus importantes d'un trame TCP, étudions maintenant comment fermer une session avec le protocole TCP.

Pour fermer une session TCP, c'est relativement simple, le premier appareil envoie un paquet `FIN` au second avec son numéro de séquence, afin de vérifier que tous les paquets ont été reçu avant de fermer la communication. Le serveur répond alors avec un `ACK` pour confirmer la réception du message. Le même échange a ensuite lieu dans l'autre sens, le serveur envoie un paquet `FIN` et le client répond avec un `ACK`.

![Comprendre%20le%20protocole%20TCP%20c2ad32e581ef4daebd3dee3d401ad213/Frame_28.webp](/static/img/tcp/Frame_28.webp)

Pfiou, ça fait beaucoup d'un coup 😅. Mettons maintenant tout ça en pratique, si vous êtes arrivé jusqu'ici, vous avez fait le plus dur, bravo 🎉.

![Comprendre%20le%20protocole%20TCP%20c2ad32e581ef4daebd3dee3d401ad213/Frame_29(5).webp](/static/img/tcp/Frame_29(5).webp)

Vous remarquerez surement la présence des mentions de `Win`; `TSval` et `TSecr`, regardons à quoi elles correspondent

`Win` correspond à la fenêtre, pour faire simple, la taille maximale d'un paquet.

`TSval` et `TSecr` sont simplement des [timestamps](https://fr.wikipedia.org/wiki/Horodatage), `TSval` correspond au moment de l'envoi du paquet et `TSecr` au moment de la réception, chacun des deux participants de la conversation peut soustraire ces deux valeurs pour déterminer le `Round Trip Time (RTT)`, le temps que prend un paquet à être échangé.

Si vous souhaitez à votre tour inspecter ce simple échange tcp, le fichier est disponible [ici](/static/misc/tcp/record.pcapng), je vous recommande l'outil [Wireshark](https://www.wireshark.org/) si vous voulez inspecter des paquets de ce type.

Vous l'aurez surement remarqué, le protocole TCP a été conçu dans l'optique de minimiser au maximum la perte de donnée, grâce à des fonctionnalité comme les accusés de réception (`ACK`) ou la somme de contrôle. Mais ces fonctionnalités posent un problème, les paquets s'en retrouvent alourdis, la partie somme de contrôle (checksum) pèse à elle seule 16 bits par exemple, autre exemple, pour chaque paquet d'envoie de données (`PSH`), un paquet `ACK` supplémentaire est nécessaire, à chaque fois ! Cette lourdeur pose notamment problème dans le cadre d'applications en temps réel, d'autres protocoles comme UDP que nous étudierons bientôt ont été créés pour remédier à ce problème.

Merci beaucoup d'être arrivé jusqu'ici, cet article était plutôt complexe j'en suis conscient, si vous avez des question n'hésitez surtout pas à les poser, si vous souhaitez commenter n'oubliez pas que vous pouvez vous connecter (avec le bouton *Log In*) via Github, Twitter et Gitlab.

À demain 👋

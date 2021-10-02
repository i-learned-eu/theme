Author: Ramle 
Date: 2021/08/07
Keywords: ipv6, réseau, slaac, RA
Slug: slaac
Title: Auto-configuration sans état en IPv6 (SLACC)

Pour pouvoir communiquer entre des machines d'un réseau IP il est requis de posséder une adresse IP dans le réseau, une méthode simple serait que chaque machine du réseau ait une adresse fixe configurée par l'utilisateur, mais cela serait vite fastidieux et un utilisateur ne connaissant pas à l'avance le réseau serait vite bloqué. Une solution est d'avoir un protocole permettant de distribuer automatiquement aux machines une adresse via un protocole fait pour, pendant longtemps le protocole utilisé était DHCP. Pour IPv6 bien que DHCP soit une possibilité, une autre méthode est plus largement utilisée : SLAAC (Stateless Address Autoconfiguration, SLAAC).

Comme son nom l'indique, SLAAC est sans état ce qui veut dire qu'il n'y a pas forcément un serveur central qui doit retenir une base de donnée avec la listes des machines.

SLAAC se base sur des "router-advert" (RA), le routeur envoie périodiquement des annonces à une adresse multicast spécifique, `FF02::1`, cette adresse correspond à tous les hôtes du réseau, c'est l'équivalent de 255.255.255.255 en IPv4. Le paquet envoyé par le routeur se base sur ICMPv6, et a la forme : 

![Router Advertisement structure du paquet](/static/img/slaac/ra.png)

Les parties importantes du paquet sont :

- Prefix qui est le préfixe du réseau
- Type : qui indique le type de paquet ICMP
- L'adresse source : c'est l'adresse depuis la quelle le paquet est envoyé, en IPv6 toutes les interfaces possèdent une IP utilisé pour les liens locaux, cette adresse est dans le préfixe `FE80::/10`, et dans le cas des RA, cette adresse est utilisée pour que la machine puisse répondre en cas de besoin.

Le soucis de cet envoi périodique est que si un appareil vient de se brancher il doit attendre un certain temps avant que le routeur renvoi un RA, pour palier à ça il existe une requête pour demander au(x) routeur(s) connecté(s) de faire une annonce spécifique pour le nouvel appareil, la demande d'annonce est adressée à un groupe multicast spécifique au routeur, `FF02::2` est le routeur, au lieu de répondre en envoyant son paquet à tout le monde, il envoie uniquement au demandeur via son adresse de lien local.

Cette requête se porte sous cette forme :

![En-tête demande de RA au(x) routeur(s)](/static/img/slaac/134.png)

Comme on peut le voir, le type de paquet ICMP est différent par rapport à un paquet pour les RA.

Comme dit plus haut, SLAAC est sans état, il ne distribue pas d'ip mais uniquement le préfixe et une route par défaut, le préfixe est donc choisit par la machine. Il y a 2 manières principal de faire, utiliser des adresses "temporaire" ou utilise un identifiant "stable" pour l'interface.

La construction de l'adresse temporaire se base le plus souvent sur une source aléatoire pour compléter le préfixe.

Pour l'adresse stable, la méthode recommandée est de faire un condensat − duquel on ne conserve que 64 bits − à partir de plusieurs informations :

- le préfixe
- le nom de l'interface
- un compteur de conflit (si on tombe sur un réseau qui a déjà l'adresse qu'on comptait prendre)
- un secret
- éventuellement un identifiant du réseau (par exemple pour du wifi, le SSID)

Afin de détecter d'éventuelles collisions, le client va simplement envoyer un ping à l'adresse choisit et voir si elle répond.

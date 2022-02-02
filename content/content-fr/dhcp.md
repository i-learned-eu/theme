Author: Ramle 
Date: 2021/12/04
Keywords: dhcp, ip, ipv4, ipv6, networking, réseau
Slug: dhcp
Summary: Pour pouvoir communiquer entre des machines d’un réseau IP il est requis de posséder une adresse IP dans le réseau, une méthode simple serait que chaque machine du réseau ait une adresse fixe configurée par l’utilisateur, mais cela serait vite fastidieux et un utilisateur ne connaissant pas à l’avance le réseau serait vite bloqué. Une solution est d’avoir un protocole permettant de distribuer automatiquement aux machines une adresse via un protocole fait pour.
Title: Comment fonctionne DHCP ?

Pour pouvoir communiquer entre des machines d’un réseau IP il est requis de posséder une adresse IP dans le réseau, une méthode simple serait que chaque machine du réseau ait une adresse fixe configurée par l’utilisateur, mais cela serait vite fastidieux et un utilisateur ne  connaissant pas à l’avance le réseau serait vite bloqué. Une solution est d’avoir un protocole permettant de distribuer automatiquement aux machines une adresse via un protocole fait pour. Nous avions déjà parlé dans un article précédent de [SLAAC](https://ilearned.eu/slaac.html), ici nous aborderons DHCP.

DHCP est majoritairement utilisé en IPv4, bien qu'il soit utilisable en IPv6. À la différence de SLAAC il est dit avec état, c'est-à-dire qu'un serveur central est requis pour attribuer et retenir l'IP de chaque appareil connecté au réseau.

Comme dit plus haut, ce n'est pas la machine qui choisit son IP, mais un serveur central. Le serveur peut attribuer de plusieurs manières, il peut soit, donner dynamiquement selon un pool réservé pour les hôtes (dans l'ordre logique, ou aléatoirement) ou bien en fonction de la machine qui demande. L'identification de la machine se fait généralement via l'adresse MAC. La plupart des serveurs DHCP retiennent les précédentes attribution pour redonner si possible la même adresse si une même machine demande. Les données envoyées via le serveur DHCP on une durée de bail (lease) avant que le client redemande les informations.

Le serveur DHCP peut distribuer d'autre configuration, sous forme d'"option", par exemple le résolveur DNS ou le nom de domaine utilisé pour le réseau local. Il existe vraiment beaucoup d'option officielle et non officielle exploitée.

Le client DHCP peut aussi envoyer différentes options au serveur, comme son nom d’hôte, ou bien des options personnalisées pour s'authentifier auprès du serveur DHCP.

Pour recevoir un bail DHCP le client va diffuser en "broadcast" (à tous les hôtes du réseau) sa requête, le serveur DHCP va donc recevoir aussi le paquet et lui répondre.

![Le client demande une IP, et le serveur lui en envoie une.](/static/img/dhcp/dhcp.webp)

Pour le renouvellement le processus change un peu, le client qui connait déjà le serveur lui demandera directement et n'enverra plus à tout le réseau.

Le processus de demande en IPv6 est sensiblement différent et ressemble dans la forme à SLAAC. Au lieu de passer par un broadcast la demande est envoyée en multicast à `ff02::1:2` qui identifie les serveurs ou relais (explication plus loin). Le serveur répondra su l'IP de lien local de la machine qui demande.

J'ai évoqué plus haut le concept de relai DHCP, c'est un moyen d'utiliser un serveur DHCP dans un seul réseau pour plusieurs réseaux. Comme on l'a vu plus haut le DHCP exploite des adresses qui ne fonctionnent que pour une machine dans le même réseau, mais comment employer un seul serveur DHCP pour plusieurs réseaux ? Avec un relai DHCP justement, le principe est d'en avoir un par réseau (sur un routeur par exemple, ça a l'avantage d'être plus léger et ne pas demander de stockage persistant contrairement à un serveur complet), il va récupérer les demandes DHCP envoyées en broadcast pour renvoyer à un serveur DHCP, pour permettre au serveur d'identifier il va exploiter l'IP de l'interface où est arrivé le paquet comme IP source.
Title: Comment fonctionne le relai privé d'Apple ?
Keywords: apple, sécurité, vpn, proxy
Summary: Dans cet article, nous allons parler du *relai privé* que propose Apple pour les personnes abonnées à iCloud+, cette fonctionnalité est arrivée avec IOS 15 et est souvent, à tort, confondue avec un VPN.
Slug: private_relay
Date: 2021-09-26
Author: Ownesis

Dans cet article, nous allons parler du *relai privé* que propose Apple pour les personnes abonnées à iCloud+, cette fonctionnalité est arrivée avec IOS 15 et est souvent, à tort, confondue avec un VPN.

### Relai privé 

Sur son [site officiel](https://www.apple.com/ios/ios-15/), Apple présente la fonctionnalité de relai privé avec ces mots:

> Le relai privé iCloud est un service qui permet de vous connecter à pratiquement n’importe quel réseau et de surfer avec Safari de façon encore plus sécurisée et confidentielle. Il veille à ce que les données envoyées par votre appareil soient toujours chiffrées et utilisent deux relais internet séparés. Ainsi, personne ne peut se servir de votre adresse IP, de votre position et de votre activité sur le Web pour établir votre profil détaillé.

*Il faut savoir, avant toutes choses que cette fonctionnalité de relai privé est en version bêta.*


Voyons maintenant comment ceci fonctionne (dans la théorie): 

Lorsque vous activez le relai privé, toute votre activité de navigation web ([http](https://ilearned.eu.org/http.html), https et [DNS](https://ilearned.eu.org/les-bases-du-dns.html)) dans **Safari** *(et une petite partie du trafic provenant des applications)* est relayée de façon chiffrée vers un relai géré par Apple.

A partir de la, vos requêtes DNS *(si vous savez pas ce que c'est je vous invite à lire [cet article](https://ilearned.eu.org/les-bases-du-dns.html))* et votre adresse IP sont séparés.

Apple conserve votre adresse IP MAIS votre requête DNS est transmise de façon chiffrée et anonyme (avec l'ip du serveur proxy d'Apple) chez un "partenaire de confiance" et c'est ce second relai qui va contacter le server web que vous voulez visiter.
Voici un [fichier `csv`](https://mask-api.icloud.com/egress-ip-ranges.csv) contenant la liste des plages d'adresses IP utilisées pour les relais de sortie.

Le premier relai qui connait votre adresse IP et donc votre emplacement approximatif, choisira le second relai le plus proche de vous (localisé dans votre région).
> Et pourquoi pas en Estonie comme dans Mr Robot ? ! 

Tout simplement pour permettre aux sites qui utilisent votre adresse IP de diffuser des informations locales comme la météo, les infos etc...

Du coup on se retrouve dans cette situation:

- Le premier relai (géré par Apple) connait votre adresse IP mais pas le contenu de vos requetes DNS.
- Le second relai (géré par un "partenaire de confiance") connait le contenu de vos requetes DNS mais ne connait pas votre adresse IP, seulement votre localisation encore plus approximative (votre région comme mentionné plus haut).
- Le serveur web que vous cherchez à contacter se retrouve dans la même situation que le second relai, il ne connait pas votre adresse IP mais seulement une zone géographique approximative.
   
Les trois parties ne peuvent donc pas créer un profil numérique basé sur votre adresse IP car ils n'ont que trop peu d'information pour faire cela.

### Quelques informations concernant les relais
- Le relai privé valide le fait que le client qui se connecte est bien un appareil Apple.
- Les relais s’appuient sur QUIC, un nouveau protocole de transport standard basé sur UDP  ([un de nos articles](https://ilearned.eu.org/http3.html) en parle). Toutes les connexions au relai privé ont lieu sur le port 443. 
- Le second relai utilise [DoH](https://ilearned.eu.org/dot-doh.html) (**D**NS **O**ver **H**TTPS).
- Le relai privé empêche les clients de pouvoir prétendre se trouver dans un autre pays (des sites internet comme Netflix restreignent l'accès à certains contenus par pays pour des raisons de droits d'auteur).
- Le premier relai est géré par Apple.
- Le second relai est géré par un partenaire de confiance choisi par Apple (ces partenaires incluent Cloudflare, Akamai et d'autres).

### Récapitulatif de l'échange et schéma
![schema_private_relay](/static/img/private_relay/private-relay.png)

**ATTENTION**
Le protocole est TRÈS peu documenté (pour le moment), à part le concept présenté dans les grandes lignes par Apple lors de leur [WWDC](https://developer.apple.com/videos/play/wwdc2021/10096/), le reste reste très flou donc pour une fois, nous allons devoir nous baser sur des spéculations.

Partons du principe que l'utilisateur souhaite accéder à `ilearned.eu.org`, il possède un iPhone et habite à Nice.

1. L'utilisateur ouvre Safari et cherche à contacter `ilearned.eu.org`.
2. Safari établie une connexion sécurisé avec QUIC vers le premier relai géré par Apple.
3. Le premier relai reçoit une connexion provenant de Nice, il vérifie si l'utilisateur utilise un appareil Apple et cherche un second relai géolocalisé en Côtes d'Azur et envoie l'identité de ce serveur au client.
4. Le client reçoit l'identité du second relai et commence à établir une connexion sécurisé (toujours avec QUIC) vers celui-ci MAIS à travers le premier relai, afin que le second ne puisse connaitre son adresse IP. *(Le protocolee utilisé est peut-etre SOCKS5, ou un protocolee créé spécialement par Apple.)* 
5. Le second relai reçoit une demande de connexion du premier relai (qui provient en réalité du client). Le client envoie sa requête DNS via le protocolee DoH - toujours à travers le premier relai - le paquet DNS est donc chiffré avec la clé publique du second relai, un échange de clés a eu lieu lors de la première connexion entre le second relai et le client. Le serveur déchiffre la requête, résout le nom de domaine `ilearned.eu.org` et initie la connexion avec celui ci.
6. Le serveur `ilearned.eu.org` reçoit une connexion provenant du second relai qui a une IP provenant de la Côte d'Azur.
7. Chaque requête du client et/ou serveur web, transitera désormais entre ces deux relais.

### Explications sur certains points
 - Dans l'étape **4**, le client établie une connexion avec le second relai mais en passant par le premier relai. Il demande au premier relai de relayer/transférer ce qu'il lui envoie vers le second relai, de cette manière, le second relai recoit un paquet provenant de l'adresse IP du premier relai et non du client (Cela ressemble beaucoup au protocolee SOCKS qui permet de faire ce genre de proxy de 'relais', un article sur ce protocolee sera bientôt disponible).
 - Dans l'étape **5**, le premier relai, ne faisant que relayer ce que le client envoie et reçoit, n'est pas en capacité de déchiffrer les paquets, il ne sert que de passerelle (voir l'article sur [TLS](https://ilearned.eu.org/tls.html) pour plus d'informations à ce sujet).
 
Du coup on se retrouve bien dans cette situation où :

 - Le premier relai connait l'adresse IP (et donc la localisation approximatif) du client mais ne sait pas ce qu'il demande au second relai, car le premier relai n'a pas connaissance de la clé de chiffrement utilisée par le client et le second relai, le premier relai n'a pas connaissance non plus du nom de domaine auquel veut se connecter le client.
 - Le second relai ne connait pas l'adresse IP du client car ce dernier utilise le premier relai pour relayer ses paquets. La localisation du client est donc inconnu pour le second relai.

### VPN or not VPN ?
Dans cette section je comparerais le relai privé aux VPNs commerciaux (NordVPN, ProtonVPN, etc) et non pas aux VPN plus "professionels".

Pour la faire courte, ce qui differencie les VPNs commerciaux et les VPNs dits "professionels" c'est que les VPNs commerciaux sont utilisés par le grand public et c'est surement à ceux-ci que les gens font référence en considèrant le relai privé porposé par Apple comme étant un VPN.

Un VPN commercial permet de changer d'adresse IP (et donc de localisation), pour contourner la censure, accéder à d'autres contenus sur les sites de streaming, sécuriser une connexion (généralement, les VPNs commerciaux chiffrent les données des client. Attention cependant, cet argument ne soit pas valable dans le cas d'une connexion HTTPS, ce qui est le cas de la majorité des connexions aujourd'hui), esquiver Hadopi ou se faire appeler Mr. Robot dans la cour de récréation. 

Tandis qu'un VPN professionel, permet d'accéder à un réseau privée (d'entreprise ou autres) ou de créer un réseau virtuel. (et oui, il y avait un indice dans le nom **V**irtual **P**rivate **N**etwork ;) ).

Bon, revenons à nos moutons, pourquoi le relai privé d'Apple n'est pas un VPN commercial ?

Comme vous avez pu le remarquer, le relai privé proposé par Apple est loin d'être un VPN commercial.
Le fonctionnement ressemble plus à un proxy HTTP et DNS qu'à un VPN.
Mis à part l'utilité et les protocolees utilisés, le relai privé peut s'apparenter à une partie du réseau Tor *(qui aura un article dédié bientôt)*, dans la mesure où le premier relai connait l'identité de l'utilisateur mais ne sait pas où il veut aller, et le second relai ne connait pas l'identité de l'utilisateur mais connait sa destination.
Pour les plus sceptiques, voici une liste des principales différences entre le relai privé d'Apple et un VPN commercial:

**Ce qui s'approche du fonctionnement d'un VPN commercial**

1. Votre adresse IP est changé.
2. Le trafic internet est chiffré entre le client et la destination.

**Ce qui ne s'approche pas du fonctionnement d'un VPN commercial**

1. Contrairement à un VPN, on ne peux pas choisir sa localisation, car on sera toujours localisé dans notre pays.
2. Un VPN "tunnélise" TOUT le trafic de votre périphérique, que ca soit le DNS, du web (http, https), du gemini, un ping (ICMP donc), bref, tout ce qui se trouve à partir de la couche `Réseau` du [modèle OSI](https://fr.wikipedia.org/wiki/Mod%C3%A8le_OSI) ou `Internet` du [modèle TCP/IP](https://fr.wikipedia.org/wiki/Mod%C3%A8le_OSI#Le_mod%C3%A8le_TCP/IP). Tandis que le relai privé d'Apple ne s'applique qu'à partir de la couche de `Transport` et seulement pour les protocoles HTTP(S) et DNS. Il ne fonctionne aussi que sur Safari, et dans de rares cas avec des applications.
3. Votre fournisseur VPN sait TOUT ce que vous faites et qui vous êtes, votre IP, donc votre localisation approximatif, quel site vous visitez et pire, si vous contactez un site qui ne propose pas TLS, le server VPN voit en clair ce que vous recevez/envoyez au site web.
4. Un VPN est généralement un même point d'entrée et de sortie. Alors que le relai d'Apple se distingue avec un point d'entrée et un point de sortie.

Alors, même si Apple utilise des "partenaires" de confiance pour nous faire comprendre que ce ne sont pas LEURS serveurs et qu'ils n'ont donc pas "d'accès" dessus, Apple est tout de même en capacité d'espionner notre trafic, tout simplement car même si le second relai n'est pas géré par eux directement, c'est leur logiciel qui y est installé, Apple est donc en capacité d'y implémenter une backdoor.
*(Sauf si ils utilisent SOCKSv5, QUIC se basant sur UDP, c'est tout à fait possible. De ce fait, les partenaires de confiance auraient juste à utiliser un serveur socks au lieu d'un logiciel propriétaire Made In Apple)*
Espérons juste que l'on aura plus de détail sur le fonctionnement de ce système et, pourquoi pas, un code OpenSource dans le futur !

Voilà :) ! J'espère que cet article vous a plu, et que vous avez compris comment fonctionne le relai privé proposé par Apple dans leur offre iCloud+.

Sources: [01net.com](https://www.01net.com/actualites/apple-private-relay-n-est-pas-un-vpn-mais-un-moyen-de-semer-ceux-qui-nous-espionnent-en-ligne-2044423.html) - [macworld.com](https://www.macworld.com/article/348965/icloud-plus-private-relay-safari-vpn-ip-address-encryption-privacy.html) - [Apple.com](https://developer.apple.com/support/prepare-your-network-for-icloud-private-relay)

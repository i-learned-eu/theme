Dans cet article, nous allons parler du *Relais privé* que propose  iCloud+ qui est arrivé avec IOS 15.

### Relais privé 
Beaucoup d'article ou de personne considère cette fonctionnalité comme un VPN, mais ce ne n'est pas dutout le cas, c'est plus embigüe.

*Il faut savoir avant toutes choses que cette fonctionnalité de relais privé est en version Bêta.*

Sur leur [site officiel](https://www.apple.com/ios/ios-15/), Apple présente leur relais privé avec ces mots:

> Le Relais privé iCloud est un service qui permet de vous connecter à pratiquement n’importe quel réseau et de surfer avec Safari de façon encore plus sécurisée et confidentielle. Il veille à ce que les données envoyées par votre appareil soient toujours chiffrées et utilisent deux relais internet séparés. Ainsi, personne ne peut se servir de votre adresse IP, de votre position et de votre activité sur le Web pour établir votre profil détaillé.

Voyons maintenant comment ceci fonctionne: 

Lorsque vous activez le relais privé, toute votre activité de naviguation web (http, https et DNS) dans **Safari** *(et une petite partie du traffic provenant des applications)* sont relayé de façon chiffrée vers un relais géré par Apple  ~~oh lala big brother~~.

A partir de la, Vos requête DNS *(si vous savez pas ce que c'est je vous invite à lire cet [article](https://ilearned.eu.org/les-bases-du-dns.html))*
et votre adresse IP sont séparé.

Apple conserve votre adresse IP MAIS votre requete DNS est transmise de façon chiffrée et anonyme (avec l'ip du server proxy d'Apple) chez un "partenaire de confiance" qui possède la clé de déchiffrement qui permet de déchiffrer la requête DNS (chiffré par le client au préalable), et c'est ce second relais qui va contacter le server web que vous voulez visiter.

Le premier relais qui connait votre adresse IP et donc votre emplacement, choisira le second relais le plus proche de vous (localisé dans votre région).
> Et pourquoi pas en Estonie comme dans Mr Robot ? ! 

Tout simplement pour permettre aux sites qui utilisent votre adresse IP de diffuser des informations locales comme la météo, les infos etc...

Ducoup on se retrouve dans cette situation:

- (Le premier relais) Apple connait donc votre adresse IP mais pas votre requete DNS.
- (Le second relais) Le "partenaire de confiance" connait votre requete DNS mais ne connait pas votre IP, seulement votre localisation TRÈS approximatif (votre région comme mentionné plus haut)
- (La destination) Le server web que vous cherchez à contacter se retrouve dans la même situation que le second relais, il ne connait pas votre adresse IP mais seulement une zone géographique approximative.
   
Les trois parties ne peuvent donc pas crééer un profile numérique sur vous car ils n'ont que trop peu d'information pour faire cela.

### Quelques informations concernant les relais
- Le Relais privé valide le fait que le client qui se connecte est un iPhone, un iPad ou un Mac, afin de garantir que les connexions viennent bien d’un appareil Apple.
- Le Relais privé iCloud s’appuie sur QUIC, un nouveau protocole de transport standard basé sur UDP  (un de nos [articles](https://ilearned.eu.org/http3.html) en parle). Les connexions QUIC dans le Relais privé sont configurées à l’aide du port 443 et de [TLS 1.3](https://ilearned.eu.org/tls.html). 
- Le Relais privé empêche les clients de pouvoir prétendre se trouver dans un autre pays.
- Le premier relais est géré par Apple
- Le deuxième relais est géré par un partenaire de confiance choisi par Apple. Apple ne les a pas nommé mais certain pense que les partenaires de confianece peuvent être: Akami, Cloudflare et Fastly. 

### Récapitulatif de l'échange et petit schéma
///// mettre shcema ////

Partons du principe que l'utilisateur souhaite accéder à `ilearned.eu.org`, il possède un iPhone et il habite à Nice.

1. L'utilisateur ouvre Safari et cherche à contacter `ilearned.eu.org`
2. Safari chiffre le nom de domaine/la requête DNS avec la clé public du second relais. L'utilisateur envoie les données chiffrés au premier relais géré par Apple.
3. Le premier relais reçoit une connexion provenant de Nice, il vérifie si l'utilisateur utilise un appareil Apple et il cherche donc un second relais geolocalisé en Cotes d'Azur et envoie les données chiffrées par l'utilisateur à ce second relais.
4. Le second relais reçoit les données chiffrées et les déchiffres avec sa clé privée. Il résout le nom de domaine `ilearned.eu.org` et commence la connexion avec celui ci.
5. Le server `ilearned.eu.org` recoit une connexion provenant du second relais qui a une IP provenant de la Côte d'Azur.
6. Chaque requêtes/réponses du client et/ou serveur web, transitera désormé entre ces deux relais.

### VPN or not VPN ?
Comme vous avez pu le remarquer, le relais privé proposé par Apple est loin d'être un VPN.
Le fonctionnement se rapproche beaucoup plus à un proxy qu'à un VPN.
Mise à part l'utilité et les protocoles utilisés, le relais privé peut s'apparenter à une partie du réseau Tor *(qui aura un article dédié bientôt)*, dans la mesure ou le premier relais connait l'identité de l'utilisateur mais ne connait pas ou il veut aller, et le second relais ne connait pas l'identité de l'utilisateur mais connait sa destination.
Mais pour les sceptiques voicis quelques différences entre le relais privé d'Apple et un VPN:

**Ce qui se rapproche au fonctionnement d'un VPN**

1. Votre ip est masqué, alors même si DE BASE un VPN n'est pas fait pour cacher une IP, la plus part des mortels connaissent le VPN comme un outil permettant de caché son IP et de nos jours c'est 90% de leurs utilisations.
2. Le traffique internet est chiffré entre le client et la destination.

**Ce qui ne s'approche pas au fontionnement d'un VPN**

1. Contrairement à un VPN, on ne peux pas choisir sa localisation, car on sera tjrs localisé dans notre pays.
2. On n'a pas accès à un réseau (c'est quand même le but 1er d'un VPN).
3. Un VPN "tunnélise" TOUT le traffique de votre périphérique, que sa soit le DNS, du web (http, https), du gemini, un ping ou tout ce qui se trouve à partir de la couche `Réseau` du modèle OSI ou `Internet` de la couche TCP/IP. (Tandis que le relais d'Apple ne s'applique qu'a partir de la couche de `Transport` et seulement pour le web, http(s) et DNS. Il ne fonctionne aussi que sur Safari, et quelque cas exceptionnel avec des applications).
4. Votre fournisseur VPN connait TOUT ce que vous faites et qui vous êtes, votre IP, donc votre localisation, quel site vous visitez et pire, si vous contactez un site qui ne propose pas TLS, le server VPN voit en clair ce que vous recevez/envoyez au site web.
5. Un VPN est généralement un même point d'entrée et de sortie. Alors que le relais d'Apple se distingue avec un point d'entrée et un point de sortie.

Voilà :) ! j'espère que cet article vous a plu, et que vous avez compris comment fonctionne (sur les grandes lignes) le relais privé proposé par Apple dans leur offre iCloud+ 

Source:
- [01net.com](https://www.01net.com/actualites/apple-private-relay-n-est-pas-un-vpn-mais-un-moyen-de-semer-ceux-qui-nous-espionnent-en-ligne-2044423.html)
- [macworld.com](https://www.macworld.com/article/348965/icloud-plus-private-relay-safari-vpn-ip-address-encryption-privacy.html)
- [Apple.com](https://developer.apple.com/fr/support/prepare-your-network-for-icloud-private-relay/)

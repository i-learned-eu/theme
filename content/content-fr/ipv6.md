title: IPv6, il est grand temps de migrer
Keywords: ipv6, ipv4, ip, migration, he, cogent
Date: 2021-05-07
author: Eban
summary: Décembre 1998, c’est la date de parution de la RFC 2460 introduisant IPv6, aujourd’hui, seulement 26% des sites les plus visités en France sont accessibles en IPv6 d’après l’Arcep. Faisons donc un petit tour d’horizon de l’adoption d’IPv6 en 2021.
Slug: ipv6

Décembre 1998, c’est la date de parution de la [RFC 2460](https://tools.ietf.org/html/rfc2460) introduisant IPv6, aujourd’hui, seulement 26% des sites les plus visités en France sont accessibles en IPv6 [d’après l’Arcep](https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/transition-ipv6/barometre-annuel-de-la-transition-vers-ipv6-en-france.html). Faisons donc un petit tour d’horizon de l’adoption d’IPv6.

IPv6 a été créé pour répondre à une problématique simple, le manque croissant d’IPv4.

![Taux d'adoption de l'IPv6 en France](/static/img/ipv6/adoption_ipv6.webp)

En effet, avec IPv4 la quantité d’IPs total est théoriquement de `4 294 967 296`, théoriquement car certains blocs d’IPs sont réservés à des usages privés comme par exemple 10.0.0.0/8. Le nombre de 4 milliards d’IPs peut sembler énorme, mais cela ne représente qu'une IP pour deux personnes sur terre, de plus beaucoups d'IPs sont allouées (plus d'informations sur l'allocation des IPs [ici](https://ilearned.eu/today-i-learned/allocation-ips.html) 😉) mais pas utilisées, comme par exemple Apple qui monopolise un /8 soit 16 777 216 IPs qui n’est presque pas utilisé ! Avec IPv6 le nombre total d’IPs théoriquement disponible est de `340 282 366 920 938 463 463 374 607 431 768 211 456`, IPv6 permet donc largement de pallier à ce problème de pénurie d’IPv4. Une adresse IPv6 typique ressemble à ça `2a03:7220:8083:3c00::1` elle est codée sur 128 bits. Vous vous demandez sûrement ce à quoi correspondent les `::` vers la fin de l’adresse, ils correspondent simplement à un remplissage avec des 0 afin d'atteindre le nombre de 128 bits. Par exemple : `2a03:7220:8083:3c00::1` correspond en réalité à `2a03:7220:8083:3c00:0000:0000:0000:0001`.  

Les opérateurs ont développé plusieurs techniques pour contrer à ce manque croissant d'IPv4, comme par exemple le CG-NAT, pour ceux qui ne le sauraient pas, le NAT c'est basiquement le fait de partager une seule IP publique entre plusieurs appareils (nous aborderons le NAT plus en détail plus tard ;)) le CG-NAT c'est donc du NAT mais à l'échelle d'une rue, d'un quartier. Le problème principal du NAT c'est qu'il empêche de nombreuses applications et protocoles de fonctionner, comme par exemple le Torrent ou même Google Maps ! Il empêche aussi d'héberger des services chez soi car seule une plage de ports est allouée au client, il faut donc avoir la chance de tomber sur la plage contenant les ports 80 et 443 pour pouvoir auto-héberger un site web par exemple.

La solution à ces maux est donc IPv6, mais comme nous l'avons vu en introduction son déploiement prend du temps, beaucoup de temps, dans son rapport annuel l'Arcep pointait du doigt la lenteur du déploiement d'IPv6, surtout chez certains opérateurs, mais aussi chez de nombreux hébergeurs qui ne fournissent pas d'IPv6 par défaut à leurs clients !

![Adoption de l'ipv6 par les opérateurs en france](/static/img/ipv6/adoption_fai.webp)

Un des raisons de la lenteur du déploiement d'IPv6 est le fait qu'utilisateurs et hébergeurs se renvoient systématiquement la balle, les uns se demandant à quoi bon avoir de l'IPv6 si tous les sites qu'ils visitent sont disponibles en IPv4, les autres disant qu'il est inutile de déployer IPv6 puisque les clients ne sont en majorité pas équipés. Cette attitude dilatoire a pour conséquence de ralentir le déploiement d'IPv6 au détriment des petits hébergeurs associatifs qui n'ont pas forcément les moyens d'acheter des ranges d'IPv4 souvent très couteuses. 

Il existe un autre frein, et pas des moindres, au déploiement et l'utilisation massive d'IPv6, le réseau IPv6 est actuellement divisé en deux, en effet, Cogent un très gros fournisseur de [transit](https://en.wikipedia.org/wiki/Internet_transit) refuse de peer (d'échanger ses routes) avec Hurrican Electric, un autre mastodonte du secteur. Ainsi, depuis le réseau IPv6 de Cogent il est impossible d'accéder à [he.net](http://he.net) (le site de Hurrican Electric) en IPv6. Ce bloquage dure depuis 2009, et malgré les nombreuses demandes de Hurrican Electric, ces deux entreprises ne parviennent pas à un accord financier.

![Gateau pour une réconciliation entre HE et Cogent](/static/img/ipv6/gateau_he.webp)

Nous finirons donc cet article sur ce joli gâteau, merci beaucoup de l'avoir lu, si vous souhaitez savoir si vous avez de l'IPv6 je vous invite à faire le test sur [test-ipv6.com](https://test-ipv6.com/). Si vous n'en avez pas renseignez-vous, il existe probablement une démarche pour obtenir de l'IPv6 de la part de votre opérateur 😉, sauf si vous êtes chez orange, pas du bol :'(, il existe cependant des personnes qui offrent des tunnels IPv6 comme [EnPLS](https://enpls.org/) par exemple.

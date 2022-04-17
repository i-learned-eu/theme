lang: fr
title: Fonctionnement du DNS over TLS et du DNS over HTTPS
Keywords: DoT, DNS, DoH, sécurité, TLS, HTTPS, DNS over HTTPS, DNS over TLS, vie privée, privacy
Date: 2021-04-30
author: Ramle
summary: Dans l'article d'aujourd'hui nous allons voir le fonctionnement de DNS Over TLS et de DNS over HTTPS.
Slug: dot-doh
Category: Réseau/DNS

Hier on évoquait le problème de l’authenticité des réponses d'un serveur DNS. Nous avons vu la solution : DNSSEC mais ce mécanisme ne fait que signer les requêtes pour empêcher une modification, il n'empêche pas un espionnage passif des requêtes. Le risque d'espionnage demande de sécuriser le canal, deux solutions ont été retenues : `DoT` et `DoH`.

DoT est l'acronyme de DNS  over TLS, ce protocole est assez "simple" si on omet l'explication de TLS qui sera vue prochainement, c'est du DNS qui passe par un canal chiffré via TLS. On utilise TCP sur le port 853.

Un soucis ce pose, TLS se base souvent, comme dans le monde du web avec HTTPS par exemple, sur des autorités de certification (abrégé CA) qui en théorie s'assure de délivrer des certificat qu'ils ont signés pour prouver la légitimité, mais en réalité ce système est assez peu fiable, il n'est en effet pas rare de voir une autorité délivrer par erreur ou même intentionnellement des certificats vérolés, qui n'aurait pas du sortir, de plus, historiquement un certificat coute assez chère, même si de nos jours certaines organisations comme [Let's Encrypt](https://letsencrypt.org/) délivre gratuitement un certificat TLS.

Pour se passer de CA plusieurs solutions existent, la plus simple est tout simplement de ne pas vérifier le certificat, cela protège d'un attaquant "passif" mais Il reste relativement aisé de remplacer le certificat à la volé. Pour empêcher ce cas on peut faire de l'épinglage de clé, ce principe se base sur un condensat du certificat qui est ensuite mit en base64, le logiciel peut ensuite comparer le certificat distant avec la clé qu'il a en local si un pirate effectue une attaque de l'homme du milieu (MITM) et remplace le certificat en court de route le client se rendra compte du subterfuge.

![SSL pining](/static/img/dns/ssl-pining.webp)

![SSL pining mauvais certificat](/static/img/dns/ssl-pining-fail.webp)

Un dernier problème dans DoT existe, un pare feu peut facilement en empêcher le fonctionnement, dans le cadre de portail captif par exemple souvent seul le trafic HTTP est autorisé. Une solution pour pallier à ce problème existe : DNS over HTTPS (DoH).

DoH permet comme DoT de chiffrer le canal de communication, mais en passant par HTTPS l'avantage est qu'il est difficilement bloquable, en effet bloquer HTTPS bloquerai par la même occasion un grands nombres de sites web. Le fonctionnement reste axé sur le principe d'HTTP, l'avantage d'HTTP est le contrôle du cache directement sur le client avec l'en-tête `Cache-Control: max-age=X` (ou X est le temps en seconde). Comme pour DoT plusieurs choix existe pour la validité du certificat, ce sont les mêmes choix qui s'offrent à nous. Pour ce qui est des codes de retour du DNS ils sont dans le corps du message, et non sous forme de code HTTP, bien sur les codes classiques HTTP sont toujours appliqués.

Ces deux méthodes peuvent poser soucis dans certains cadre, en effet, il est dans beaucoup de cas requis de passer par un programme qui "traduit" de DoH ou DoT vers le protocole DNS directement. Un exemple de logiciel est par exemple `stubby` sous Linux.

![Proxy DoH/DoT](/static/img/dns/proxy-dot-doh.webp)

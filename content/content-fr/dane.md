title: DANE et TLSA - Empêcher les certificats TLS frauduleux
Keywords: dane, tlsa, ca, fake ca
Date: 2021-05-01
author: Eban
summary: Aujourd'hui nous allons étudier le protocole DANE, ce protocole a été créé pour répondre à une problématique simple, comment garantir l'authenticité d'un certificat TLS ?
Slug: dane

Aujourd'hui nous allons étudier le protocole DANE, ce protocole a été créé pour répondre à une problématique simple, comment garantir l'authenticité d'un certificat TLS si le [CA](https://fr.wikipedia.org/wiki/Autorit%C3%A9_de_certification) est corrompu et délivre un certificat à, par exemple, un service de renseignement afin qu'il puisse intercepter et déchiffrer les requêtes des utilisateurs ? Cet exemple n'est pas pris par hasard, [un cas similaire](https://security.googleblog.com/2013/12/further-improving-digital-certificate.html) s'est produit en 2013 où l'ANSSI avait délivré des certificats pour des domaines de Google, probablement à des fins de renseignement. La [`RFC 6698`](https://tools.ietf.org/html/rfc6698) introduit donc le standard DANE (DNS Authentication of Named Entities) et le record DNS `TLSA`. Le principe est simple, ajouter un record dans la zone DNS qui contient un condensat du véritable certificat TLS, cette méthode ressemble très fortement au TLS Pinning, évoqué dans [l'article d'hier](https://ilearned.eu/dot-doh.html) mais a pour spécificité de placer le condensat au niveau du DNS.

Voici un exemple de record pour [ilearned.eu](https://ilearned.eu) :

```

_443._tcp.blog.eban.bzh. 10800	IN	TLSA	3 1 1 D7DF5F6E8325454CF25B711D7FCB22CD639C4F26514E5473EC73C59353C16F0D

```

On voit donc que l'on doit spécifier dans le record le port (ici, 443), le protocole utilisé (ici TCP, en passant, restez à l'affut dans les prochains jours un article à propos de ce protocole pourrait sortir 👀) puis le domaine auquel il s'applique, les trois numéros suivant `3 1 1` correspondent respectivement, à l'utilité du cadre d'utilisation de ce record, ici `DANE-EE: Domain Issued Certificate` un certificat donné pour un nom de domaine. Le `1` suivant indique le type de certificat hashé, `0` correspondant à un [certificat fullchain](https://en.wikipedia.org/wiki/Chain_of_trust) et `1` à la clé publique uniquement, le dernier `1` correspond enfin à la fonction de hashage utilisée, ici [SHA-256](https://en.wikipedia.org/wiki/SHA-2). Une fois ce certificat mis en place le navigateur devrait, en principe, comparer ce hash avec un hash qu'il génèrerait de son côté, en principe car DANE n'est présent dans [aucun navigateur grand publique](https://bugzilla.mozilla.org/show_bug.cgi?id=1479423). Il existe cependant le module [DNSSEC/DANE Validator](https://addons.mozilla.org/en-US/firefox/addon/dnssec-dane-validator) pour firefox et [TLSA Validator](https://chrome.google.com/webstore/detail/tlsa-validator/gmgeefghnadlmkpbjfamblomkoknhjga) pour chromium et dérivés. Pour résumer le fonctionnement de DANE, voici un petit schéma.

![/static/img/dane/Frame_21.webp](/static/img/dane/Frame_21.webp)

![/static/img/dane/Frame_22.webp](/static/img/dane/Frame_22.webp)

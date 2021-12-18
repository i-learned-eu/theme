Author: Eban
Date: 2021/12/16
Slug: ocsp
Summary: Nous connaissons tous le protocole TLS, les certificats de TLS se basent sur le bien connu protocole x509, avec la généralisation de l'utilisation de ce protocole sur Internet, un problème se pose : comment faire en sorte que tous les clients sachent quand un certificat est révoqué ? Afin de répondre à cette question, a été créé le protocole OCSP (Online Certificate Status Protocol).
Title: Comment fonctionne le protocole OCSP ?

Nous connaissons tous le protocole [TLS](https://ilearned.eu/tls.html), les certificats de TLS se basent sur le bien connu protocole [X.509](https://ilearned.eu/x509), avec la généralisation de l'utilisation de ce protocole sur Internet, un problème se pose : comment faire en sorte que tous les clients sachent quand un certificat est révoqué ? Afin de répondre à cette question, a été créé le protocole OCSP (Online Certificate Status Protocol).

Un client qui utilise OCSP (tous les navigateurs web récents) va interroger à chaque fois un serveur OCSP (appelé répondeur OCSP) en lui demandant le status dudit certificat (révoqué ou non).

Une requête OCSP ressemble à ça :

![Requête du client OCSP](/static/img/ocsp/ocsp_request.png)

- requestorName correspond au nom du client, ce champ est optionnel

Le client indique ensuite des informations qui permettent d'identifier le certificat

- L'algorithme de hashage utilisé pour hasher les deux champs suivants
- Le hash du nom de l'issuer (celui du certificat TLS de ce site est Let's Encrypt par exemple)
- Le hash de la clé publique de l'issuer
- Le numéro de série du certificat pour lequel on demande le certificat

Le serveur répond ensuite avec une réponse au format suivant :

![Réponse du server OCSP](/static/img/ocsp/ocsp_response.png)

- responderID correspond à l'identifiant du serveur qui nous a répondu
- producedAt correspond à l'heure à laquelle la vérification a été faite
- certID contient les mêmes valeurs que celles données lors de la requête initiale
- certStatus peut être trois valeurs
    - good : le certificat est valide
    - revoked : le certificat est révoqué
    - unknown : le status du certificat est inconnu
- thisUpdate l'heure la plus récente où le certificat a été reconnu comme valide par le responder.

Le protocole OCSP est très simple dans son fonctionnement et son concept, mais il est une brique essentielle de la sécurité des certificats TLS que nous utilisons quotidiennement. Il comporte néanmoins un problème majeur, le respect de la vie privée. En effet, le répondeur OSCP pourrait facilement connaître l'ensemble des sites que visite une IP. Pour pallier à cela il existe une technique appelée OCSP Stapling qui permet au serveur web d'envoyer directement la réponse OCSP au client. Ainsi, seul le client et le serveur web sont impliqués dans cet échange.
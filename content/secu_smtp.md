lang: fr
Author: Eban
Date: 2021/12/06
Keywords: mail, sécurité
Slug: secu_smtp
Summary: Dans un précédent article nous avions abordé le fonctionnement de SMTP, aujourd'hui nous verrons les différents moyens de sécuriser ce protocole.
Title: Faire rimer SMTP et sécurité
Category: Réseau/Mail

Dans [un précédent article](https://ilearned.eu/smtp.html) nous avions abordé le fonctionnement de SMTP, aujourd'hui nous verrons les différents moyens de sécuriser ce protocole.

# STARTTLS

STARTTLS est une "extension" de SMTP qui permet de communiquer de façon chiffrée avec les serveur SMTP en utilisant TLS. Elle est définie dans la [RFC 320](https://datatracker.ietf.org/doc/html/rfc3207). Avec STARTTLS, l'utilisation de TLS n'est pas rendue obligatoire, elle est simplement possible pour les clients/serveurs qui le supportent. De cette non-obligation découle une problématique, étant donné que l'échange initial (le EHLO) qui indique les extensions supportées est envoyé en clair, il est trivial pour un attaquant de modifier les paquets d'initialisation de la connexion pour désactiver STARTTLS. Cette extension, standardisée en 2002, apporte donc une certaine avancée, mais n'est pas suffisant.

## MTA-STS (SMTP MTA Strict Transport Security)

MTA-STS est une mécanisme standardisé en 2018 qui permet à un serveur de spécifier à l'avance s'il supporte l'utilisation de TLS en plaçant un record TXT dans la zone du MTA ([Mail Transfer Agent](https://ilearned.eu/smtp.html)).

```jsx
_mta-sts.example.com.  IN TXT "v=STSv1; id=20160831085700Z;"
```

Dans cet exemple v correspond à la version de MTA-STS utilisée, et id à l'ID de la policy.

La policy, c'est un fichier placé à l'URI `[https://mta-sts.example.com/.well-known/mta-sts.txt](https://mta-sts.example.com/.well-known/mta-sts.txt)` qui spécifie

- La version de MTA-STS utilisée
- Le "mode" qui spécifie comment un MTA où la validation de la policy échouerait devrait réagir, trois valeurs sont possibles :
    - enforce : le message ne doit pas être délivré si la validation échoue.
    - testing : le message doit être délivré mais cet échec doit être signalé en utilisant le protocole `TLSRPT`.
    - none : le message doit être délivré comme si aucun échec n'avait eu lieu.
- `mx` spécifie les [mx](https://ilearned.eu/smtp.html) qui peuvent être utilisés
- `max_age` correspond au temps maximal (en secondes) que doit être conservé en cache cette policy.

```jsx
version: STSv1
mode: enforce
mx: mail.example.com
mx: *.example.net
mx: backupmx.example.com
max_age: 604800
```

STARTTLS couplé à MTA-STS permettent donc de garantir un niveau de confidentialité satisfaisant entre les serveurs SMTP.

# SMTP-AUTH

Nous avons vu comment sécuriser la communication entre les différents acteurs d'un envoi de mail avec SMTP, mais pas comment authentifier l'utilisateur auprès du serveur, pour cela a été créé l'extension SMTP-AUTH.

```c
S: 220 smtp.example.com ESMTP Server
C: EHLO client.example.com
S: 250-smtp.example.com Hello client.example.com
S: 250-AUTH GSSAPI DIGEST-MD5
S: 250-ENHANCEDSTATUSCODES
S: 250 STARTTLS
C: STARTTLS
S: 220 Ready to start TLS
    ... TLS negotiation proceeds.
     Further commands protected by TLS layer ...
C: EHLO client.example.com
S: 250-smtp.example.com Hello client.example.com
S: 250 AUTH GSSAPI DIGEST-MD5 PLAIN
C: AUTH PLAIN dGVzdAB0ZXN0ADEyMzQ=
S: 235 2.7.0 Authentication successful
```

Dans cet exemple, de l'authentification en "Plaintext" est utilisé, ce qui signifie que le mot de passe est envoyé tel quel simplement encodé en base64. Une fois de plus on peut remarquer la simplicité du protocole SMTP.

Cette extension permet donc d'authentifier les clients, mais aucunement de garantir une protection contre l'usurpation d'adresse mail. C'est un sujet plutôt complexe et qui n'est pas directement lié à SMTP que nous aborderons dans les prochains jours !

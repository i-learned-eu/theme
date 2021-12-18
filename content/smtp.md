Author: Eban
Date: 2021/12/03
Keywords: mail, réseau
Slug: smtp
Summary: Nous utilisons les mails quotidiennement, mais savons nous seulement comment fonctionnent les protocoles qui sous-tendent ce service ? Aujourd'hui nous aborderons le protocole SMTP.
Title: Comment fonctionne SMTP ?

Nous utilisons les mails quotidiennement, mais savons-nous seulement comment fonctionnent les protocoles qui sous-tendent ce service ? Vous trouverez dans ce calendrier de l'Avent de décembre un ensemble d'articles répondants à cette question. Aujourd'hui nous aborderons le protocole SMTP.

SMTP (Simple Mail Transfer Protocol) est un très ancien protocole qui a été standardisé pour la première fois en 1981, soit un an avant que le minitel soit présenté au grand publique en France ! De par son ancienneté, il hérite aussi d'une certaine simplicité. La communication avec SMTP s'organise autour de cinq acteurs majeurs : 

- Le client mail (MUA pour mail user agent) c'est lui qui envoie le mail
- L'agent de dépôt (MSA pour mail submission agent) il est chargé de recevoir les mails à envoyer.
- L'agent de transfert (MTA pour mail transfert agent) il est chargé de faire en sorte de trouver la route à utiliser pour acheminer correctement les mails.
- L'échangeur de mail (MX pour mail exanger) c'est un serveur exposé sur internet, il est chargé de recevoir les mails de l'agent de transfert et de transférer les mails à l'agent de distribution.
- L'agent de distribution (MDA pour mail delivery agent) il est chargé de stocker les mails pour ensuite les distribuer au destinataire.

Les agents de dépôt (MSA) et de transfert (MTA) sont, notamment dans les petites infrastructures, regroupés sur une seule machine, mais sur de plus grosses infrastructures ils peuvent être séparés notamment pour assurer une plus grande disponibilité du service.

Afin de trouver à quel échangeur de mail s'adresser, le MTA (agent de transfert) exploite le [DNS](https://ilearned.eu/les-bases-du-dns.html) et cherche un enregistrement MX dans la zone du nom de domaine de destination.

![Boot mbr.png](/static/img/smtp/Boot_mbr.png)

Plus concrètement, un exemple simple d'envoi de mail a lieu comme suit :

![SMTP_exchange.png](/static/img/smtp/SMTP_exchange.png)

1. Dans un premier temps, le client envoie un message de "présentation", EHLO, dans lequel il indique son hostname. Vous avez peut-être déjà vu HELO au lieu de EHLO, HELO est en fait une commande dépréciée par la RFC 5321 depuis 2008 ! L'usage de EHLO est donc préféré.
2. Puis, le client envoie l'adresse depuis laquelle il souhaite envoyer le mail.
3. Ensuite, il envoie l'adresse du destinataire, cette dernière sera ensuite utilisée par le MTA afin de savoir comment envoyer le mail.
4. Le client envoie le contenu du mail
5. On ferme la connexion

Comme on a pu le voir, SMTP est un protocole plutôt simple dans son fonctionnement, néanmoins, cette simplicité n'est pas sans conséquence, elle implique un manque certain de sécurité. Afin de pallier à ces problèmes, un certain nombre de solutions ont été mises en place, nous les aborderons dans un prochain article.

Author: Eban
Date: 2021/12/01
Slug: about
Title: À Propos d'I Learned
Summary: Le premier article d'I Learned est sortit le 24 Avril 2021, d'un projet d'initialement deux personnes, il réunit maintenant huit contributeurs et quelques 33 000 vues cumulées. Depuis, l'infrastructure a quelques peu évolué et est devenue (presque) propre. Dans ce court article nous ferrons le tour du fonctionnement et de l'organisation d'I Learned.

Le premier article d'I Learned est sortit le 24 Avril 2021, d'un projet d'initialement deux personnes, il réunit maintenant 8 contributeurs et quelques 33 000 vues cumulées. Depuis, l'infrastructure a quelques peu évolué et est devenue (presque) propre. Dans ce court article nous ferrons le tour du fonctionnement et de l'organisation d'I Learned.

# Infrastructure

## DNS

I Learned s'appuie sur trois serveur dns autoritaires `ns1.eban.eu.org`, `ns.ramle.be`, `ns2.bb0.nl` ainsi que [`ns1.immae.eu`](http://ns1.immae.eu/) pour garantir la redondance côté DNS.

## Web

Le site est hébergé sur une VM chez [tetaneutral](http://tetaneutral.net). 

## Automatisation

Tout le code source d'I Learned est disponible sur notre [git](https://git.ilearned.eu.org), et l'automatisation est gérée avec Drone CI. 

Drone CI nous permet entre autre de vérifier que les métadonnées des articles sont bien remplies, mais aussi de build automatiquement le site à chaque nouveau push dans la branche master `master` avec pelican.

Le git d'I Learned ainsi que la CI sont hébergés chez [Ramle](https://ilearned.eu/authors.html).

## Mail

Les mails d'I Learned sont gracieusement hébergés par [Outout](https://ilearned.eu/authors.html) chez bakker-it.

# Organisation interne

I Learned a une organisation volontairement non-hiérarchique, tous les contributeurs réguliers on un droit de "vote" sur les changements de l'organisation d'I Learned.

## Publication d'un nouvel article

Pour publier un nouvel article sur I Learned, il suffit d'être relu et approuvé par deux autres collaborateurs !

## Licence

Tous les articles publiés sur I Learned sont distribués sous la licence CC-BY-NC-SA et le code sous licence AGPL 3.0.

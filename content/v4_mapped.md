Author: Eban 
Date: 2021/08/03
Keywords: réseau, sécurité
Slug: v4_mapped
Summary: Il y a maintenant une vingtaine d'années avait été mis en place sur certaines machines un système permettant d'avoir des adresse IPv6 mappant une adresse IPv4. Ce principe peut sembler une bonne idée, mais il représente en réalité une vulnérabilité importante.
Title: Le danger des IPv4 mappées en IPv6

Il y a maintenant une vingtaine d'années avait été mis en place sur certaines machines un système permettant d'avoir des adresse IPv6 mappant une adresse IPv4, le but était de n'avoir qu'un [socket](https://fr.wikipedia.org/wiki/Berkeley_sockets) (qui est basiquement un intermédiaire entre les interfaces réseau physiques et les logiciels accédant au réseau) écoutant seulement en IPv6 mais acceptant les IPv4 mappées. Ces adresses IPv6 ont pour 80 premiers bits des zéros, les 16 suivants sont des `f`, et les 32 derniers bits représentent une adresse IPv4. `:ffff:0a00:0001` est l'adresse IPv6 correspondant à l'adresse `10.0.0.1`, on peut aussi l'écrire sous la forme `::ffff:10.0.0.1`. Si vous souhaitez calculer une adresse IPv4 mappée, vous pouvez utiliser [ce](http://www.gestioip.net/cgi-bin/subnet_calculator.cgi) site, nous utiliserons l'écriture `::ffff:10.0.0.1` pour le reste de cet article.

Ce mode de fonctionnement peut paraître un bon moyen de transitionner vers un déploiement massif d'IPv6, mais les adresses IPv4 mappées représentent une réelle menace, en effet, quand un programme reçoit une adresse IPv4 il n'a aucun moyen de savoir si cette adresse IP était mappée sur une IPv6 ou si c'est une *véritable* adresse IPv4, donc si un attaquant envoie une requête avec une adresse IPv6 `::ffff:127.0.0.1` par exemple, cela pourrait être interprété comme l'adresse IPv4 de loopback `127.0.0.1` et donc permettre à l'attaquant d'accéder à certains logiciels qui donneraient certaines permissions dans leur ACL à l'adresse IP `127.0.0.1`.

![Schéma décrivant une attaque type utilisant une adresse IPv4 mappée](/static/img/v4_mapped/Mapped_v4(2).png)

[Le document](https://datatracker.ietf.org/doc/html/draft-itojun-v6ops-v4mapped-harmful) qui détaille ces problèmes de sécurité recommande simplement d'interdire les adresses IPv4 mappées, mais ce n'est malheureusement pas encore le cas, de nombreux systèmes récents, à l'exception de NetBSD, OpenBSD et FreeBSD.

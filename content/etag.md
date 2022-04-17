lang: fr
title: Comment fonctionne le tracking par ETag
Keywords: etag, tracking, rgpd, cookie, no cookie
Date: 2021-05-09
author: Eban
summary: De plus en plus de navigateurs mettent en place des mesures pour bloquer le tracking, Firefox par exemple, bloque par défaut les cookies third party. Pour contourner ces mesures de protection des utilisateurs, les entreprises de tracking sont à la recherche d'autres moyens de pister les utilisateurs, ETag est l'un d'eux.
Slug: etag
Category: Sysadmin

De plus en plus de navigateurs mettent en place des mesures pour bloquer le tracking, Firefox par exemple, [bloque](https://blog.mozilla.org/blog/2019/09/03/todays-firefox-blocks-third-party-tracking-cookies-and-cryptomining-by-default/) par défaut les cookies third party. Pour contourner ces mesures de protection des utilisateurs, les entreprises de tracking sont à la recherche d'autres moyens de pister les utilisateurs, ETag est l'un d'eux. Nous en avons brièvement parlé dans l'article sur [HTTP](https://ilearned.eu/http.html), l'en-tête ETag est dans le cas du serveur web [Nginx](https://www.nginx.com/) que nous prendrons comme exemple ici, un condensat de la date de modification et de la longueur (lenght) du fichier demandé. Ce hash a été créé pour permettre au navigateur de savoir s'il y a eu des changements sur un fichier et s'il doit montrer la version du fichier conservée en cache à l'utilisateur ou télécharger à nouveau le fichier depuis le serveur.

![Schéma décrivant le fonctionnement de base des ETags](/static/img/etag/etag_fonctionnement_base.webp)

![Schéma décrivant le fonctionnement des ETags, lorsque ceux du client et du serveur ne correspondent pas](/static/img/etag/etag_not_same.webp)

Ce système d'ETag peut cependant être détourné, afin de vérifier si les ETag correspondent, le client envoie l'ETag de la version qu'il a du fichier au serveur, le serveur peut donc, pour chaque utilisateur, servir un fichier différent (qui aura donc un ETag différent) et grâce à cet ETag savoir quel utilisateur a consulté quelle page à quelle moment. Des entreprises comme [Hulu ou Spotify](https://www.extremetech.com/internet/91966-aol-spotify-gigaom-etsy-kissmetrics-sued-over-undeletable-tracking-cookies) ont été épinglées pour avoir mis en place cette pratique, qui ne respecte évidemment pas le RGPD.

![Schéma décrivant le fonctionnement du tracking via ETag](/static/img/etag/etag_based_tracking.webp)

Merci d'avoir lu cet article, en espérant qu'il a été clair :) On se retrouve demain pour parler de décentralisation !

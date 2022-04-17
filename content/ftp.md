lang: fr
Author: Ramle
Date: 2021/12/23
Keywords: réseau
Slug: ftp
Summary: Dans cet article nous découvrirons le fonctionnement du protocole FTP !
Title: Comment fonctionne le protocole FTP ?
Category: Sysadmin

Pour transférer des fichiers sur internet avant HTTP il existait un protocole qui se voulait assez simple : FTP (file transfer protocol).

FTP se base sur TCP, par défaut le serveur écoute le port 21. Le client FTP qui va se connecter au serveur envoie une commande FTP au serveur. Par exemple pour récupérer un fichier sur le serveur :

`RETR example.txt`

Pour transférer les données FTP utilise un second canal. Il a 2 modes de connexions pour ce canal, actif et passif.

En mode actif le client écoute sur un port précis, contacte le serveur FTP en lui disant de répondre sur le port et le serveur FTP initialise une connexion de données sur ce port.

Le souci avec ce mode de fonctionnement est qu’il ne fonctionne pas avec du NAT ou un pare-feu restrictif sur les connexions entrantes.

![Les données envoyées par le serveur sont bloquées par le Firewall en mode passif](/static/img/ftp/passif.webp)

Un autre mode pour palier à ces soucis existe, le mode passif. Pour ce mode-là le client envoie la commande `PASV`, le serveur envoie alors en retour une IP et un numéro de port que le client utiliseras pour répondre.
ss
![Les données ne sont pas bloquées par le firewall en mode actif](/static/img/ftp/actif.webp)

FTP demande par défaut une authentification, une parade utilisée pour permettre un accès au fichier par n’importe qui est le FTP anonyme. Le principe est d’utiliser l’utilisateur `anonymous` sans mot de passe pour accéder aux ressources.

Le protocole FTP souffre de nombreux problèmes de sécurités et est en voie de disparition. Par exemple de base FTP n’a aucun chiffrement, il y a cependant FTPS qui a vu son apparition, c’est simplement FTP au-dessus de TLS.

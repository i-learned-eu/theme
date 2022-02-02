Author: Ramle 
Date: 2021/07/20
Keywords: sécurité
Slug: mac
Summary: Un reproche souvent fait à Linux est sa gestion des droits souvent trop permissive, pour remédier à cela on été créés les MAC
Title: Sécuriser votre système d'exploitation grâce aux MAC

Un reproche souvent fait à Linux est sa gestion des droits souvent trop permissive. Il y a bien sûr une raison historique, à la naissance des différents systèmes d'exploitation que l'on connait aujourd'hui la sécurité n'était pas la préoccupation principale. Le but de base n'était pas non plus de compliquer la tâche des utilisateurs (la sécurité se fait toujours au prix de complexité supplémentaire). Le problème de cette philosophie de départ est qu'il faut repenser la sécurité avec une base trop ouverte.

Sous Linux tout est fichier, les périphériques physiques ont par exemple, un fichier attribué dans `/dev`. La sécurité d'accès pour les fichiers se base sur les permission de chaque fichier. Ce mécanisme montre vite des limites. Les autorisations sont très limitées, sous Linux ces autorisations sont divisées en 3, ce que l'utilisateur propriétaire peut faire, ce que le groupe propriétaire peut faire et ce que tout le monde est autorisé à faire. Chaque partie peut avoir 3 droits différents :

- R (read) : Lecture
- W (write) : Écriture
- X (Execute) : Exécution (dans le cadre d'un dossier c'est l'autorisation pour lister le contenu)

On peut visualiser les permissions via la commande `ls -l <dossier>` :

```jsx
% ls -l
total 0
-rwxr-xr-x 1 ramle ramle 0 Jul 19 17:05 executable
-rw------- 1 root  root  0 Jul 19 17:05 root_only
```

`ls` divise en 3 parties les permissions, celle de l'utilisateur, du groupe et de tout le monde :

![Détails des droits affichés par LS](/static/img/mac/ls(2).webp)

Le soucis de se baser uniquement sur les permissions des fichiers est le manque de contrôle, le schéma de sécurité des MAC permet de renforcer le tout en regardant beaucoup plus de facteur. Le concept est de regarder toutes le actions faites sur la machine, et de regarder l'action et l'autoriser ou non en fonction des règles d'accès. L'avantage de ce modèle par rapport à la sécurité historique de Linux (et UNIX par la même occasion) est d'être bien plus précis, par exemple autoriser à une application seulement certains ports et fichiers (fichier qui pourrait selon le système de fichier lui être autorisé).

Sous Linux, il n'y a pas de base de framework de MAC, mais des modules dans le noyaux sont prévu pour qu'on y greffe un framework il y en a deux importants, Apparmor et SELinux.

Les deux ont des fonctionnalités similaires, mais se différencient par un point important, Apparmor se base sur le chemin complet d'un fichier, là ou SELinux se base seulement sur le nom, cette différence est assez minime dans la plupart des cas, mais en fonction du framework utilisé, des méthodes de contournement se basant sur ces spécificités, par exemple en utilisant des liens virtuels (symlink) ou renommant un fichier, une bonne politique d'accès évite cependant les contournements.

Bien sûr, Linux n'est pas le seul système d'exploitation qui utilise des contrôles d'accès plus poussé qu'uniquement des permissions basiques, Windows fonctionne sur [ce principe](https://ilearned.eu.org/secu_windows.html) aussi tout comme MacOS et BSD avec l'intégration de TrustedBSD.

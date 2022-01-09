Author: Ramle 
Date: 2021/12/21
Slug: wayland
Title: Comment fonctionne Wayland ?
Summary: Cet article détaille le fonctionnement de Wayland, un système de fenetrage alternatif à X11
Keywords: Linux

L’affichage graphique d’un système d’exploitation est très complexe, si l’on veut avoir plusieurs fenêtre et application affichée en même temps en harmonie un logiciel qui gère les différents périphériques d’entrées et de sorties, l’isolation de chacun d’elle pour éviter qu’une application puisse récupérer les données d’une autre. Le but de cet article est d’essayer de comprendre le protocole Wayland qui vise à remplacer le vieillissant X11.

En résumer, Wayland (comme X11) sert à rajouter une couche d’abstraction pour les applications pour ne plus avoir à tout réinventer systématiquement.

Son mode de fonctionnement est client serveur. Le compositeur contrôle KMS et Evdev.

Evdev c’est la gestion des périphériques d’entrée sous Linux. Chaque périphérique se voit attribué dans /dev/input des fichiers qui permettent de recevoir les événements. Wayland utilise libinput (qui lui accède à evdev via libevdev) pour recevoir les entrées, la détection des nouveaux périphérique utilise udev. Le compositeur se charge d’envoyer au client les entrées. Une grosse avancée en sécurité par rapport à X11 est que les entrées ne sont pas envoyées à touts les clients, mais seulement celui concerné.

Pour la sortie vidéo chaque application envoie directement un buffer vidéo, un buffer c'est ce qui reçu par le gpu pour concevoir l’image le compositeur n’a plus qu’à assembler les différents buffers pour composer l’image finale,  au compositeur, le compositeur s’occupe de gérer les fenêtres et de composer l’image complète avant de la renvoyer à KMS. KMS est le module kernel qui s’occupe de gérer l’affichage.

![Schéma de l'architecture de Wayland](/static/img/wayland/1.png)

(source : [https://wayland.freedesktop.org/architecture.html](https://wayland.freedesktop.org/architecture.html))

Le souci qui peut se poser est la rétrocompatibilité avec les applications X11, pour résoudre ce souci xwayland existe, c’est une couche de compatibilité. Xwayland s’occupe de faire un serveur X minimaliste pour les applications.


![Xwayland est un intermédiaire entre les applications utilisant X11 et Wayland](/static/img/wayland/2.png)

(source : [https://wayland.freedesktop.org/docs/html/ch05.html](https://wayland.freedesktop.org/docs/html/ch05.html))

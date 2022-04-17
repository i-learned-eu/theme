lang: fr
Author: Eban
Date: 2021/09/05
Keywords: linux, sandboxing, systemd, sécurité
Slug: systemd-sandboxing
Summary: Si vous être un utilisateur de Linux, vous connaissez sûrement systemd, systemd est ce que l'on appelle un init, c'est le premier logiciel lancé par le système d'exploitation et il est chargé de démarrer tous les autres. Pour être démarré par systemd un logiciel doit être reconnu comme un service par systemd. Un service c'est un fichier qui détaille les informations à propos des logiciels à lancer, comment les lancer, les arrêter, leur nom, quels sont leurs dépendances et plus encore. systemd propose des fonctionnalités de sécurité plutôt avancées et très utiles pour sécuriser son système. C'est ces fonctionnalités que nous détaillerons dans cet article.
Title: Comment sécuriser ses services systemd ?
Category: Cybersécurité/Blue Team

Si vous être un utilisateur de Linux, vous connaissez sûrement `systemd`, systemd est ce que l'on appelle un init, c'est le premier logiciel lancé par le système d'exploitation et il est chargé de démarrer tous les autres. Pour être démarré par `systemd` un logiciel doit être reconnu comme un `service`. Un service c'est un fichier qui détaille les informations à propos des logiciels à lancer, comment les lancer, les arrêter, leur nom, quels sont leurs dépendances et plus encore. `systemd` propose des fonctionnalités de sécurité plutôt avancées et très utiles pour sécuriser son système. C'est ces fonctionnalités que nous détaillerons dans cet article.

Dans cet article, nous sécuriserons le service systemd de unbound, un serveur DNS résolveur. Pour inspecter la sécurité d'un service systemd, on peut utiliser la commande `systemd-analyze security example.service`, essayons donc avec le service systemd de unbound :

```diff
user@vm01:~$ systemd-analyze security unbound.service
→ Overall exposure level for unbound.service: 9.5 UNSAFE 😨
```

9.5/10 en score d'exposition, y'a du boulot 😅. Jetons un oeil au service systemd de Unbound.

```diff
[Unit]
Description=Unbound DNS server # Description du service
Documentation=man:unbound(8) # Lien vers la documentation
After=network.target # Dépendance, le service ne démmarera que si l'ordinateur est connecté au réseau
Before=nss-lookup.target # Doit être ancé avant que les logiciels utilisant DNS le soient
Wants=nss-lookup.target # Lance les logiciels utilisant DNS une fois que le service unbound est lancé

[Service]
Type=notify
Restart=on-failure # Redémarre le service s'il rencontre une erreur
EnvironmentFile=-/etc/default/unbound # Fichier d'environnement Bash
ExecStartPre=-/usr/lib/unbound/package-helper chroot_setup # Commande à exécuter avant de lancer unbound
ExecStartPre=-/usr/lib/unbound/package-helper root_trust_anchor_update # Commande à exécuter avant de lancer unbound
ExecStart=/usr/sbin/unbound -d $DAEMON_OPTS # Commande à exécuter pour lancer unbound
ExecReload=/usr/sbin/unbound-control reload # Commande à exécuter pour recharger la configuration d'unbound
PIDFile=/run/unbound.pid # Emplacement du PID

[Install]
WantedBy=multi-user.target
```

On a ici un service systemd tout ce qu'il y a de plus classique, si vous n'avez pas l'habitude d'utiliser systemd, toutes les directives présentes dans ce fichier sont commentées.

Afin d'améliorer la sécurité de ce service systemd, voici la liste des différentes directives que nous pouvons ajouter

- `AmbientCapabilities` permet de donner des capacités au processus lors de son lancement. Les capacités permettent de donner des permissions à certains processus de façon plus précise que le système de permissions plus classique de Linux. Elles permettent par exemple de donner le droit à un processus d'allouer des port en dessous de 1024 sans droits root.
- `CapabilityBoundingSet` permet de limiter les capacités qui peuvent être données au processus. C'est une liste des capacités qui peuvent être données au processus.
- `Group` et `User` permettent de spécifier quel utilisateur et quel groupe lance le logiciel, c'est une directive quasi indispensable pour sécuriser un service systemd.
- `LockPersonality` empêche le processus de changer de domaine d'exécution. Red Hat définit très bien ce que sont les domaines d’exécution : pensez aux domaines d'exécution comme à la "personnalité" d'un système d'exploitation. Étant donné que d'autres formats binaires, tels que Solaris, UnixWare et FreeBSD, peuvent être utilisés avec Linux, les développeurs peuvent changer la façon dont le système d'exploitation traite les appels système (syscall) provenant de ces binaires en modifiant la "personnalité" de la tâche.
- `NoNewPrivileges` empêche le processus d'obtenir de nouveaux privilèges, cela permet d'éviter qu'un attaquant puisse utiliser ce processus pour gagner des privilèges supplémentaires.
- `PrivateDevices` crée un dossier /dev spécifique à ce service lui donnant accès aux pseudo-device (/dev/null, /dev/random etc.) mais pas aux device physiques (/dev/sdaX, /dev/sdbX etc.).
- `PrivateTmp` crée un dossier /tmp spécifique à ce service.
- `ProtectClock` empêche le service de modifier l'horloge du système.
- `ProtectControlGroups` empêche le service de modifier/ajouter des [cgroup](https://man7.org/linux/man-pages/man7/cgroups.7.html).
- `ProtectHome` rend les répertoires `/home/, /root, et /run/user` inaccessibles et vides aux yeux du processus.
- `ProtectKernelLogs` empêche le processus de lire les logs du kernel.
- `ProtectKernelModules` empêche le processus de charger des modules kernel.
- `ProtectKernelTunables` empêche le processus d'écrire dans les variables kernel (souvent dans /sys).
- `ProtectSystem` monte les répertoires /usr, /boot et /efi en lecture seul.
- `ReadWriteDirectories` définit les répertoires accessibles en écriture et en lecture aux processus exécutés.
- `RestrictAddressFamilies` définit les type d'adresse (adresses IPs, de socket unix etc.) que le processus peut utiliser
- `RestrictNamespaces` empêche le processus d'accéder à n'importe quel namespace. Un namespace, sous linux, est une sorte de conteneur (même si le terme n'est pas exact) qui permet d'isoler, en partie, des processus du reste du système, cette directive empêche donc les processus du service d'accéder à d'autres namespaces que le sien. Pour en savoir plus, je vous invite à lire [cet article de Linux Embedded](https://linuxembedded.fr/2020/11/namespaces-la-brique-de-base-des-conteneurs).
- `RestrictRealtime` empêche le processus d'utiliser des options relatives au "Système de planification en temps réel" (real-time scheduling system) ce système permet de planifier l'exécution de différentes actions, mais il peut être abusé afin de mener des attaques DoS (Denial of Service).
- `RestrictSUIDSGID` permet d'empêcher le service de changer l'utilisateur ou le groupe qui détient un fichier ou un dossier.
- `SystemCallFilter` permet de n'autoriser que certains appels systèmes (syscall).

Ça fait beaucoup de directives 😅 Si vous souhaitez en avoir une liste plus détaillée je vous invite à lire [la documentation de systemd](https://www.freedesktop.org/software/systemd/man/systemd.exec.html). Appliquons maintenant toutes ces directives que nous venons de voir, cela nous donne ce service systemd

```diff
[Unit]
Description=Unbound DNS server
Documentation=man:unbound(8)
After=network.target
Before=nss-lookup.target
Wants=nss-lookup.target

[Service]
Type=notify
User=unbound
Group=unbound
Restart=on-failure
EnvironmentFile=-/etc/default/unbound
ExecStartPre=-/usr/lib/unbound/package-helper chroot_setup
ExecStartPre=-/usr/lib/unbound/package-helper root_trust_anchor_update
ExecStart=/usr/sbin/unbound -d $DAEMON_OPTS
ExecReload=/usr/sbin/unbound-control reload
PIDFile=/etc/unbound/unbound.pid

AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
SecureBits=keep-caps
NoNewPrivileges=yes
ProtectSystem=full
ProtectHome=true
RestrictNamespaces=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
PrivateTmp=true
PrivateDevices=true
ProtectClock=true
ProtectControlGroups=true
ProtectKernelTunables=true
ProtectKernelLogs=true
ProtectKernelModules=true
LockPersonality=true
RestrictSUIDSGID=true
RemoveIPC=true
RestrictRealtime=true
SystemCallFilter=@system-service
MemoryDenyWriteExecute=true
ReadWriteDirectories=/etc/unbound

[Install]
WantedBy=multi-user.target
```

Et tout cela nous donne un score d'exposition de 1.9/10 ! 🎉 Vous pourrez retrouver une liste de services systemd les plus communs "renforcés" [sur le gitea d'I Learned](https://gitlab.ilearned.eu/i-learned/blog/Systemd-hardened), si vous voyez qu'il manque certains services n'hésitez pas à les ajouter en faisant une pull request ou en créant un ticket.

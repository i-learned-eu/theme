lang: fr
Author: Ramle
Date: 2021/10/17
Keywords: Android, sécurité, Verified boot, secure boot
slug: verified_boot
Title: Fonctionnement du démarrage d'un système Android
Summary: Les smartphones occupent une place de plus en plus importante, pour beaucoup d'usage ils remplacent même les machines de bureau plus classiques. La question de la sécurité du système embarqué dans ces machines est donc relativement importante, je vais, dans cet article, me pencher sur Android.
Category: Sysadmin/Android

Les smartphones occupent une place de plus en plus importante, pour beaucoup d'usage ils remplacent même les machines de bureau plus classiques. La question de la sécurité du système embarqué dans ces machines est donc relativement importante, je vais, dans cet article, me pencher sur Android.

## Démarrage d'Android

Pour bien comprendre les vecteurs d'attaques, il faut comprendre comment le système fonctionne. Le processus de démarrage est un élément indispensable au bon fonctionnement d'un système et de sa sécurité.

Lorsque le bouton "Power" est appuyé, Un code présent dans la rom est éxecuté, la ROM est l'endroit ou sont stockées les informations utiles au démarrage de l'appareil, est lancé. Ce programme est chargé d'amorcer le "bootloader", le bootloader est un programme qui se lance avant le noyau, il est chargé d'initialiser certains composants, il s'occupe aussi du lancement du noyau et de lui passer différentes options. Cette partie est comparable à l'amorçage en [UEFI](https://ilearned.eu.org/secure_boot.html) (ou BIOS).

Le noyau s'occupe de monter les différentes partitions et systèmes de fichiers spéciaux comme `/dev` pour ensuite, démarrer le système d'initialisation (init). L'init c'est le premier programme qui est lancé, il s'occupe de lancer un certain nombre de logiciels. Systemd, par exemple, est un init. Un des logiciels intéressants qui est lancé se nomme "native daemons"

![Boot d'android](/static/img/boot-android/boot_android.webp)
Native daemon lance plusieurs processus dont un qui est Zygote.

Zygote est lancé dans une VM Android RunTime (ART), ART c'est la machine virtuelle android pour lancer du code Java, Zygote s'occupe de lancer un processus nommé System Server, il lance aussi d'autres processus par exemple il précharge les classes Java. ART n'est pas la seule application lancée par native daemon, native daemon permet de lancer directement en "userland" des processus.

Un processus lancé en userland signifie qu'il est lancé avec des droits utilisateur classique et sans accès avec des privilèges élevés au kernel.

Quand un utilisateur clique sur l'icone d'une application l’événement est routé vers l'Activity Manager (lancé par le system server) c'est ce service qui va gérer les permissions de l'application et la démarrer en l'isolant dans un utilisateur spécifique. Une application n'a donc pas accès au stockage des autres applications ou de l'utilisateur (sauf s'il l'a autorisé) et n'a accès qu'aux permissions que l'utilisateur lui a autorisées.

Un souci se pose maintenant, tout est proprement isolé et le minimum tourne avec des privilèges élevés, mais comment vérifier que les fichiers n'ont pas été modifiés et qu'une application est bien celle qu'elle prétend ?

## Vérification du démarrage

Pour commencer, pour le processus de boot il est vérifié via une technologie nommée "Verified Boot". Verified boot est l'équivalent mobile de [Secure Boot](https://ilearned.eu.org/secure_boot.html), il y existe plusieurs "état" :

- Verrouillé
- Verrouillé avec une chaine de clés personnalisées
- Ouvert

Verrouillé signifie qu'il y a une vérification au démarrage des signatures cryptographique des éléments présents dans /boot, les clés peuvent être celle de base du constructeur, ou bien avec une chaine différente (l'utilisateur qui a remplacé le système par exemple). D'ailleurs c'est justement cette partie là que certains constructeurs bloque et qui empêche de modifier la ROM (c'est le cas par exemple d'huawei, xiaomi, et bien d'autre).

![Procédure vérification](/static/img/boot-android/verified_boot.webp)

Le bootloader et le kernel sont tout deux signés par une clé privée et vérifié par l'ordiphone sur base d'une clé publique stockée dans une partie matérielle accessible uniquement en lecture (en réalité c'est modifiable, mais souvent il faut effectuer une action depuis le système, pour éviter qu'un attaquant modifie facilement). Verified boot permet aussi d'empêcher le "downgrade" du système vers une version précédente en notant la version actuelle dans une partie elle aussi en lecture seule, cette protection empêche notamment de profiter d'une faille présente dans une vielle version de pouvoir être exploitée.

Verified boot permet d'éviter un kernel ou bootloader corrompu, mais les partitions systèmes restent vulnérables à une modification, pour éviter ça dm-verity est utilisé. Ce mécanisme se base sur le framework Device mapper qui est directement géré par Linux (le noyau) (DM).

Device mapper permet de faire des périphériques de stockage virtuel qui peuvent avoir plusieurs propriétés spécifique, par exemple dans notre cas empêcher la lecture si le noyau détecte un bloc corrompu.

Pour vérifier que la partition n'ai pas été modifiée, il y a une vérification du bloc lu en temps réel, la vérification se base sur une arborescence de condensats.

![Dm-verity hash table](/static/img/boot-android/dm-verity-hash-table.webp)
(source : [https://source.android.com/security/verifiedboot/dm-verity](https://source.android.com/security/verifiedboot/dm-verity))

Pour vérifier que personne n'aie modifié la table de hashs, elle est signé par une pair de clé. Cette clé est mise dans la partition boot et est elle signée par la clé utilisée pour verified boot.

## Chiffrement

La partition qui contient les données utilisateurs ne peut, elle, pas être mises en lecture seule, contrairement aux partitions systèmes.
Pour éviter qu'une personne puisse modifier ou lire la partition elle est donc chiffrée.

Contrairement à ce qu'on fait d'habitude, chaque fichier est chiffré au lieu d'avoir toute la partition. Les fichiers sont doncs seulement déchiffré quand ils sont lus. Le chiffrement se base sur votre système d'authentification (code pin, biométrie, etc.) comme clé. Cette clé est gardée en mémoire après avoir été tapée la première fois au démarrage du profile. Tant que le profil n'est pas déconnecté la clé reste en mémoire, c'est une source d'attaque possible (d'où l'importance d’éteindre son téléphone si on ne l'utilise pas). La consomation sur la ram ou le CPU n'est pas forcément plus important, sur du FDE on déchiffre par bloc, là ou sur du FBE on déchiffre par fichier ce qui n'est pas forcément plus lourd en RAM ou CPU.

L'avantage du FBE (file-based encryption) au lieu du FDE (full-disk encryption) est dans le cas d'une utilisation de plusieurs profiles, chaque profile aura sa clé et ne saura donc pas déchiffrer les fichiers d'un autre profile.

Title: Processus de démarrage d'android
Author: Ramle
Slug: boot_android
Date: 2021/10/10
Status: draft
Description: Les smartphones occupent une place de plus en plus importante, pour beaucoup d'usage ils remplacent même les machines de bureau plus classiques. La question de la sécurité du système embarqué dans ces machines est donc relativement importante, je vais, dans cet article, me pencher sur Android.

Les smartphones occupent une place de plus en plus importante, pour beaucoup d'usage ils remplacent même les machines de bureau plus classiques. La question de la sécurité du système embarqué dans ces machines est donc relativement importante, je vais, dans cet article, me pencher sur Android.

## Démarrage d'Android

Pour bien comprendre les vecteurs d'attaques, il faut comprendre comment le système fonctionne. Le processus de démarrage est un éléments indispensable au bon fonctionnement d'un système, et de sa sécurité.

Lorsque que le bouton "Power" est appuyé, un code présent dans la ROM, la ROM est l'endroit ou est stockées les informations utiles au démarrage de l'appareil, est lancé. Ce programme est chargé d'amorcer le "bootloader", le bootloader est un programme qui se lance avant le noyau, il est chargé d'initialiser certains composants, il s'occupe aussi du lancement du noyau et de lui passer différentes options. Cette partie est comparable à l'amorçage en UEFI (ou BIOS).

Le noyau s'occupe de monter les différentes partitions et système de fichiers spéciaux comme `/dev` pour ensuite, démarrer le système d'initialisation (init). L'init c'est le premier programme qui est lancé, il s'occupe de lancer un certains nombres de logiciels. Un des logiciels intéressant qui est lancé se nomme "native daemons"

![Boot execution(4).png](Boot%20android%20a50a09146809407a9cc462a52238a56e/Boot_execution(4).png)

Native daemon lance plusieurs processus dont un qui est Zygote. 

Zygote est lancé dans une VM Android RunTime (ART), Zygote s'occupe de lancer un processus nommé System Server, il lance aussi d'autre processus par exemple il précharge les classes Java. 

Quand un utilisateur clique sur l'icone d'une application l’événement est routé vers l'Activity Manager (lancé par le system server) c'est ce service qui va gérer les permissions de l'application et la démarrer en l'isolant dans un utilisateur spécifique. Une application n'a donc pas accès au stockage des autres applications ou de l'utilisateur (sauf si il l'a autorisé) et n'a accès qu'au permission que l'utilisateur lui a autorisé.

![Untitled](Boot%20android%20a50a09146809407a9cc462a52238a56e/Untitled.png)

Un soucis se pose maintenant, tout est proprement isolé et le minimum tourne avec des privilèges élevés mais comment vérifier que les fichiers n'ont pas été modifié et qu'une application est bien celle qu'elle prétends ?

## Vérification du démarrage

Pour commencer, pour le processus de boot il est vérifié via une technologie nommée "Verified Boot". Verified boot est l'équivalent mobile de [Secure Boot](https://ilearned.eu.org/secure_boot.html), il y existe plusieurs "état" :

- Verrouillé
- Verrouillé avec une chaine de clés personnalisées
- Ouvert

Verrouillé signifie qu'il y a une vérification au démarrage des signatures, les clés peuvent être celle de base du constructeur, ou bien avec une chaine différente (l'utilisateur qui a remplacé le système par exemple). D'ailleurs c'est justement cette partie là que certains constructeur bloque et qui empêche de modifier la rom (c'est le cas par exemple d'huawei, xiaomi, et bien d'autre).

![external-content.duckduckgo.com.jpg](Boot%20android%20a50a09146809407a9cc462a52238a56e/external-content.duckduckgo.com.jpg)

Le bootloader et le kernel sont tout deux signé par une clé privée et vérifié par l'ordiphone sur base d'une clé public stockée dans une partie matériel accessible uniquement en lecture (en réalité c'est modifiable, mais souvent il faut effectuer une action depuis le système, pour éviter qu'un attaquant modifie facilement). Verified boot permet aussi d'empêcher le "downgrade" du système vers une version précédente en notant la version actuel dans une partie elle aussi en lecture seul, cette protection empêche notamment de profiter d'une faille présente dans une vielle version de pouvoir être exploitée.

Verified boot permet d'éviter un kernel ou bootloader corrompu, mais il reste les partitions systèmes reste vulnérable à une modification, pour éviter ça dm-verity est utilisé. Ce mécanisme se base sur le framework Device mapper qui est directement géré par Linux (le noyau) (DM).

Device mapper permet de faire des périphériques de stockage virtuels qui peuvent avoir plusieurs propriété spécifique, par exemple dans notre cas empêcher la lecture si le noyau détecte un bloque corrompu.

Pour vérifier que la partition n'ai pas été modifiée, il y a une vérification du bloque lu en temps réel, la vérification se base sur une arborescence de condensats. 

![dm-verity-hash-table.png](Boot%20android%20a50a09146809407a9cc462a52238a56e/dm-verity-hash-table.png)

Pour vérifier que personne n'ait modifié la table de hashs, elle est signé par une pair de clé. Cette clé est mise dans la partition boot et est elle signée par la clé utilisée pour verified boot.

## Chiffrement

La partitions qui contient les données utilisateurs ne peut elle ne pas être mise en lecture seule, contrairement aux partitions systèmes.
Pour éviter qu'une personne puisse modifier ou lire la partition elle est donc chiffrée.

Contrairement à ce qu'on fait d'habitude, chaque fichier est chiffré au lieu d'avoir toutes la partitions. Les fichiers sont donc seulement déchiffré quand ils sont lu. Le chiffrement se base sur votre système d'authentification (code pin, biométrie, etc.) comme clé. Cette clé est gardée en mémoire après avoir été tapée la première fois au démarrage du profile. Tant que le profile n'est pas déconnecté la clé reste en mémoire, c'est une source d'attaque possible (d'ou l'importance d’éteindre son téléphone si on ne l'utilise pas).

L'avantage du FBE (file-based encryption) au lieu du FDE (full-disk encryption) est dans le cas d'une utilisation de plusieurs profiles, chaque profile aura sa clé et ne sera donc pas déchiffrer les fichiers d'un autre profile.

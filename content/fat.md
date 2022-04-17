lang: fr
title: FAT, comment fonctionne un système de fichier
Keywords: FAT, FAT32, FAT16, FS, Windows, Linux
Date: 2021-12-05
Author: Ownesis
Summary: FAT, qu'est-ce que c'est, a quoi il sert et comment fonctionne ce système de fichier ?.
Slug: fat
Category: Sysadmin

Aujourd'hui je vais vous parler du système de fichier `FAT` (File Allocation Table).
Avant de commencer, qu'est-ce qu'un système de fichier ?
Il peut désigner deux choses :

1. La hiérarchie d'un système d'exploitation, par exemple sous les Unix like comme BSD, Linux, macOS, le système commence a la racine `/`.
Sous Windows, le système commence depuis `C:\`.

2. L'organisation du fichier dans un support de stockage (volume physique ou logique), et il en existe tout un tas de type différent : `NTFS`, `FAT`, `FAT32`, `ext4fs`, `zfs`, ...

Ici on va parler de la 2ᵉ définition et de `FAT`.
Ce système de fichier a été utilisé pour le système Windows, on le retrouve aussi parfois sur des clés USB.
La table d'allocation indexe le contenu d'un fichier se trouvant dans un support de stockage avec son emplacement dans ledit support.
Il faut savoir que les "blocs" qui constituent un fichier ne peuvent pas être stockés de manière contiguë sur le disque, le fichier est "fragmenté". Une table d'allocation permet d'indexer et de retrouver chaque fragment du fichier.
Le système `FAT` est un système sur 16 bits et permet de nommer un fichier avec un nom d'une longueur de 8 caractères et d'une extension de 3 caractères. On appelle ce système `FAT16` (16 pour les 16 bits).

8 caractères + les 3 caractères d'extension, c'est... ridicule. Pour remédier à ce "problème", Windows 95, qui utilise le système FAT16, avait une version "amélioré" de celle ci, le `VFAT` (Virtual FAT).
Ce système contrairement au `FAT16`, était un système 32 bits et permettait d'enregistrer un fichier avec un nom de 255 caractères de long.

Revenons sur notre système 16 bits. Que signifie les `16 bits` ? C'est le nombre maximum de **cluster** que peut adresser le système de fichier.

> Un **cluster** ? qu'est-ce donc ?

Pour faire simple, un **cluster** est un groupe de **secteurs**, c'est dans ces clusters que sont stocké les données d'un fichier.

> Et qu'est ce que c'est qu'un **secteurs** ?

Un **secteur** est la plus petite unité physique de stockage sur un support de donnée.

Pour notre exemple, on va partir du principe qu'un secteur a une taille de `512` octets.
Un cluster a une taille fixée de secteurs (4, 8, 16, 32, ...).
Pour déterminer la taille maximum d'une partition `FAT16` il faut multiplier la taille d'un cluster avec la taille d'un secteur, partons du principe que nous avons un cluster de `32` secteurs, `32 * 512` = `16 384`.
Maintenant, il suffit de multiplier ce nombre par le nombre de clusters maximum géré par le système de fichier (`2^16 = 65536`):
`16 384 * 65536` = `1073741824` (~1Go)

Un fichier occupe un cluster, même une partie de fichier. En gros, si on reprend notre exemple plus haut, sur des secteurs de `16 384` octets, si un fichier fait `20 000` octets, les `16 384` premiers octets du fichier seront stocké dans un cluster entier, mais les `3616` derniers octets du fichier seront stocké dans un autre cluster lui aussi de `16 384` octets, (`16 384 - 3616`)  = `12 768`, on perd donc **12 768** octets !
Ces octets-là ne pourront pas être utilisés par un autre fichier. Alors vous l'aurez surement compris, plus un cluster est petit en taille, moins il y a de gaspillage de place.
En moyenne, on estime qu'un fichier gaspille la moitié d'un cluster... aïe.


Le système `FAT` est composé de 3 grandes sections :

1. Le secteur de boot, contenant le `BPB` c'est le premier secteur de la partition.
2. Les tables d'allocation
3. Le répertoire racine

On ne va pas s'attarder sur le secteur de boot.

Le répertoire racine, pour faire simple, c'est lui qui va stocker le nom du fichier, sa taille, ses attributs, la date et heure de création, de modification etc ; et le plus important, le numéro du premier cluster.

Il faut imaginer une Table d'allocation comme un tableau de "nombres" indexé par un numéro de cluster.
Chaque "nombres", correspond à une information concernant le cluster :

| Nombres         | Description                                      |
| --------------- |-------------------------------------------------:|
| 0x0000          | Cluster vide                                     |
| 0x0001          | Cluster réservé                                  |
| 0x0002 - 0xFFEF | Cluster utilisé, pointant vers le cluster suivant |
| 0xFFF0 - 0xFFF6 | Valeurs réservées                                |
| 0xFFF7          | Mauvais cluster                                  |
| 0xFFF8 - 0xFFFF | Cluster utilisé, dernier cluster                  |

On pourrait imaginer la table d'allocation suivante :
> C*x* = Cluster n°*x*

![Deux fichier, un sur plusieurs clusters et un second sur un seul](/static/img/fat/fat.webp)

> Un fichier qui utilse les clusters 2, 3 et 5 et un autre fichier le cluster 6.

Voilà, c'est fini pour cet article, j'ai essayé d'être plus simple possible pour que vous ayez l'idée de comment fonctionne et à quoi peut ressembler un système de fichier.
Pour plus de détails je vous invite à lire les sources ci-dessous, plus complète, notamment celle de Wikipédia.

Source : [Wikipedia (File Allocation Table)](https://fr.wikipedia.org/wiki/File_Allocation_Table) - [Commentcamarche (FAT16 et FAT32)](https://www.commentcamarche.net/contents/1016-fat16-et-fat32)

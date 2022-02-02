Author: Ramle 
Date: 2021/07/07
Keywords: sécurité
Slug: secure_boot
Summary: La vérification de l’intégrité d'un système lors de son démarrage est crucial, si un attaquant est capable de modifier des fichiers il peut facilement avoir les pleins pouvoirs pour y implémenter un malware. Pour remédier à cela, Secure Boot a été créé.
Title: Vérifier l’intégrité d'un système d'exploitation grâce à Secure Boot.

La sécurité d’un système dépend de beaucoup de facteurs, un des facteurs importants est de pouvoir vérifier l’intégrité du système démarré, en effet sans cette vérification un attaquant pourrait sans trop de difficultés modifier les fichiers de démarrage pour ajouter un malware. Cet article se concentrera sur les machines de bureau.

Pour bien comprendre comment des attaques peuvent être effectuées pendant le boot, il est important de comprendre le fonctionnement du démarrage en mode BIOS, et son remplaçant l'UEFI.

## BIOS

Le démarrage en BIOS s'appuie sur une table des partitions en MBR (Master Boot Record). Pour démarrer le BIOS va exécuter du code contenu dans la table des partitions, ce code s'occupe de passer la main au bootloader qui va s'occuper de lancer le système. Un problème assez flagrant apparait déjà, du code peut être directement inséré dans cette partie, aucune vérification n'est effectuée par le BIOS. Un attaquant pourrait aussi attaquer le bootloader qui ne peut pas être chiffré.

Sous Linux (nous verrons le fonctionnement de Windows un peu plus loin), le bootloader le plus courant est GRUB. Il insère dans le MBR de quoi charger son code complet qui est contenu dans `/boot`, la plupart des bootloaders sous Linux fonctionnent sur le même principe.

![Un système non chiffré](/static/img/secure_boot/Boot_mbr.webp)

Pour éviter une modification du système on pourrait chiffrer la partition root (aussi appelé Userland) et faire un `/boot` à part (le bootloader ne peut pas être chiffré). Un problème se pose alors, l'initramfs et le kernel sont toujours en clair.

![Un système chiffré avec seulement le userland de chiffré](/static/img/secure_boot/Boot_mbr(1).webp)

GRUB (et c'est à ma connaissance le seul) permet de déchiffrer le partition boot, pour garder l'initramfs et le kernel chiffré. Mais GRUB en lui même est toujours modifiable, même chose pour le code exécuté directement dans le MBR.

![Un système chiffré avec le userland et le kernel de chiffré](/static/img/secure_boot/Boot_mbr(2).webp)

En plus de ne pas être totalement sécurisé, avec cette méthode la phrase de passe doit être tapée deux fois : une fois pour lire l'initramfs et une autre fois pour déchiffrer la partition root. (GRUB ne la retient pas.)

Une solution possible serait de signer les différents éléments du boot, le problème est qu'en BIOS aucun mécanisme pour la vérification de signature existe.

Avec un BIOS nous n'avons pas de possibilité de sécuriser entièrement un système Linux.

Pour Windows, le concept est très proche. Le BIOS va exécuter le code dans le MBR, ce code va enclencher le bootloader de Windows (qui, depuis Windows Vista, est bootmgr). Chiffrer son disque pose le même soucis que sous Linux : le bootloader restera en clair.

## UEFI

Avec UEFI on se passe de MBR au profit de GPT qui apporte un certain nombre d'avantages. Le processus de boot ne se passe plus par un code exécutable dans la partie MBR, ce code est contenu dans une partition en FAT32 (ou FAT16), ce qui permet de ne plus être aussi limité en taille (la partie dédié au code de démarrage dans MBR n'est que de 446 octets). UEFI apporte aussi une évolution majeure pour la sécurité : Secure Boot, c'est un moyen de vérifier l'intégrité via une signature du fichier EFI. Un fichier EFI est un exécutable lancé par l'UEFI qu'on pourrait le comparer aux ELF de Linux ou aux exe de Windows.

Lorsque qu'un PC avec Secure Boot démarre, il vérifie le binaire EFI pour voir si la signature correspond à une clé de "confiance" et si la signature n'est pas dans dans la liste des clés à refuser.

L'UEFI se base sur des variables pour les clés, vous pouvez les voir depuis Linux via l'utilitaire "efi-readvars". Ce qui sur ma machine donne :

```jsx
Variable PK, length 823
PK: List 0, type X509
    Signature 0, size 795, owner 5b2a4205-8ee1-404d-a357-45629f968019
        Subject:
            CN=Ramle PK
        Issuer:
            CN=Ramle PK
Variable KEK, length 825
KEK: List 0, type X509
    Signature 0, size 797, owner 5b2a4205-8ee1-404d-a357-45629f968019
        Subject:
            CN=Ramle KEK
        Issuer:
            CN=Ramle KEK
Variable db, length 823
db: List 0, type X509
    Signature 0, size 795, owner 5b2a4205-8ee1-404d-a357-45629f968019
        Subject:
            CN=Ramle DB
        Issuer:
            CN=Ramle DB
Variable dbx has no entries
Variable MokList has no entries
```

Regardons de plus près chaque variable :

- PK : C'est la clé la plus haute dans la chaine de confiance, elle est là pour signer la clé KEK, une seule clé est possible dans cette variable. En général c'est le constructeur qui met sa clé, si vous voulez contrôler totalement la chaine de confiance il faudra donc la changer.
- KEK : Ces clé sont utilisées pour signer les clés qui iront dans DB ou DBX, souvent de base il y a 2 KEK, une pour Microsoft et une autre pour le fabricant.
- DB : Ce sont les clés utilisées pour la vérifications des binaires EFI. Souvent l'ordinateur vient avec les clés du constructeur, de Microsoft, Canonical (entreprise qui est derrière Ubuntu) et parfois d'autres entreprises.
- DBX : C'est la liste des clés qui ne sont plus de confiance.
- MOKList : C'est utilisé par un outil du nom de Shim, cet outil est là pour charger un autre bootloader qui ne serait pas signé avec les clés présentes dans DB. Shim va vérifier le bootloader via les clés dans la MOKList qui est géré par l'utilisateur, et non via l'UEFI directement.

![La chaine de confiance de Secure Boot](/static/img/secure_boot/Cl_secure_boot(1).webp)

Ces variables sont bien sûr modifiables sur la plupart des PC, ce qui permet de gérer sa propre PKI (public key infrastructure).

Si on veut un réel contrôle il faut gérer soit même ses clés. Sous Linux c'est possible sans trop de difficultés, FreeBSD et OpenBSD semblent supporter aussi (je n'ai pas eu l'occasion de tester) et sous Windows on peut soit utiliser les clés de Microsoft ou utiliser ses propres clés ce qui semble en théorie possible.

J'espère que cette article vous aura plus, je pense prochainement faire un petit guide pour la gestion de Secure Boot sous Linux, je vous laisse donc surveiller les sorties 👀. On se retrouve après demain pour un article sur MQTT.

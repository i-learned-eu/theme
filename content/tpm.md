lang: fr
Author: Ramle
Date: 2021/07/31
Keywords: sécurité
Slug: tpm
Summary: Windows 11 montre aux yeux du public l’existence d'une puce matériel du nom de TPM, mais quelle est cette puce et pourquoi Microsoft pousse à son adoption ?
title: La puce TPM, quelle est son utilité ?
Category: Sysadmin

Il y a moins d'un mois Microsoft annonçait officiellement Windows 11. Cette nouvelle version à fait débat, et pour cause, beaucoup (trop) d'appareils sont incompatibles avec cette version de Windows, une des raisons avancées par Microsoft est le support manquant de TPM 2.0. Mais au fond, Qu'est ce que TPM et quels sont les changements apporté par la deuxième version de TPM.

TPM est l'acronyme de "Trusted Platform Module", c'est une puce qui permet de faire des opérations cryptographiques, ou de garder des secrets.

Cette puce est principalement faite pour générer des clés RSA – RSA est un algorithme de cryptographie asymétrique – stocker ces clés et gérer l'accès à ces dites clés. Cette puce est aussi utilisée pour [Secure Boot](https://ilearned.eu.org/secure_boot.html).

Une puce TPM possède une clé RSA qui permet de l'authentifier, cette clé ne peut en théorie pas sortir de la puce.

Un des usages principaux de TPM est de stocker différents secrets, pour par exemple chiffrer un disque avec une technologie comme BitLocker sous Windows, ou Luks sous Linux. La sécurité du stockage de la clé pourrait poser question, comment s'assurer qu'un autre système ne puisse pas avoir accès a la clé de déchiffrement ? Afin d'améliorer la sécurité de cette puce, on peut configurer un PIN à entrer pour accéder à la clé de déchiffrement.

Si la clé n'est pas protégée par un PIN, la puce laissera quand même l'accès uniquement au système qui a crée la clé, même si dans certains cas particulier la vérification ne se fait pas correctement.

Comme faille de sécurité dans TPM on peut notamment citer [TPM-FAIL](https://tpm.fail) qui permet simplement d'extraire la clé privée. Un autre problème de sécurité que présente TPM est qu'avec un accès physique il est possible d'espionner ce que la puce fait et donc d'en extraire des données confidentielles, si vous souhaitez en savoir plus, la page Wikipedia sur TPM cite d'autres failles de sécurité : [https://en.wikipedia.org/wiki/Trusted_Platform_Module#Attacks](https://en.wikipedia.org/wiki/Trusted_Platform_Module#Attacks).

Un autre problème de TPM qui est très répandu c'est le vecteur d'attaque physique, en observant directement sur les bus de la puce avec du matériel spécifique il est possible d'extraire les clés de la puce, ce type d'attaque se nomme [cold boot atttack](https://en.wikipedia.org/wiki/Cold_boot_attack).

La puce TPM est divisée en plusieurs partie qu'on nomme des Platform configuration Registers qui ont plusieurs utilité, comme le stockage de clé, firmware etc.

TPM a connu des évolutions, je vais me concentrer ici seulement sur la version 1.2 et 2 de TPM. Une des avancées majeure est l'implémentation des courbes elliptiques sur la version 2, les algorithmes de chiffrement à courbe elliptique sont des algorithmes de cryptographie asymétrique, concurrents à RSA
notamment, qui au lieu d'utiliser les nombres premiers utilisent des courbes elliptiques, l'avantage comparé à RSA c'est leur résistance supposée aux ordinateurs quantiques. Une autre avancée est le support de SHA256 qui est bien plus résistant que SHA1 à différent type d'attaque.

À mon avis, le fait pour Windows 11 de forcer TPM est relativement inutile, en effet BitLocker n'est pas activé par défaut, et [Secure Boot](https://ilearned.eu.org/secure_boot.html) ne dépends pas forcément de TPM. Le mieux serait de recommander sans pour autant forcer. TPM reste très intéressant pour éviter de taper un mot de passe au boot, qui en plus de prendre du temps peut être vu par un attaquant, et permettre de vérifier l’intégrité du démarrage en séparant la gestion des clés du bios (l'avantage est que pour changer le jeu de clés publiques il faut effacer la clé de déchiffrement). Un des soucis les plus important de TPM reste que la plupart des implémentations ne sont pas libres, une backdoor pourrait donc y être inséré par le constructeur.

Une alternative à TPM peut être des puces plus spécifique comme la puce titan de google, ou T2, mais ces deux puces restent malheureusement propriétaires.

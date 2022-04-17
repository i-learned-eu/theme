lang: fr
Author: Eban
Date: 2021/10/24
Keywords: blockchain, sécurité
Slug: blockchain
Summary: Ces derniers temps, on entend beaucoup parler de la blockchain comme étant le remède à tous nos maux. Dans cet article nous allons nous pencher sur le fonctionnement technique de cette fameuse blockchain et voir en quoi elle peut (ou non 😏) être utile.
Title: La blockchain, comment ça marche vraiment ?
Category: Sysadmin

Ces derniers temps, on entend beaucoup parler de *la blockchain* comme étant le remède à tous nos maux. Dans cet article nous allons nous pencher sur le fonctionnement **technique** de cette fameuse blockchain et voir en quoi elle peut (ou non 😏) être utile.

# Une blockchain, ça veut dire quoi ?

Une blockchain, car il en existe plusieurs, est une chaine de blocs liés ensemble cryptographiquement. Cela permet donc de créer une chaine de confiance non falsifiable, notamment utile dans le cadre des cryptomonnaies.

Afin de les lier entre eux, chaque bloc de la chaine contient le hash du bloc précédent, ce qui permet de s'assurer que la chaine n'est pas falsifiée.

![Une chaine de blocs avec à l'intérieur de chacun le hash du précédent](/static/img/blockchain/blockchain.webp)

Si un attaquant cherchait à ajouter un bloc a posteriori, il serait tout de suite détecté. La chaine de blocs a aussi pour avantage d'être vérifiable par n'importe qui ayant à sa disposition un ordinateur capable d'exécuter des fonctions de hashage.

![Une chaine de blocs avec à l'intérieur de chacun le hash du précédent, sauf le troisième qui est un intrus](/static/img/blockchain/blockchain_hacked.webp)

# Comment ça fonctionne concrètement ?

Vous l'imaginez bien, la vision présentée ci-dessus est grandement simplifiée. Dans les fait, les blockchain publiques sont confrontées à des problématiques comme le fait que le réseau puisse être saturé par une arrivée massive de paquets. Pour éviter cela, a été créée la méthode du **Proof of Work**.

Afin de complexifier la création d'un bloc, la méthode du Proof of Work (PoW) requiert d'ajouter un champ à notre bloc que l'on remplira de données aléatoirement jusqu'à ce que le hash du paquet commence par un nombre donné de 0 (et donc soit d'une certaine taille). Pour le bitcoin par exemple à date d'écriture de cet article, pour qu'un paquet soit valide, il faut que son hash commence par 19 zéros. Cette valeur est déterminée en fonction des 2016 derniers blocs minés (et change donc très fréquemment) afin d'assurer qu'il n'y ai toujours en moyenne qu'un bloc validé toutes les dix minutes. Cette méthode se base donc sur la complexité calculatoire des fonctions de hashage. Un bloc a la structure suivante

![ID Du bloc - Hash du bloc précédent - Données - Proof of Work - Hash de ce bloc](/static/img/blockchain/block_structure.webp)

Le problème de cette méthode, c'est qu'elle est très énergivore, elle implique d'avoir des fermes entières de "minage" (qui ne sont donc en réalité que des machines qui calculent des hash) qui consomment beaucoup d'électricité afin de garantir la sécurité de la blockchain. Entre le mineurs, la conccurence est rude et au final, seul le travail d'un mineur sera récompensé, toutes les autres fermes ont donc travaillé, et consommé beaucoup d'électricité pour... rien. À l'heure d'une prise de conscience généralisée autour de l'urgence climatique, cette méthode semble donc inadaptée.

Afin de répondre aux problématiques, notamment environnementales, que pose le Proof of Work, a été créé le **Proof of Stake**.

Contrairement au Proof of Work, cette méthode ne se base pas sur la complexité cryptographique des fonctions de hashage, mais sur une quantité de cryptomonnaie mise sous *séquestre*. Les mineurs mettent sous *séquestre* une certaine quantité de cryptomonnaie, plus on a mis d'argent sous *séquestre*, plus on augmente ses chances d'être choisit aléatoirement pour valider le bloc, et donc de toucher une récompense.

Le problème de ces deux systèmes, et c'est encore plus flagrant avec le Proof of Stake, est que les personnes qui peuvent investir le plus au début, les "riches", auront plus de chances d'être choisit pour valider un bloc, et donc de devenir encore plus "riche". Ce genre de système est pûrement capitaliste (fondé sur la possession d'un capital en cryptomonnaies), et donc pas forcément souhaitable 👀.

Afin d'éviter ces travers, la blockchain Polkadot a mis en place un système très intéressant appelé Nominated Proof of Stake. Avec ce système, les mineurs sont appelés **validateurs**, ces validateurs sont élus et ont, comme avec les autres modes de fonctionnement pour rôle de valider les différents blocs. Afin de désigner les validateurs, des **nominateurs** indiquent les candidats au rôle de validateur en qui ils ont confiance, et mettent sous *séquestre* une quantité de cryptomonnaies pour les supporter. Si un candidat qu'ils ont soutenu est élu validateur, ils reçoivent une part des gains (ou des sanctions) de ce validateur. Ce fonctionnement donne donc à chacun, riche ou pas, une voix **égale**, ce qui permet de rendre ce système bien moins inégalitaire. Néanmoins ce système n'est pas exempté de problèmes, un personne riche pourrait par exemple créer une multitude de comptes pour les faire voter pour lui, et remporter la mise à chaque fois mais aussi peser plus que les autres dans le processus de décision relatif à la blockchain, et donc de pouvoir changer les règles à son avantage.

Je vous invite à lire [cet article](https://medium.com/web3foundation/how-nominated-proof-of-stake-will-work-in-polkadot-377d70c6bd43) pour plus d'informations

# Conclusion

Pour conclure, les blockchain sont des systèmes très intéressants permettant de créer une forme de **confiance** numérique vérifiable par tout le monde. Cela représente donc une avancée considérable dans l'émancipation des grosses plateformes centralisées qui dominent actuellement le monde de l'informatique. Il faut néanmoins rester vigilant-es, les blockchains ne sont que des outils, il ne faut donc pas en attendre autre chose qu'un outil.

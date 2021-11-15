Author: Eban 
Date: 2021/11/14
Keywords: cryptographie, sécurité
Slug: rsa
Summary: RSA est sûrement l'algorithme de chiffrement asymétrique le plus connu, il est utilisé chaque jour par des millions d'appareils, même le certificat TLS du site que vous visitez en ce moment est basé sur RSA ! Cet article détaillera le fonctionnement mathématique de RSA, aucun pré-requis n'est nécessaire (à part peut-être une tasse de café ☕).
Title: RSA, comment ça marche ?

RSA est sûrement l'algorithme de chiffrement asymétrique le plus connu, il est utilisé chaque jour par des millions d'appareils, même le certificat TLS du site que vous visitez en ce moment est basé sur RSA ! Cet article détaillera le fonctionnement mathématique de RSA, aucun prérequis n'est nécessaire (à part peut-être une tasse de café ☕).

# La cryptographie asymétrique, qu'est-ce que c'est ?

Il existe deux types d'algorithmes de chiffrement 

- Les algorithmes de chiffrement **symétriques** : ils impliquent d'avoir un secret (un "mot de passe") partagé entre les différents appareils. Ce genre d'algorithme a pour avantage d'être plutôt rapide mais a pour inconvénient, et pas des moindres, de devoir avoir un canal sécurisé pour transmettre le secret.
- Les algorithmes de chiffrement **asymétriques** : ces algorithmes, dont RSA fait partie, ne nécessitent pas de partager un secret à l'avance. Ils se basent sur une paire de clés (une publique et une privée) liées mathématiquement. Cet algorithme a donc pour avantage de ne pas nécessiter un canal sécurisé pour initier la connexion, mais pour inconvénient d'être nettement moins rapide que les algorithmes de chiffrement symétriques.

# Alors, comment fonctionne RSA ?

Cette partie sera un peu plus mathématique mais devrait être accessible pour tout le monde. Si vous avez des questions, n'hésitez pas à les poser dans les commentaires en bas de cet article !

## Génération des clés

1. On choisit deux nombres premier distincts $p$ et $q$ (pour rappel, un nombre premier est un nombre qui n'a que deux diviseurs, 1 et lui-même.)
    
    $$p = 5 \\
    q = 13$$
    
2. On calcule $n$ le produit de $p$ et $q$.
    
    $$n = 5×13 \\
    n = 65$$
    
3. On calcule la *valeur indicatrice d'Euler* en $n$. *L'indicaquoi ?* 🤨 La valeur indicatrice d'Euler c'est une fonction notée $\phi$ qui, à tout entier naturel $n$ associe le nombre d'entiers naturels compris entre 1 et $n$ et premiers avec $n$. *Premier avec ?* 🤔 Quand deux nombres sont premiers entre eux, ça veut simplement dire qu'ils n'ont aucun [facteur premier](http://www.recreomath.qc.ca/am_facteur.htm) en commun.
    
    Par exemple, 12 est premier avec 5 car dans la décomposition en facteurs premiers de 12 ($2\times2\times3$) on ne retrouve pas 5
    
    Voici un petit exemple de la valeur indicatrice d'Euler qui devrait vous permettre de bien comprendre :
    
    $$\phi(12) = 4 \\ \small{(1, 5, 7, 11)}$$
    
    Les nombres 1, 5, 7 et 11 sont bien premiers avec 12.
    
    Nous allons donc calculer la valeur indicatrice d'Euler en $n$.
    Pour calculer cette dernière, il faut connaitre les propriétés suivantes :
    
    $$\phi(a\times b) = \phi(a)\times \phi(b)$$
    
    Pour n'importe quel nombre premier c, $\phi(c)=c-1$
    
    Avec ces deux propriétés en tête et sachant que p et q sont deux nombres premiers, on peut affirmer que
    
    $$\phi(p) =p - 1 \\
    \phi(q) = q-1 \\
    \phi(n) = \phi(p \times q) = \phi(p) \times \phi(q) \\
    \phi(n) = (p - 1) \times (q - 1)$$
    
    On remplace par nos valeurs d'exemple
    
    $$\phi(5) = 5 - 1 \\
    \phi(13) = 13-1 \\
    \phi(5 \times 13) = \phi(5)*\phi(13) \\
    \phi(65) = (5 - 1)(13 - 1) \\
    \phi(65) = 4*12 \\
    \phi(65) = 48 \\
    $$
    
4. On choisit un entier naturel $e$ premier avec $\phi(n)$ (qui est donc ici 48).
    
    $$e = 
    5$$
    
5. On calcule $d$, l'inverse modulaire de $e$ modulo $n$. *L'inverse modulaire ? Modulo ? Qu'est-ce que c'est ces trucs ?* 🧐
Pour comprendre le concept d'inverse modulaire, il est nécessaire de comprendre ce qu'est la congruence sur les entiers. Deux entiers $a$ et $b$ sont dits congrus modulo $n$ si le reste de la division euclidienne de $a$ par $n$ et de $b$ par $n$ est identique. Par exemple 33 et 9 sont dits congrus modulo 12 car le reste de la division euclidienneHee de 33 par 12 est 9, et que le reste de la division euclidienne de 9 par 12 est 9. On note cela de la façon suivante :
    
    $$33 \equiv 9 \mod{12} \\
    \small\textit{33 et 9 sont congrus modulo 12}$$
    
    Une autre façon de se représenter la chose serait d'imaginer une horloge (avec donc 12 heures), si on fait tourner l'aiguille des heures de 9 heures ou de 33, elle se retrouvera au même endroit à la fin.
    
    ![Horloge tournant 33 heures et horloge tournant 9 heurs](/static/img/rsa/clock.gif)
    
    Donc, calculer l'inverse modulaire d'un entier $a$ modulo $n$ c'est trouver un entier $u$ résolvant l'équation : 
    
    $$au \equiv 1 \mod{n}$$
    
    Ce qui revient donc à chercher un nombre $u$ tel que le reste de la division euclidienne de $a \times u$ par n soit égal au reste de la division euclidienne de 1 par $e$.
    
    Comment déterminer $u$ ? Et bien pas de formule magique, il suffit de bruteforcer tous les nombres entiers entre 0 et $n$. On note cela : 
    
    $$
    u \in~ ⟦0~;~n⟧$$
    
    Dans notre exemple, on veut calculer l'inverse modulaire de $e$ modulo $\phi(p\times q)$. On fait donc
    
    $$5d \equiv 1 \mod{48} \\
    5*29\equiv 1 \mod 48 \\
    d = 29$$
    
    Et c'est fini ! On a nos clés publiques et privées. Le couple (n,e) est notre clé publique et le nombre d notre clé privée.
    

## Chiffrement d'un message

Maintenant que l'on a notre paire de clés, on peut chiffrer notre premier message.

Soit M, le message que l'on souhaite chiffrer strictement inférieur à n, on calcule C le message chiffré de la façon suivante.

$$M^{e}\equiv C \mod n$$

Exemple avec M = 42

$$42^{5}\equiv C \mod 65 \\
42^5 \equiv 22 \mod 65$$

Le message chiffré pour notre clé publique est donc 22

## Déchiffrement d'un message

Une fois notre message chiffré, on peut le déchiffrer en appliquant la formule suivante :

$$M \equiv C^d \mod n \\
M \equiv 22^{29} \mod 65 \\
M = 42$$

## Décryptage d'un message

*Petit rappel, décrypter un message consiste à déterminer le contenu du dit message sans connaitre la clé utilisée pour le chiffrer.*

Pour décrypter un message, il faut trouver l'inverse modulaire de $e$ modulo $n$ ce qui n'est pas possible sans connaître $p$ et $q$. Le seul moyen est donc bruteforcer en vérifiant pour chaque nombre qu'il est premier, mais aussi que le produit de ces deux nombres n'est pas factorisable.

# Conclusion

La robustesse de RSA se base donc sur la complexité calculatoire des algorithmes de vérification de primauté de très grands nombres. Le problème est que pour créer des clés toujours plus robustes, il faut augmenter la taille de la clé ce qui peut devenir contraignant. Afin de répondre à cette problématique, et à d'autres que nous aborderons plus tard, ont été introduites des fonctions de chiffrement asymétrique basées sur les courbes elliptiques.

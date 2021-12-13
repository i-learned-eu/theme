Author: Ramle 
Date: 2021/12/13
Keywords: réseau, sécurité, wep, wifi
Slug: wep
Summary: Pour se connecter à Internet on utilise énormément des réseaux wifi, mais mais sont-ils pour autant sécurisés correctement ? Dans cet article, je vais parler de WEP.
Title: Le fonctionnement de WEP


Pour se connecter à Internet on utilise énormément des réseaux wifi, mais sont-ils pour autant sécurisés correctement ? Dans cet article, je vais parler de WEP.

# Fonctionnement de WEP

Les prémices du wifi commencent il y a bien longtemps, dans les années nonante. La norme IEE 802.11 couvre la norme WIFI, originellement la fréquence est 2.4 GHz et la vitesse entre 1Mb/s et 2Mb/s. À l'origine il y avait 2 manières de faire, au tout début de la norme, c'était ouvert, pas de chiffrement n'importe qui pouvait se connecter à un point d'accès et lire ce qui y passait. Assez rapidement la norme WEP est arrivé, elle propose un ajout de sécurité.
WEP utilise une clé de chiffrement de 40 ou 104 bits. Pour éviter que chaque paquet utilise la même clé un vecteur d'initialisation de 24 bits est utilisé, on arrive donc à 64 ou 128 bits pour la taille de la clé, il change pour chaque trame réseau. Les paquets sont chiffrés avec RC4, le problème est que pour avoir un minimum de sécurité, il faut une clé d'une taille plus importante, on répète alors la clé d'origine 32 fois (pour une clé de 64 bits à la base) ou 16 fois (pour une clé de 128 bits). Sur base de la clé privée on va générer une "seed" pour un générateur de nombre pseudo aléatoire (PRGA), une seed c'est ce qui est utilisé comme base pour les PRGA (si on connait la seed on peut ainsi retrouver plus facilement un nombre généré). Pour chiffrer chaque message en RC4 on aura besoins d'une clé de la même taille que le message + la somme d'intégrité qui utilise du CRC32 (qui prends 4 octets). On appelle cette suite aléatoire le keystream. Une fois le keystream obtenu on fait un XOR avec les données et la clé. Mais comment les 2 machines font pour connaitre le vecteur d'initialisation me diriez-vous ?  Il est tout simplement envoyé en clair, ce qui niveau sécurité est loin d'être optimal.
En WEP un message envoyé ressemble à ça :

![Schéma frame webp](/static/img/wep/frame_wep.png)

Nous avons vu comment un échange se passe, mais comment authentifier le routeur ? Un pirate pourrait sans problème faire une attaque de l'homme du milieu pour récupérer la clé. Il y a un premier handshake, le client va dire au routeur qu'il veut se connecter, le routeur va lui répondre avec un texte que l'utilisateur devra lui répondre chiffré. Le routeur va vérifier qu'il est capable de déchiffrer les données.

# Faiblesse du WEP

Un attaquant pour essayer de casser du WEP peut analyser les trames réseaux. Le souci est que presque tout est chiffré sur base d'une clé inconnue. Résumons donc les informations visible en clair :

- Le vecteur d'initialisation
- La taille de clé

Le vecteur d'initialisation ne fait que 24 bits, la probabilité de réutilisation du même au bout d'un certain nombre de paquets est donc fort probable or comme nous l'avons vu RC4 utilise XOR, et si la même clé est utilisée plusieurs fois, il peut être plus simple de retrouver la clé. On peut donc, sur base du vecteur d'initialisation qui est visible, repérer des valeurs similaire et récupérer la clé.

WEP comme on l'a vu est très peu sécurisé, de nos jours des technologies comme WPA devrait être utilisé, nous en reparlerons d'ailleurs dans un prochain article ;) 
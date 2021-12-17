Author: Ramle 
Date: 2021/12/17
Title: VRRP
Keywords: networking, réseau, vrrp
Slug: vrrp
Summary: Comment permettre la redondance de la passerelle par défaut pour un utilisateur final ?


Il peut être très utile pour un réseau, en entreprise par exemple, d'avoir une certaine redondance. Le DNS ou SLAAC/DHCP sont des protocoles relativement simple à redonder, l'utilisateur prendra le plus rapide cependant pour la route par défaut, souvent appelé passerelle ou gateway il est rarement possible d'avoir plusieurs IPs qui répondent (pour des utilisateurs finaux du moins, pour des routeurs ou serveurs on peut utiliser de l'ECMP). Une technologie a été créée pour pallier ce problème : VRRP.

VRRP fonctionne avec plusieurs routeurs qui partagent une adresse MAC virtuelle. Chaque routeur a une priorité, celui a la priorité la plus haute est le "master".

Pour savoir le status de chaque routeur tous les membres du groupe s'échangent des paquets avec une adresse multicast, si le maitre ne répond plus le routeur avec la deuxième priorité la plus haute va prendre le relai. Leur échangent utilisent un protocole spécifique à VRRP.

Le paquet VRRP est échangé par les routeurs comme dit plus haut en multicast. L'adresse utilisée en IPv6 est `FF02:0:0:0:0:0:0:12` et  `224.0.0.18` en IPv4.

Le numéro de protocole utilisé pour VRRP est le 112, et le paquet est présenté sur la forme : 

 

![En-tête d'un paquet VRRP](/static/img/vrrp/vrrp_header.png)

Les parties importantes sont :

- Virtual RTR ID : qui est le champ qui identifie un routeur.
- Priority : La valeur peut varier de 1 à 254, c'est la priorité du routeur.
- Max Adver Int : l'interval entre 2 requêtes avant de considérer un routeur comme hors ligne.
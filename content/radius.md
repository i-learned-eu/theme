Author: Ramle 
Date: 2021/05/20
Keywords: 802.1x, networking, RADIUS, réseau, sécurité, udp
Slug: RADIUS
Summary: Une question se pose parfois, comment gérer facilement de l'authentification et des autorisations d'utilisateur sur un réseau avec plusieurs machines sans répliquer la liste d'utilisateur avec les propriétés unique à chacun sur chaque machine.
Title: Fonctionnement de RADIUS

Une question se pose parfois, comment gérer facilement de l'authentification et des autorisations d'utilisateur sur un réseau avec plusieurs machines sans répliquer la liste d'utilisateur avec les propriétés unique à chacun sur chaque machine.

Une solution pour ce genre de cas est RADIUS, c'est un protocole qui permet d'authentifier et de donner une liste de propriété pour un utilisateur.

Un cas d'usage est par exemple un stockage réseau (aussi appelé [NAS](https://fr.wikipedia.org/wiki/Serveur_de_stockage_en_r%C3%A9seau)). Le serveur [NAS](https://fr.wikipedia.org/wiki/Serveur_de_stockage_en_r%C3%A9seau) va demander l'utilisateur et le mot de passe au client, il va ensuite se connecter avec le serveur RADIUS pour valider l'authentification.

![Demande d'accès depuis le client](/static/img/client_nas_radius.png)

À chaque requête le [NAS](https://fr.wikipedia.org/wiki/Serveur_de_stockage_en_r%C3%A9seau) transmet les identifiants que le client lui a envoyé afin de savoir s'il peut accéder à la ressource demandée. Le client RADIUS (ici le [NAS](https://fr.wikipedia.org/wiki/Serveur_de_stockage_en_r%C3%A9seau)) doit s'authentifier auprès du serveur RADIUS, pour se faire il utilise un secret qui est partagé entre le serveur RADIUS et le [NAS](https://fr.wikipedia.org/wiki/Serveur_de_stockage_en_r%C3%A9seau). Ce secret permet aussi de chiffrer les identifiants de l'utilisateur via un "[xor](https://fr.wikipedia.org/wiki/Fonction_OU_exclusif)", un [xor](https://fr.wikipedia.org/wiki/Fonction_OU_exclusif) est un moyen de chiffrer sur base d'une clé unique, on parle donc de chiffrement symétrique.

La communication entre le serveur RADIUS et son client se base sur [UDP](https://blog.eban.bzh/today-i-learned/udp.html) (il peut aussi passer par [TCP](https://blog.eban.bzh/today-i-learned/tcp.html), mais nous n'en parlerons pas), le client doit donc être capable de gérer la retransmission dans le cas ou aucune réponse ne lui est accordée.

La phase d'authentification du client se base sur un paquet contenant l'utilisateur et le mot de passe. Ce paquet est nommé `Access Challenge`, il contient par exemple l'attribut `User-Name = ramle` et `User-Passsword = phrase-de-passe`. Le client reçoit ensuite une réponse du serveur, si le client RADIUS n'est pas connu du serveur il ne recevra pas de réponse. Si le client est connu alors, le serveur peut répondre de 3 manières 

- `Access-Accept` en cas d'identifiant valide
- `Access-Reject` en cas d'identifiant invalide
- `Acces-Challenge` si l'authentification requiert plus de paramètre, par exemple un code PIN ou un carte d'accès.

La réponse du serveur inclut aussi des informations supplémentaire appelé `attribut`, ce champs peut contenir des informations sur l'adresse IP qui doit être assigné à l'appareil, à la VLAN dans le quel il doit se trouver et bien d'autre paramètre.

Le paquet RADIUS se forme en plusieurs partie :

- **Code** : Il définit le type de paquet
- **Identifier** : Il identifie le paquet, ce mécanisme permet de détecter une duplication, ou de savoir à quelle demande correspond la réponse car la réponse garde le même identifiant que la demande.
- **Authenticator :** Il authentifie la demande du client ou du serveur
- **Attributes** : il permet de donner les attributs spécifiques au client

![Paquet RADIUS](/static/img/paquet_radius.png)

La partie `Authenticator` du paquet dans la requête `Access Challenge` est intéressante à étudier, cette partie ne contient que 16bits et nécessite un haut taux de confidentialité car il contient le mot de passe utilisateur. On utilise [xor](https://fr.wikipedia.org/wiki/Fonction_OU_exclusif) et le secret évoqué plus haut, dans le cas ou le password est trop long, il est alors hashé en MD5 puis transformé via un [xor](https://fr.wikipedia.org/wiki/Fonction_OU_exclusif).

RADIUS gère aussi l'itinérance, le serveur RADIUS du réseau local fera donc un proxy pour renvoyer la requête au serveur qui gère l'utilisateur. Le canal peut être sécurisé de plusieurs manières, soit un tunnel chiffré entre les 2, ou bien en sécurisant le canal avec le protocole TLS.

![Riaming Raadius](/static/img/roaming_radius.png)

J'espère que cette article vous aura plus :), on se retrouve demain pour parler de **802.1x**, un protocole utilisant RADIUS.

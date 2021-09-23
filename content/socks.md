# Socks

# Le protocol
Socks est un protocol réseau qui permet à un `client` de faire transiter ses données par un `server`.
D'après le modèle OSI, le protocole SOCKS est une couche intermédiaire entre la couche applicative et la couche transport, donc il "commencerait" couche 5 (session).  
Le client, *qu'on verra plus tard*, peut faire passer dans la socket tout protocol au dessus de la couche de transport (TCP ou UDP).
Donc, HTTP(S),  FTP(S), SSH, DNS, et j'en passe.

## Version 4
La version 4 de socks ne supporte que le protocol TCP et l'IPv4.

Il propose au client de se connecter à un server distant ou d'écouter pour une connexion entrante.

[RFC](https://www.openssh.com/txt/socks4.protocol).


### Header CONNECT et BIND

 - **Requete**

		+----+----+----+----+----+----+----+----+----+----+....+----+
		| VN | CD | DSTPORT |      DSTIP        | USERID       |NULL|
		+----+----+----+----+----+----+----+----+----+----+....+----+
           1    1      2              4           variable       1

	- `VN` est la version de SOCKS (`4`).
	- `CD` Indique le "type" de conexion:
		- `1` CONNECT
		- `2` BIND
	- `DSTPORT` Indique le port distant à contacter.
	-  `DSTIP` Indique l'IPv4 du server distant à contacter.
	-  `UERID` Peut etre tout est n'importe quoi, `tsocks` (un client socks) y met le nom d'utilisateur.
	- `NULL` Est un octet NULL `0`, il indique la fin de `USERID`
- **Reponse**

		+----+----+----+----+----+----+----+----+
		| VN | CD | DSTPORT |      DSTIP        |
		+----+----+----+----+----+----+----+----+
          1    1      2              4

	- `VN` Correspond à la version de code de réponse, il doit être mit à `0`.
	- `CD` Correspond à un code de resulats:
		- `90` : demande acceptée.
	 	- `91` : demande rejetée ou échouée.
	 	- `92` : demande rejetée car le serveur SOCKS ne peut pas se connecter à identifié sur le client.
	 	- `93` : demande rejetée car le programme client et identd signaler des identifiants différents.
	- `DSPORT` est  ignoré pour `CONNECT`, mais pour `BIND` ca correspond au port mis en écoute par le server socks.
	-  `DSTIP` est ignoré pour `CONNECT`, mais pour `BIND` ca correpond à l'ip utilisé par le server socks qui attend la connexion. 

Le type de connexion `BIND` devrait être envoyé seulement après une connexion de type `CONNECT`, ceci est utilisé par les services qui utilise le "multiple connexion", par exemple lors d'une connexion FTP en mode "active", quand le client écoute sur un port pour recevoir les données.
Cette option permet donc de ne pas créer de connexions direct entre le server et le client.

## Version 4a
La version 4a de socks est une *mini* update de la version 4 avec une bonne idée mais mal implémenté (je trouve).

Cette nouvelle version ajoute la possibilité de donner au server un nom de domaine au lieu d'une ip, et c'est le serveur socks qui doit lui même resoudre le nom de domaine.

Sur le papier c'est cool. L'implémentation c'est une autre histoire.

De ce que j'ai compris, pour envoyer un nom de domaine, il faut mettre les 3 premiers octets  du champ `DSTIP` à `0` et le 4 ème octet doit être une valeur non `NULL`.

Example:

`0.0.0.x` (x étant une valeur autre que `0`)

Cette IPv4 est bien entendu  invalide, et le server "comprend" qu'il doit lui même résoudre un nom de domaine.
> mais ... ou mettons-nous ce nom de domaine ?! *me diriez-vous.* 

On le met après l'octet `NULL` qui termine le nom d'utilisateur, et on on rajoute un octet `NULL` à la fin du nom de domaine. 

C'est fastidieux je vous l'accorde, mais heursement la version 5 de socks implémente cette idée d'une bien meilleur facon, et bien plus encore.

## Version 5
La version 5 de socks, rajoute d'autre fonctionnalité au protocol comme :

[RFC](https://datatracker.ietf.org/doc/html/rfc1928).

- Methode d'authentification.
- Support d'IPv6 
- VRAI support de nom de domaine
- Prise en charge d'UDP 

Contrairement a la  version 4 et 4a de socks, socks5 établit un "handshake" avec le serveur.
Voici comment ca se passe:

1. Le client se connecte et envoie une annonce qui inclut une liste de méthodes d'authentification qu'il supporte.
2.  Le serveur choisit l'une de ces méthodes ou envoie une erreur si aucune méthode n'est acceptable.
3. Plusieurs messages sont alors échangés selon la méthode d'authentification choisie.
4. Une fois authentifié, le client envoie une requête de connexion assez similaire du protocole SOCKS v4(a).
5. Le serveur répond d'une manière similaire à SOCKS v4.

### Header AUTH

- **Requete**

		+----+-----------+----------+
		|VER | NMETHODES | METHODES |
		+----+-----------+----------+
		| 1  |    1      |  1 à 255 |
		+----+-----------+----------+

	- `VER`, Correspond à la version socks (`5`).
	- `NMETHODES`, Correspond aux nombres de methodes d'authentifications que le client supporte.
	- `METHODES`, Correspond aux methodes d'authentifications que le client supporte.
		- `0x00`: Pas d’authentification exigée.
		- `0x01`: GSSAPI
		- `0x02`: Nom d’utilisateur/mot de passe.
		- `0x03` à `0x7F`: Alloué par l’IANA.
		- `0x80` à `0xFE`: Réservé pour des méthodes privées.
		- `0xFF`: Pas de méthode acceptable.

- **Reponse**

		+----+---------+
		|VER | METHODE |
		+----+---------+
		| 1  |   1     |
		+----+---------+
	- `VER`, Correspond à la version de socks: (`5`).
	- `METHODE`, Correspond à la methode choisi par le server socks. 		


### Header connexion
- **Request**

		+----+-----+-------+------+----------+----------+
		|VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
		+----+-----+-------+------+----------+----------+
		| 1  |  1  | X'00' |  1   | Variable |    2     |
		+----+-----+-------+------+----------+----------+
	- `VER`: Version du protocole : `5`.
	- `CMD` : Commande: 
		- `01`CONNECT.
		- `02` BIND.
		- `03`UDP ASSOCIATE.
	- `RSV`: Réservé (`0x0`).
	- `ATYP`: Type d’adresse de `DST.ADDR`:
		- `0x01`: IPv4.
		- `0x03`: Nom de domaine.
		- `0x04`: IPv6.
	- `DST.ADDR`: Adresse de destination désirée.
	- `DST.PORT`: Port de destination désiré.

- **Reponse**

		+----+-----+-------+------+----------+----------+
		|VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
		+----+-----+-------+------+----------+----------+
		| 1  |  1  | X'00' |  1   | Variable |    2     |
		+----+-----+-------+------+----------+----------+

	- `VER`: Version du protocole (`5`).
	- `REP`: Champ de réponse.
		- `0x00` Succès.
		- `0x01` Echec général du serveur SOCKS.
		- `0x02` Connexion interdite par les règles.
		- `0x03` Réseau injoignable.
		- `0x04` Hôte injoignable.
		- `0x05` Connexion refusée.
		- `0x06` TTL expiré.
		- `0x07` Commande non acceptéeo.
		- `0x08` Type d’adresse non accepté.
		- `0x09` à `FF`: Non alloué.
	- `RSV`: Réservé (`0x0`).
	- `ATYP`: Type d’adresse de l’adresse qui suit:
		- `0x01`: Adresse IPv4.
		- `0x03`: Nom de domaine.
		- `0x04` Adresse IPv6
	- `BND.ADDR`: Adresse du serveur connecté.
	- `BND.PORT`: Port du serveur connecté.

### Header UDP
 - **Requete et Reponse**

		+----+------+------+----------+----------+----------+
		|RSV | FRAG | ATYP | DST.ADDR | DST.PORT |   DATA   |
		+----+------+------+----------+----------+----------+
		| 2  |  1   |  1   | Variable |    2     | Variable |
		+----+------+------+----------+----------+----------+
	
	- `RSV`: Réservé (`0x0`).
	-  `FRAG`: Numéro de fragment actuel.
	- `ATYP`: Type d’adresse:
		- `0x01`: IPv4.
		- `0x03`: Nom de domaine.
		- `0x04`: IPv6.
	- `DST.ADDR`: Adresse de destination désirée.
	- `DST.PORT`: Port de destination désiré.
	- `DATA`: Données à envoyer.

# Le server
Le server socks c'est le server "intermediaire" qui sera entre le client et le server distant.

Il fonctionne comme suit:

![schema](static/img/socks/schema_moche.png)

Exemple (TCP):

- Le server socks accept la connexion du client.
- Il récupère l'ip/domaine et le port du server distant que le client lui envoie.
- Le server socks établie une nouvelle connexion avec le serveur distant.

De ce fait, le server socks est un proxy/intermidiaire entre le client et le server distant, donc tout ce que le client envoie au server socks, le serveur socks l'envoie au server distant, et inversement.

Pour UDP c'est la même chose, sauf qu'il n'y a pas de "connexion" approprement parler, il y'a un header precis pour UDP et le client envoie cette header la au server socks, et en cas de réponse, le server socks envoie cette header aussi au client (avec les données "réponse").

Il est aussi tout a fait possible de demander à un server socks de se connecter à un autre server socks, c'est ce qu'on appel une chaine de proxy, et c'est le principe du réseau Tor (le réseau anonyme qui aura son article dédié bientôt) qui utilise le protocol SOCKSv5 et utilise une chaine de proxy pour faire transiter les requêtes du client.

SSH permet aussi la mise en place d'un server socks, avec l'argument `-D`.

sur la machine `iusearchbtw` j'execute cette commande:

`ssh owni@socks.example.com -D 9090 -N`.

Cela ouvre  le  port `9090` sur la machine `isuearchbtw` et si j'accède à `localhost:9090` sur la dite machine, ca fera transité les données vers `socks.example.com` (qui sera utilisé comme server socks) qui fera transiter ensuite les données vers le server cible.

Il existe l'outil [microsocks](https://github.com/rofl0r/microsocks) écrit en **C** qui permet de mettre en place un server socks5 facilement.

# Le client 
Le client socks, comme son nom l'indique, c'est celui qui "sait" parler aux servers socks, c'est l'application qui se connecte au server socks et qui dis au server socks sur quel server distant se connecter.

C'est rare de trouver des clients socks comme ca "native", c'est généralement une "option" à une application. Par exemple, `curl` a une option `--socks5` permettant de passer par un server socks5.
Il existe aussi des "wrapper" socks, par exemple : `torsocks`, `tsocks` ou `proxychains-ng`, ces outils la permettent de faire passer toutes les connexions TCP et/ou UDP du programme appelant, par un server socks.

Example:

Cette commande utilisant `curl` permet de contacter `mikadmin.fr` à travers `localhost:9090` (`localhost` ayant un server socks écoutant sur le port `9090`)

`curl --socks5 localhost:9090 mikadmin.fr`.

Cette commande utilisant le wrapper `proxychains` permet d'utiliser `ncat` pour se connecter à `fibs.com` sur le port `4321` à travers un server socks.

`proxychains ncat fibs.com 4321`

*ici on ne precise pas de server socks car il est dans un fichier de cofiguration: `/etc/tsocks.conf`*

# Conclusion
- Le protocol SOCKS est un protocol permettant de contacter un server et/ou client socks.
- La derniere version du protocol SOCKS est la v5
- Le protcol socks est couche 5 du model OSI, (il est par dessus TCP/UDP).
- Un server SOCKS  se place entre le client et un server distant, il joue le role de proxy. Il envoie au server distant ce que le client envoie et inversement.

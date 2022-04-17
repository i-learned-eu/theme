lang: fr
Date: 2021/09/18
Keywords: ip, ipv4, linux, réseau
Slug: ipv4-header
Summary: Dans cet article, nous allons voir à quoi ressemble l’en-tête (header) de l’IPv4, avec son contenu et ce que fait tout ce beau monde.
Title: Comprendre l’entête IPv4
Author: Ownesis
Category: Réseau/Routage & IP

Dans cet article, nous allons voir à quoi ressemble l’en-tête (header) de l’IPv4, avec son contenu et ce que fait tout ce beau monde.

Je vous invite d'abord à aller voir [cet](https://mikadmin.fr/blog/structure-de-ladresse-ipv4/) article concernant le format d’une adresse IPv4. Même si ceci ne sera pas très utile pour cet article, c’est toujours bien de savoir de quoi on parle.

![Schema du header IPv4](/static/img/ipv4-header/Header_IP_schema.webp)

Voyons donc plus en détail les différents champs de ce header.

### **Version** `(4 bits)`

Ce champ correspond (comme son nom l’indique) à la version du protocol IP, `4` pour `ipv4`.

### **IHL** `(4 bits)`

`Internet Header Lenght` aussi appelé `IHL`, correspond au nombre de champs présents dans le header IP en les combinants par groupe de `32 bits (4 octets)`.
De base la taille du header IP est de `20 octets`, on fixe donc le champ `IHL` à `5`.
Mais la taille peut varier en fonction des `options` ajoutées au header, mais sachez que, étant donné que le champ fait `4 bits`, la valeur maximum de l’`IHL` sera de `15`, donc la taille maximum d’un header IP sera de `60 octets`.
Pour mieux comprendre j'ai fait un petit calcul, ce n'est pas forcément très règlementaire mais à ma grande surprise ça marche et ça reste cohérent.

```
(IP_Header_Length / 4) = IHL

(20 / 4) = 5
```
`20` : Taille de l'entête IP (en octets).
`4` : 32 bits = 4 octets

### **Type of Service** `(8 bits)`

(Type de Service) aussi appelé `TOS`, ce champ correspond au …*suspense*… type de service.
Je vais vous présenter 4 choix possibles, mais il y'en a bien plus, je vous laisse lire [cet](https://www.frameip.com/entete-ip/#33-8211-service) article de [frameip.com](https://www.frameip.com) ou la page 12 de la [RFC](https://tools.ietf.org/html/rfc791#section-3.1) pour plus de détails, mais sachez qu'aujourd'hui ce champ on ne l'utilise plus.
Les **4** choix “historique”:

1. **Minimize delay**

	(Délai minimum) C’est pour les applications qui envoient des petits paquets et qui ont besoin d’une réponse rapide, fissa.
	Sa valeur hexadécimale est: `0x10`.

2. **Maximize throughput**

	(Maximiser le débit) C’est tout l’inverse du premier, c’est utilisé par les applications qui envoient beaucoup de paquet.
	Sa valeur hexadécimale est: `0x08`.

3. **Maximize reliability**

	(Maximisez la fiablité) C’est pour préférer la qualité de la connexion.
	Sa valeur hexadécimale est: `0x04`

4. **Minimize monatary cost**

	(Minimisez le cout) Alors, pour celui la, apparemment, il permet de prendre le chemin qui occasionnera le moins de cout monétaire. J’ai pas connu cette époque mais si avant il fallait en plus de payer sa connexion internet de 56k, payer le trajet de son paquet ip… sacré époque.
	*En réalité je ne sais pas si ça parle pour le client ou pour le routeur du FAI ou… j’en sais rien. Si un barbu du réseau lit cet article et connait la réponse, je veux bien savoir :).*


### **Total Length** `(8 bits)`

(Taille total), ce champ correspond à la taille total du paquet.
Si on contact un serveur HTTP, le champ `Total Length` sera `Taille_IP_Header + Taille_TCP_Header + Taille_TCP_Data`.
Pour faire un exemple concret, on va envoyer une requête avec la méthode HEAD à mikadmin.fr
Header HTTP (ce qui correspond à `Taille_TCP_Data`):
```
HEAD / HTTP/1.1\r\n
Host: mikadmin.fr\r\n
\r\n
```
(Il y a 40 caractères, donc la taille de `Taille_TCP_Data` (qui, je le rappelle, est l’header HTTP) fait `40 octets`)
Un header TCP fait de base `20 octets` (mais peut varier selon les options qu’on lui donne, c'est exactement la même chose avec IP).
Maintenant avec toutes ces infos, on peut déterminer la taille totale du paquet `20 + 20 + 40` = `80`

### **Identification** `(16 bits)`

Aussi appelé `ID`, ce champ correspond à l’identification du paquet.
Quand on fragmente un paquet, on met par exemple le champ `ID` à `1` et tous les fragments du même paquet devront avoir le même `ID`, donc `1` pour cet exemple.
Pour plus d'informations je vous invite à lire cette [RFC](https://www.frameip.com/rfc-815-ip-datagram-reassembly-algorithms/).

### **Flags** `(3 bits)`

(Drapeaux) Ce champ est utilisé pour la fragmentation.
Voici les 3 bits possibles:
1. **Reservé**, ce bit est réservé, donc on le met à `0`.
2. **Don't Fragment** (Ne pas fragmenter) aussi appelé `DF`, si ce bit est à `1` le paquet ne sera **pas** fragmenté. Si il est à `0` il le sera.
3. **More Fragments** (Plusieurs fragments) aussi appelé `MF`, si ce bit est à `1` cela veut dire que ce n'est **pas** le dernier fragment, et que d'autres vont arriver. Si il est à `0` cela veut dire que c'est le dernier fragment.

### **Fragment offset** `(13 bits)`

(Position du fragment) ce champ permet d’indiquer la position de ce fragment par rapport au premier paquet.
Le premier paquet aura la valeur `0` pour le champ fragment offset et le dernier paquet aura la même valeur que `Total Length`.

### **Time To Leave** `(8 bits)`

(Durée de vie) aussi appelé `TTL`, correspond à la durée de vie du paquet, en fait, ceci correspond aux nombres de ‘sauts’ que le paquet pourra effectuer.
Pour faire simple, à chaque fois que le paquet rencontre un équipement réseau (routeur, switch de niveau 3, etc.) le `TTL` est décrémenté de `1`.
Ça sert à éviter que le paquet se balade indéfiniment sur le réseau et qu’il pose des problèmes de latence.
De base on met la valeur `255` qui est le maximum.

### **Protocol** `(8 bits)`

Ce champ correspond au protocole de transport ou autres protocoles qui suivra le header IP qu’on va utiliser (ex: TCP, UDP, ICMP) on peut trouver les numéros correspondant au protocole dans le fichier `/etc/protocols` ou le fichier header C `/usr/include/netinet/in.h`
**/etc/protocols**
```
icmp1   ICMP# internet control message protocol
tcp 6   TCP # transmission control protocol
udp 17  UDP # user datagram protocol
```

**/usr/include/netinet/in.h**

```
IPPROTO_ICMP = 1, /* Internet Control Message Protocol*/
IPPROTO_TCP = 6,  /* Transmission Control Protocol*/
IPPROTO_UDP = 17, /* User Datagram Protocol   */
```

### **Header checksum** `(16 bits)`

(Somme de contrôle du header) Permet de vérifier la validité du paquet pour éviter toutes modifications extérieures. Ce champ a pour contenu un hash.
Voici le code en **C** trouvé dans la [RFC](https://tools.ietf.org/html/rfc1071#section-4.1) pour calculer le checksum.
```c
/* Compute Internet Checksum for "count" bytes
* beginning at location "addr".
*/
register long sum = 0;

while( count > 1 )  {
/*  This is the inner loop */
sum += * (unsigned short) addr++;
count -= 2;
}
/*  Add left-over byte, if any */
if( count > 0 )
sum += * (unsigned char *) addr;
/*  Fold 32-bit sum to 16 bits */
while (sum>>16)
sum = (sum & 0xffff) + (sum >> 16);
checksum = ~sum;
```

### Source Address `(32 bits)`
(Adresse IP source) c’est l'adresse IP de l'émetteur du paquet.

### Destination Address `(32 bits)`
(Adresse IP de destination) c’est l’adresse distante, celle qu’on veut contacter.
> Attention dans le header IP, les adresses ip ne sont pas représentées sous la forme 192.168.1.2 mais en décimal : 3232235778.
Calcul:

```
192.168.1.2 = (192 * 256^3) + (168 * 256^2) + (1 * 256^1) + (1 * 256^0)
```
En C il y a les fonctions présentes dans la librairie `arpa/inet.h` pour faire ce genre de calcul et plus encore.

### **Options** `(8 bits)`

Ce champ de taille variable n’est pas obligatoire, elle permet de spécifier des options pour *pimper* notre paquet.
C’est utilisé pour le débogage ou la supervision du réseau. Je ne vais pas rentrer dans les détails car c’est pour des besoins très spécifiques et j’imagine que ce n'est plus du tout utilisé de nos jours.
Si on ajoute des `options`, il faudra donc modifier la valeur du champ `IHL`.
Pour les curieux, je vous laisse lire l’[article](https://www.frameip.com/entete-ip/#313-8211-options) de [frameip.com](https://frameip.com/) ou, pour les plus courageux, lire la [RFC](https://tools.ietf.org/html/rfc791#section-3.1).

### **Padding** `(8 bits)`

(Bourrage) ce champ permet de combler le champ `options` pour obtenir une taille de l’en-tête IP multiple de `32 bits`
Les `8 bits` sont mis à `0`.
Pour les curieux voici comment la structure du header IP est définit en C dans le noyau linux, trouvable ici `/usr/include/netinet/ip.h`.
```c
struct iphdr
  {
#if __BYTE_ORDER == __LITTLE_ENDIAN
unsigned int ihl:4;
unsigned int version:4;
#elif __BYTE_ORDER == __BIG_ENDIAN
unsigned int version:4;
unsigned int ihl:4;
#else
# error	"Please fix <bits/endian.h>"
#endif
uint8_t tos;
uint16_t tot_len;
uint16_t id;
uint16_t frag_off;
uint8_t ttl;
uint8_t protocol;
uint16_t check;
uint32_t saddr;
uint32_t daddr;
/*The options start here. */
  };
```

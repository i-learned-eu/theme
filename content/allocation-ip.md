Title: Comment sont allouées les adresses IPs
Keywords: IP, AS, ASN, AFNIC, IANA, ARIN, LACNIC, RIPE NCC, APNIC
Date: 2021-04-28
summary: Aujourd'hui on va voir comment les adresses IP sont allouées sur internet.
Slug: allocation-ips
Author: Eban

Internet est un énorme "réseau de réseaux" et comme toute grande organisation son fonctionnement est relativement complexe, aujourd'hui nous allons tenter de décrypter le fonctionnement de l'allocation d'adresse IP sur Internet 🙂. Vous commencez à avoir l'habitude, commençons par un schéma.

![Schéma allocation IP](/static/img/allocation-ip/schema-ip.png)

À la tête d'Internet, il y a une organisation, l'ICANN (Internet Corporation for Assigned Names and Numbers soit Société pour l'attribution des noms de domaine et des numéros sur Internet en français) cette entreprise américaine gère les noms de domaine et les adresses IPs via l'IANA qui est un département de cette institution. 

Les IPs sont ensuite redistribuées entre cinq organisations appelés RIRs,

- L'ARIN pour les pays d'Amérique du nord. À qui l'IANA attribue 93 /8
- Le LACNIC pour les pays d'Amérique du sud. À qui l'IANA attribue 10 /8
- L'AFRINIC pour les pays d'Afrique. À qui l'IANA attribue 42 /8
- Le RIPE NCC pour l'Europe et le Moyen-Orient? À qui l'IANA attribue 6 /8
- L'APNIC pour l'Asie et le Pacifique. À qui l'IANA attribue 51 /8

![Organisation par continent](/static/img/organisation-ip-continent.svg)

On remarque donc de grandes inégalités dans l'allocation des IPs entre les RIRs. Ces RIRs attribuent ensuite eux même des plages d'IPs à de LIRs (Local Internet Registry ou registre Internet local), nous prendrons ici l'exemple de *iFog GmbH* qui est un LIR déclaré après du RIPE NCC. Les LIRs sont des intermédiaires entre les RIR et les AS. 

Nous en venons donc à notre dernier point, les AS (Autonomous System) sont des entités identifiées par un numéro de 32 bits (ou 16 avant 2007 ou dans certains cas aujourd'hui), ces numéros sont appelés ASN (Autonomous System Number), promit c'est le dernier acronyme 😛, ce sont ces AS qui peuvent avoir des ranges d'IPs, par exemple l'AS213253 a le range `2a0c:9a40:81fb::/48` qui lui est attribué par l'intermédiare d'iFog GmbH, cette AS possède aussi `2a0e::fd45::2a00::/40` qui lui est attribué par un autre LIR : Bakker IT. 

Il faut savoir qu'un AS est couteux, pour vous donner un ordre d'idée le coût approximatif d'un AS à l'année est d'environ 4000€ en prenant en compte le transit, les IPs etc.

Merci d'avoir lu cet article qui, je l'espère vous aura éclairé sur le fonctionnement d'Internet ;) Si vous avez des questions n'hésitez pas à les formuler dans les commentaires, on se retrouve demain pour parler de DNSSEC.

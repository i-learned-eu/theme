title: IPv6, it's time to migrate
Keywords: ipv6, ipv4, ip, migration, he, cogent
Date: 2021-05-07
author: Eban
summary: December 1998 is the date of publication of the RFC 2460 introducing IPv6, today, only 26% of the most visited sites in France are accessible in IPv6 according to Arcep. So let's have a look at the IPv6 adoption in 2021.
Slug: ipv6
Translator: MorpheusH3x
Status: draft

December 1998 is the date of publication of the [RFC 2460](https://tools.ietf.org/html/rfc2460) introducing IPv6, today, only 26% of the most visited sites in France are accessible in IPv6 [according to the Arcep](https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/transition-ipv6/barometre-annuel-de-la-transition-vers-ipv6-en-france.html). So let's have a look at the adoption of IPv6.

IPv6 was created to address a simple problem, the growing lack of IPv4.

![IPv6 adoption rate in France](/static/img/ipv6/adoption_ipv6.png)

Indeed, with IPv4 the total quantity of IPs is theoretically `4 294 967 296`, theoretically because some blocks of IPs are reserved for private uses like for example 10.0.0/8. The number of 4 billion IPs may seem huge, but it only represents one IP for two people on earth, moreover many IPs are allocated (more information on IPs allocation [here](https://en.ilearned.eu.org/ips-allocation.html) 😉 ) but not used, like for example Apple which monopolizes a /8 that is to say 16 777 216 IPs which is almost not used ! With IPv6 the total number of IPs theoretically available is `340,282,366,920,938,463,374,607,431,768,211,456`, so IPv6 largely makes up for this IPv4 scarcity problem. A typical IPv6 address looks like this `2a03:7220:8083:3c00::1` it is coded on 128 bits. You are probably wondering what the `::` at the end of the address means, it is simply a padding with 0's to reach the 128 bit number. For example: `2a03:7220:8083:3c00::1` is really `2a03:7220:8083:3c00:0000:0000:0001`.  

Operators have developed several techniques to counter this growing lack of IPv4, such as CG-NAT, for those who don't know, NAT is basically the fact of sharing a single public IP between several devices (we'll talk about NAT in more detail later ;)) CG-NAT is therefore NAT but at the scale of a street, of a neighborhood. The main problem with NAT is that it prevents many applications and protocols from working, like Torrent or even Google Maps! It also prevents hosting services at home because only a range of ports is allocated to the client, so you must be lucky enough to find the range containing ports 80 and 443 to be able to self-host a website for example.

The solution to these problems is IPv6, but as we saw in the introduction, its deployment takes time, a lot of time, in its annual report Arcep pointed the finger at the slow deployment of IPv6, especially with some operators, but also with many hosts who do not provide IPv6 by default to their customers!

![Adoption of IPv6 by operators in France](/static/img/ipv6/adoption_fai.png)

One of the reasons of the slow deployment of IPv6 is the fact that users and hosts systematically pass the ball back and forth, the ones wondering what is the point of having IPv6 if all the sites they visit are available in IPv4, the others saying that it is useless to deploy IPv6 since the majority of the customers are not equipped. This dilatory attitude slows down the deployment of IPv6 to the detriment of small hosting associations that do not necessarily have the means to buy IPv4 ranges that are often very expensive. 

There is another brake, and not the least, to the deployment and the massive use of IPv6, the IPv6 network is currently divided in two, indeed, Cogent a very big provider of [transit] (https://en.wikipedia.org/wiki/Internet_transit) refuses to peer (to exchange its routes) with Hurrican Electric, another behemoth of the sector. Thus, from Cogent's IPv6 network it is impossible to access [he.net](http://he.net) (Hurrican Electric's website) in IPv6. This blocking has been going on since 2009, and despite numerous requests from Hurrican Electric, the two companies have not reached a financial agreement.

![Gateau for a reconciliation between HE and Cogent](/static/img/ipv6/gateau_he.png)

We will finish this article on this nice cake, thank you very much for reading it, if you want to know if you have IPv6 I invite you to do the test on [test-ipv6.com](https://test-ipv6.com/). If you don't have it, there is probably a way to get IPv6 from your operator 😉 except if you are with orange, no luck :'(, there are however people who offer IPv6 tunnels like [EnPLS](https://enpls.org/) for example.

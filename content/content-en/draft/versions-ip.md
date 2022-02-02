Author: Eban 
Date: 2021/07/05
Keywords: ip, ipv1, ipv2, ipv3, ipv4, ipv5, ipv6, ipv7, ipv8, ipv9, networking, réseau
Slug: versions-ip
Summary: We all know IPv4 and IPv6 which are two widely used protocols, in this article we will explore the unknown versions of the Internet protocol.
Title: The forgotten versions of the IP protocol
Translator: MorpheusH3x
Status: draft

We all know IPv4 and [IPv6](https://en.ilearned.eu.org/ipv6.html) which are two widely used protocols (although one of them is not widely used enough ^^), but we could legitimately wonder if there are other versions of the Internet Protocol, so we will make in this article a small overview of the different iterations of the IP protocol and their specificities.

# IPv1, 2 and 3 - The genesis of the Internet Protocol

The first document describing how IP works is [RFC 675](https://www.rfc-editor.org/rfc/rfc675.html) published in 1974 but presented to the International Network Working Group in 1973. If you read this RFC you will notice that it does not mention the IP protocol, but TCP, because at that time, TCP and IP were not separated and the principle of layers brought by the TCP/IP model, released in 1976, was not yet current. Talking about IPv1 is therefore an abuse of language, the appropriate term would be TCP version 1.

This protocol had an interesting particularity, it contained four address fields in its header, against two for IPv6. One for the destination (and origin) network, remember, we are in 1974 and at that time the Internet network as we know it today does not exist, there are therefore different competing networks, this field in the header aims to specify on which network the packet must transit. Thus, you can see below the different possible values for this field and thus the main networks that coexist at that time.

```
1010 = ARPANET
1011 = UCL
1100 = CYCLADES
1101 = NPL
1110 = CADC
1111 = EPSS
```

The third and fourth fields are intended to host the `TCP addresses` of origin and destination, these addresses are not very detailed in the RFC, but we know that they are 16 bits long (65 536 different addresses), they correspond more or less to what we call today `IP addresses`.

This first version of TCP is really experimental, it has not been widely deployed as IPv4 and IPv6 have been.

Then comes in 1977 the second version of TCP (and thus by extension of the Internet protocol), this version, published in the [IEN 5](https://www.rfc-editor.org/in-notes/ien/ien5.pdf), brings some improvements of which in particular the passage to a "Network Identifier", what was before called network of destination/origin, coded on 8 bits.

![List of different networks](/static/img/versions-ip/network_list.png)

Another difference is that the "host identifiers", formerly called "TCP addresses", are now coded on 24 bits, for a total of 16 777 216 addresses. We can also see the beginning of the separation between TCP and IP in this old diagram with the parts "TCP Header" and "Internet Header".

![TCP Header where we see two parts, one called "TCP Header" and the other "IP Header"](/static/img/versions-ip/header.png)

Separation which will be [acted](https://datatracker.ietf.org/doc/html/rfc760) in the version 3 of TCP, published in 1978, which represents a major advance in the evolution of the Internet protocol.

# IPv5

IPv5 did not really exist, it is in fact [Stream Protocol](https://datatracker.ietf.org/doc/html/rfc1190), abbreviated ST-II, a layer 3 protocol (like IP), created to facilitate the sending of video and audio over the Internet and which had the value 5 in the version field. It was therefore a modified version of IPv4 but had addresses coded on 32 bits, as for IPv4, which therefore did not answer the main problem posed by IPv4, the lack of addresses. This protocol marks the beginning of VoIP (Voice over IP) but it will not be deployed on a large scale, VoIP will then simply be deployed on IPv4.

# IPv7, 8 and 9 - The future? Or not...

IPv7 is a protocol called `TP/IX` released in 1993, the IP addresses are coded on 64 bits (against 128 with IPv6), we will not detail more this protocol but if you want to know more I invite you to read the [RFC](https://datatracker.ietf.org/doc/html/rfc1475) of IPv7 which is very understandable

[IPv8](https://datatracker.ietf.org/doc/html/rfc1621) (my little favorite ^^) called `PIP` and released in 1994, its operation is partly based on the [DNS](https://en.ilearned.eu.org/dns-basics.html) system, each user of the network has a `PIP ID`, a unique identifier coded on 64 bits, so, no matter where he connects to the network, it is possible to identify him only with his ID. `PIP` was therefore primarily thought to facilitate exchanges between devices changing IP address. We could for example imagine an SSH connection using only the `PIP ID` to authenticate itself and which, even if one of the two components of the connection (the client or the server) changes IP address, remains stable. I mentioned earlier the DNS, indeed, with `PIP` the DNS is modified to return both the IP address(es) and the `PIP ID`. This system has one major problem though, the `PIP ID` would allow tracking users very easily.

IPv9 finally is a very little detailed protocol, it had been [announced](http://www.china.org.cn/english/scitech/100279.htm) in great pomp by the Chinese government, this one boasting of the fact that this version of IP was adopted in the military and civil sectors, but since this effect of announcement no technical specification was published, only rumours that the addresses would be coded on 256 bits and composed only of numerical characters (and not hexadecimal as it is the case of IPv6)


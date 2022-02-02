Author: Eban 
Date: 2021/08/03
Keywords: réseau, sécurité
Slug: ip-v4-mapped
Summary: About twenty years ago, a system was set up on some machines allowing to have IPv6 addresses mapping an IPv4 address. This principle may seem like a good idea, but it actually represents a major vulnerability.
Title: The threat of IPv4 mapped to IPv6
Translator: MorpheusH3x
Status: draft

About 20 years ago, a system was set up on some machines to have IPv6 addresses mapping an IPv4 address, the goal was to have only one [socket](https://fr.wikipedia.org/wiki/Berkeley_sockets) (which is basically an intermediary between the physical network interfaces and the software accessing the network) listening only in IPv6 but accepting mapped IPv4 addresses. These IPv6 addresses have the first 80 bits as zeros, the next 16 as `f`, and the last 32 bits as an IPv4 address. `:ffff:0a00:0001` is the IPv6 address corresponding to the address `10.0.0.1`, it can also be written as `::ffff:10.0.0.1`. If you want to calculate a mapped IPv4 address, you can use [this site](http://www.gestioip.net/cgi-bin/subnet_calculator.cgi), we will use the writing `::ffff:10.0.0.1` for the rest of this article.

This may seem like a good way to transition to a massive IPv6 deployment, but mapped IPv4 addresses are a real threat, because when a program receives an IPv4 address it has no way of knowing if that IP address was mapped to an IPv6 or if it is a *real* IPv4 address, so if an attacker sends a request with an IPv6 address `::ffff:127. 0.0.1` for example, this could be interpreted as the loopback IPv4 address `127.0.0.1` and thus allow the attacker to access certain software that would give certain permissions in their ACL to the IP address `127.0.0.1`.

![Diagram describing a typical attack using a mapped IPv4 address](/static/img/v4_mapped/ip_v4_attack.png)

[The document](https://datatracker.ietf.org/doc/html/draft-itojun-v6ops-v4mapped-harmful) that details these security issues simply recommends banning mapped IPv4 addresses, but unfortunately this is not yet the case on many recent systems, with the exception of NetBSD, OpenBSD and FreeBSD.

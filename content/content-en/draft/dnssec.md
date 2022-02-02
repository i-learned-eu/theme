Title: How does DNSSEC works?
Keywords: DNSSEC, DNS, sécurité, DS, NSEC, RSSIG, KSK, ZSK
Date: 2021-04-29
author: Ramle
summary: Today, we are going to talk about how DNSSEC works and see the different risks that this mechanism solves or not.
slug: dnssec
status: draft

Small reminder: this blog has an [RSS feed](https://ilearned.eu.org/rss.xml), feel free to add it to your favorite RSS feed reader :)

Yesterday we saw how to secure the connection between a slave server and a master server, but the problem of authenticity of the answers still arises, to begin with the traffic between the authoritative server and the resolver is not encrypted, any attacker who practices a [`MITM`](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) type attack can therefore modify the answers. The channel is not the only problem, especially since it is already possible to secure the channel between resolver and authoritative server, and between resolver and client via `DoT` (DNS over TLS) and `DoH` (DNS over HTTPS), we'll talk more about that tomorrow ;). Securing the channel if the server is corrupted does not help much, that's why `DNSSEC` (`RFC 4033`) was invented.

![DNSSEC risk diagram](/static/img/dns-basics/schema_risk_without_dnssec.png)

DNSSEC is a way to cryptographically sign a DNS zone based on an asymmetric key system, an asymmetric key system relies on 2 keys, a private one which is kept preciously and which is used to sign or decrypt data and a public one which is used to verify or encrypt data. In DNSSEC, encryption is not used, so the private key is only used to sign. 

To do this, two key pairs are generally used: the `KSK` (key-signing key) and the `ZSK` (zone-signing key). The KSK is only there for the signature of the ZSK, it is given a longer life span than the ZSK and it can be stored and generated offline to increase its security, the advantage of this system is to be able to keep the same key longer without adding too much risk of leakage since it is stored offline, in a secure place. The ZSK is used to sign the zone, so it must be present on the machine that generates the zone, it is changed more often to avoid the risk of leakage. The slave servers do not need either of the two keys, they receive the signed zone directly, so changing the zone on their part is no longer possible if the resolver checks with DNSSEC.

DNSSEC does not sign the entire zone, but signs each record independently, the signature is contained in the `RSSIG` record. This poses a problem if it allows you to sign a DNS entry, how do you prove that a record does not exist? To solve this problem the record of type `NSEC` exists.

NSEC is a way to prove the non-existence (symbolized by the return code `NXDOMAIN`) of a record by giving the next (alphabetically) record of the zone, a problem of confidentiality arises with this method, it is indeed very simple to enumerate the list of record. To prevent this kind of attack NSEC3 was born, instead of giving the FQDN we return only the condensate, enumeration becomes impossible.

A last problem, and not the least, exists, how to exchange reliably the keys on a large scale? We cannot give them to each other from person to person, it is unmanageable considering the number of zones present on the Internet. To solve this problem two records exist: DS and DNSKEY.

Let's start with DNSKEY, it allows to register the public key that signs the zone, this registration is stored in the zone itself.

With only DNSKEY you can't validate the zone correctly, the reliability of the chain is not guaranteed, it slaves could modify this record to modify the zone as you wish, to verify this there is a DS record that is located in the parent zone and allows you to make a reference to the public key used to sign the FQDN zone, it's the registrar that takes care of placing this record. As for the `.` zone, it is impossible to define a DS record above it, because it is the lowest zone, so the IANA gives the key used and it is available here: [https://www.iana.org/dnssec/files](https://www.iana.org/dnssec/files).

![DNSSEC schema](/static/img/dns-basics/schema_functional_DNSSEC.png)

That's all for this article, I hope it will be more useful for you. If you have any comments or questions don't hesitate to comment.

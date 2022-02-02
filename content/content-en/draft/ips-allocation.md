Title: How are IP addresses allocated
Keywords: IP, AS, ASN, AFNIC, IANA, ARIN, LACNIC, RIPE NCC, APNIC
Date: 2021-04-28
summary: Today we will see how IP addresses are allocated on the Internet.
Slug: ips-allocation
Author: Eban
status: draft

Internet is a huge "network of networks" and like any large organization its operation is relatively complex, today we will try to decipher how IP address allocation works on the Internet 🙂. You are getting used to it, let's start with a diagram.

![IP allocation schema](/static/img/allocation-ip/schema-ip.png)

At the head of the Internet, there is an organization, the ICANN (Internet Corporation for Assigned Names and Numbers) this American company manages the domain names and IP addresses via the IANA which is a department of this institution. 

The IPs are then redistributed between five organizations called RIRs,

- The ARIN for the North American countries. To whom IANA allocates 93 /8
- LACNIC for South American countries. To which IANA assigns 10 /8
- The AFRINIC for the African countries. To which IANA assigns 42 /8
- RIPE NCC for Europe and the Middle East? To whom IANA assigns 6 /8
- APNIC for Asia and the Pacific. To whom IANA assigns 51 /8

![Organization by continent](/static/img/allocation-ip/organization-ip-continent.svg)

We can see great inequalities in the allocation of IPs between RIRs. These RIRs allocate then themselves IPs ranges to LIRs (Local Internet Registry), we will take here the example of *iFog GmbH* which is a LIR declared after the RIPE NCC. LIRs are intermediaries between RIRs and SAs. 

So we come to our last point, AS (Autonomous System) are entities identified by a number of 32 bits (or 16 before 2007 or in some cases today), these numbers are called ASN (Autonomous System Number), promit it's the last acronym 😛, it's these AS that can have ranges of IPs, for example AS213253 has the range `2a0c: 9a40:81fb::/48` which is assigned to it through iFog GmbH, this AS also has `2a0e::fd45::2a00::/40` which is assigned to it by another LIR: Bakker IT. 

You should know that an AS is expensive, to give you an idea the approximate cost of an AS per year is about 4000€ taking into account the transit, IPs etc.

Thank you for reading this article which I hope will have enlightened you on how the Internet works ;) If you have any questions, don't hesitate to ask them in the comments.

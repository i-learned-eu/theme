title: How DNS over TLS and DNS over HTTPS works ?
Keywords: DoT, DNS, DoH, sécurité, TLS, HTTPS, DNS over HTTPS, DNS over TLS, vie privée, privacy
Date: 2021-04-30
author: Ramle
summary: In today's article we will see how DNS over TLS and DNS over HTTPS work.
Slug: dot-doh
Status: draft

In the [article on how does DNSSEC works](https://en.ilearned.eu.org/dnssec.html), the problem of authenticity of DNS server responses was mentioned. We have seen the solution: DNSSEC but this mechanism only signs the requests to prevent modification, it does not prevent passive spying on the requests. The risk of eavesdropping requires securing the channel, two solutions have been chosen: `DoT` and `DoH`.

DoT is the acronym of DNS over TLS, this protocol is quite "simple" if we omit the explanation of TLS which will be seen soon, it is DNS which passes by an encrypted channel via TLS. We use TCP on port 853.

A concern arises, TLS is often based, as in the world of the web with HTTPS for example, on certification authorities (abbreviated CA) which in theory ensures to deliver certificates that they have signed to prove the legitimacy, but in reality this system is quite unreliable, it is indeed not uncommon to see an authority deliver by mistake or even intentionally corrupted certificates, which should not have been issued, moreover, historically a certificate is quite expensive, even if nowadays some organizations like [Let's Encrypt](https://letsencrypt.org/) deliver a TLS certificate for free.

To do without a CA several solutions exist, the simplest is simply not to verify the certificate, this protects from a "passive" attacker but it remains relatively easy to replace the certificate when stolen. To prevent this case we can do key pinning, this principle is based on a condensate of the certificate which is then put in base64, the software can then compare the remote certificate with the key it has locally if a hacker performs a man-in-the-middle attack (MITM) and replaces the certificate in the middle of the road the client will realize the subterfuge.

![SSL pining](/static/img/dns/ssl-pining.png)

![SSL pining bad certificate](/static/img/dns/ssl-pining-fail.png)

A last problem in DoT exists, a firewall can easily prevent it from working, in the context of a captive portal for example often only HTTP traffic is allowed. A solution to overcome this problem exists: DNS over HTTPS (DoH).

DoH allows like DoT to encrypt the communication channel, but by passing through HTTPS the advantage is that it is difficult to block, indeed blocking HTTPS would block at the same time a large number of websites. The operation remains centered on the principle of HTTP, the advantage of HTTP is the control of the cache directly on the client with the header `Cache-Control: max-age=X` (where X is the time in second). As for DoT several choices exist for the validity of the certificate, these are the same choices that are offered to us. As for the return codes of the DNS, they are in the body of the message, and not in the form of HTTP code, of course the classic HTTP codes are always applied.

These two methods can cause problems in some cases, indeed, it is in many cases required to use a program that "translates" from DoH or DoT to the DNS protocol directly. An example of such a program is `stubby` under Linux.

![Proxy DoH/DoT](/static/img/dns/proxy-dot-doh.png)

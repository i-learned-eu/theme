title: DANE and TLSA - Preventing fraudulent TLS certificates
Keywords: dane, tlsa, ca, fake ca
Date: 2021-05-01
author: Eban
summary: Today we will study the DANE protocol, this protocol was created to answer a simple problem, how to guarantee the authenticity of a TLS certificate?
Slug: dane
Status: draft

Today we are going to study the DANE protocol, this protocol was created to answer a simple problem, how to guarantee the authenticity of a TLS certificate if the [CA](https://en.wikipedia.org/wiki/Certificate_authority) is corrupted and delivers a certificate to, for example, an intelligence service so that it can intercept and decrypt users' requests? This example is not taken by chance, [a similar case](https://security.googleblog.com/2013/12/further-improving-digital-certificate.html) happened in 2013 where the ANSSI had issued certificates for Google domains, probably for intelligence purposes. RFC 6698](https://tools.ietf.org/html/rfc6698) therefore introduces the DANE (DNS Authentication of Named Entities) standard and the DNS record `TLSA'. The principle is simple, add a record in the DNS zone which contains a condensate of the real TLS certificate, this method is very similar to TLS Pinning, mentioned in this [article](https://en.ilearned.eu.org/dot-doh.html) but has the specificity of placing the condensate at the DNS level.

Here is an example of a record for `blog.eban.bzh` (former blog domain):

```

_443._tcp.blog.eban.bzh. 10800	IN	TLSA	3 1 1 D7DF5F6E8325454CF25B711D7FCB22CD639C4F26514E5473EC73C59353C16F0D

```

So we see that we have to specify in the record the port (here, 443), the protocol used (here TCP, by the way, stay tuned in the next few days an article about this protocol might come out) then the domain to which it applies, the three following numbers `3 1 1` correspond respectively, to the usefulness of the framework of use of this record, here `DANE-EE: Domain Issued Certificate` a given certificate for a domain name. The next `1` indicates the type of certificate hashed, `0` corresponding to a [fullchain certificate](https://en.wikipedia.org/wiki/Chain_of_trust) and `1` to the public key only, the last `1` finally corresponds to the hashing function used, here [SHA-256](https://en.wikipedia.org/wiki/SHA-2). Once this certificate is set up, the browser should, in principle, compare this hash with a hash it would generate on its own, in principle because DANE is not present in [any public browser](https://bugzilla.mozilla.org/show_bug.cgi?id=1479423). There is however the [DNSSEC/DANE Validator](https://addons.mozilla.org/en-US/firefox/addon/dnssec-dane-validator) module for firefox and [TLSA Validator](https://chrome.google.com/webstore/detail/tlsa-validator/gmgeefghnadlmkpbjfamblomkoknhjga) for chromium and derivatives. To summarize the functioning of DANE, here is a small diagram.

![Authentic TLS certificate](/static/img/dane/authentic_TLS_certificate.png)

![Rogue TLS certificate](/static/img/dane/rogue_LS_certificate.png)

Title: Gemini, a viable alternative to HTTP?
Keywords: gemini, privacy, http
Date: 2021-05-06
author: Eban
summary: Hey, today we are talking about the Gemini protocol, an alternative protocol to HTTP ;)
Slug: gemini
Status: draft

Hey, today we're talking about the Gemini protocol, Gemini is an alternative protocol to HTTP or Gopher to name a few, created in June 2019 with the aim of being much lighter than HTTP, and to better respect the privacy of users, indeed, with Gemini, no JS, cookies or eTag, user tracking is almost impossible. Gemini was not created to compete with HTTP but to offer a lighter and more secure alternative to users. This protocol includes the TLS protocol, so unlike HTTP, there is no possibility of having unencrypted communications. This protocol is partly based on HTTP 0.9 and is essentially textual, but images can also be integrated. 

A Gemini request is very simple, the client asks for a file on the target server, the server answers with an error code (here, 20 = OK), the type of file, most often `text/gemini` and finally sends the file. This is simpler than TCP the day before yesterday, isn't it?
So here's a standard request on Gemini. `C` represents the client and `S` the server.

```
C: gemini://gemini.circumlunar.space/docs/faq.gmi
S: 20 text/gemini
S: # Hey !
S: This is a website running under Gemini :D
```

I purposely left out the whole TLS part in the above example request because TLS will be the subject of a more complete article in a short while.

In order to be independent of external CAs which, [as we have seen](https://en.ilearned.eu.org/dane.html) are a SPOF (single point of failure) which, if compromised, could deliver fraudulent certificates Gemini relies on the TOFU principle, Trust on first use, it is a mechanism also used by SSH for example, to trust a certificate, the software simply relies on the certificate it has encountered for the first time on this site. This way of working is decried by some who prefer to work with CA. However, mechanisms like [DANE](https://en.ilearned.eu.org/dane.html) coupled with [DNSSEC](https://en.ilearned.eu.org/dnssec.html) exist and allow to make Gemini relatively secure.

For this post, I made my blog available on Gemini, I invite you to have a look at `gemini://eban.bzh` you will find [here](https://gemini.circumlunar.space/clients.html) a list of Gemini clients.

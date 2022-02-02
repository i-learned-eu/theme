title: How does HTTP work?
summary: Nowadays the web is widely used, a protocol is behind this success: HTTP
slug: http
Keywords: HTTPS, HTTP, web, internet
Date: 2021-05-08
author: Ramle
Translator: MorpheusH3x
Status: draft

The web is the most famous use of the internet, a rather old protocol (but not as old as the internet) is behind this success: HTTP.

HTTP is the acronym of Hyper Text Transfer Protocol, it was invented to overcome some shortcomings of FTP which at the time was the majority, one of the main points is the notion of data format, that is to say to indicate to the client what is the type of data, this allows the client to be able to interpret and display without asking the user what he must do with each file. This notion of "data format" is called MIME.

![MIME Scheme](/static/img/http/mime.png)

HTTP has known several versions, the initial one being 0.9 (noted HTTP/0.9) which has never been standardized in an RFC, an RFC (for request for comment) is a technical document identified by a number defining procedures or protocols, these documents are accessible on [https://www. rfc-editor.org/rfc/](https://www.rfc-editor.org/rfc/) (or gemini://gemini.bortzmeyer.org/rfc-mirror/rfc-index.gmi via [Gemini](https://en.ilearned.eu.org/gemini.html)), the use of this version of HTTP is quite marginal nowadays. A few years later is released through an RFC (the [1945](https://www.rfc-editor.org/rfc/rfc1945.html)) HTTP/1.0 this RFC is mainly concerned with specifying how HTTP works, it does not bring any evolution with version 0.9. Quite quickly HTTP/1.1 is released, this version brings some optimizations, like sending several requests simultaneously.

HTTP is based on the [TCP protocol] (https://en.ilearned.eu.org/tcp.html), by default the port used is 80. To request or send contents we use "methods", a method is a command sent to the server. We can quote several of them:

- GET : Request a resource
- HEAD : Request only the information
- POST : Send data

The list is not complete, I let you search by yourself for more information about this ;)

We can look deeper into HTTP by looking at the network transmissions:
![HTTP network capture diagram](/static/img/http/capture_http.png)
The data part, the one which contains the page itself is not directly visible here, I let you look at the network dump on wireshark, it is available [here](/static/misc/http.pcap).


Another interesting aspect of HTTP are the headers that give information to the client about the server, and vice versa. On the client side for example, we have the "Host" header which gives the domain name requested by the client, this allows to distribute a different content depending on it. The server can give the type of content via "Content-Type". There are many other possible headers, if you want to look at the one for a URL the `curl` command allows this via the `-I` option, for example for [https://ramle.be](https://ramle.be) :

```bash
% curl -I https://ramle.be
HTTP/2 200 
server: nginx
date: Sat, 08 May 2021 14:40:55 GMT
content-type: text/html; charset=utf-8
content-length: 1992
last-modified: Fri, 23 Apr 2021 18:18:34 GMT
vary: Accept-Encoding
etag: "60830f7a-7c8"
content-security-policy: default-src 'none'; style-src cdn.ramle.be; img-src cdn.ramle.be
x-frame-options: SAMEORIGIN
x-xss-protection: 1; mode=block
x-content-type-options: nosniff
referrer-policy: same-origin
x-permitted-cross-domain-policies: master-only
expect-ct: max-age=60, enforce
permissions-policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()
strict-transport-security: max-age=31536000; includeSubDomains; preload
accept-ranges: bytes
```

We notice on the first line the version of HTTP, here it is the version 2. We see then the list of headers:

- content-type** indicates the content type (the [MIME](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types))
- etag** indicates a sequence of ASCII characters, this string changes if the remote content changes, this allows to cache the resources. There is no defined method for generating this string.

I have only described here the headers that I thought were important for this article, many other headers are still very useful but less used, often security oriented, some of them will surely be the subject of a future article ;). If you want more precise information on this one I let you go and see the MDN documentation which is quite complete.

I quoted above the version 2 of HTTP (noted HTTP/2) without explaining the changes brought by this version, so in this paragraph we will see the differences with HTTP/1.1, to begin with the implementation made by many browsers imposes the encryption via HTTPS (we will talk again below about HTTPS), another change is in the transport itself, HTTP/1.1 is based on text, where HTTP/2 uses binary, it makes it more compact and easy to parse, but not readable by a human without specific tool. There is also a change in the TCP connection itself, instead of making one [TCP](https://en.ilearned.eu.org/tcp.html) connection per resource, we use a single connection for all the resources, the latency gain is quite important considering the number of [TCP](https://en.ilearned.eu.org/tcp.html) round trips.

![HTTP/2 vs HTTP/1.1 scheme](/static/img/http/http2.png):

You have probably noticed that HTTP has almost no basic security mechanism, it is indeed not possible to verify the authenticity of the resources nor to prevent an attacker from spying on the connection, to solve this problem HTTPS was born, it is simply a matter of passing HTTP via TLS, for verification we rely on certification authorities, unlike other protocols such as [Gemini](https://en.ilearned.eu.org/gemini.html), I invite you to go and see the article on [DANE](https://en.ilearned.eu.org/dane.html) for more details about the certification authorities 

HTTP allows to reduce the size of the sent data by compressing them, the two algorithms used to compress the data are gzip and brotli, the client can tell the server which of these algorithms it supports via the "**Accept-encoding**" header.

That's all for today's article, I hope you'll like it :), See you tomorrow to talk about **radvd**.

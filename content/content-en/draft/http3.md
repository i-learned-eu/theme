Author: Ramle 
Date: 2021-05-18
Keywords: HTTP, http3, QUIC
Slug: http3
Title: How does HTTP/3 work?
Summary: In today's article we will see how HTTP/3 and QUIC work.
Translator: MorpheusH3x
Status: draft

Not long ago we discovered how [HTTP](https://en.ilearned.eu.org/http.html) works, and different versions of this protocol, but one of them has not been seen: HTTP/3, this version brings a change on the transport method based on QUIC which itself uses [UDP](https://en.ilearned.eu.org/udp.html) instead of [TCP](https://en.ilearned.eu.org/tcp.html).

To start, let's take a closer look at QUIC, there are currently two versions of this protocol, one made by Google that has not been standardized, and one that is being written to be published as an RFC at the IETF (the body that handles the publication of RFCs). The Google version focuses on HTTP/3, unlike the IETF version which wants to make QUIC a transport protocol for other uses than [HTTP](https://en.ilearned.eu.org/http.html), for [DNS](https://en.ilearned.eu.org/les-bases-du-dns.html) for example.

At the moment the IETF (which is based in part on Google's work) is still in the drafting stage of the standard and is focusing on HTTP/3 as the use for the first version. This article will be based on the IETF's work, not Google's.

To start, QUIC is based on [UDP](https://en.ilearned.eu.org/udp.html) and wants to solve some problems of [TCP](https://en.ilearned.eu.org/tcp.html), with HTTP/2 for example, several transfers are done on a single [TCP](https://en.ilearned.eu.org/tcp.html) flow, I refer you to the article on [HTTP](https://en.ilearned.eu.org/http.html) which explains in detail this concept, with [TCP](https://en.ilearned.eu.org/tcp.html) if in the list of packets waiting a packet is lost all the packets before the lost one will have to wait for the return. We can make a parallel with a car traffic jam, if a car blocks the road, the ones before the car will have to wait for it to pass.

![Packet congestion](/static/img/http/congestion_http.png)

TCP also adds significant latency due to different handshakes, [UDP](https://en.ilearned.eu.org/udp.html) does not use a handshake sequence. QUIC adds some to ensure a minimum of reliability. There are a total of 4 round trips to retrieve a page (or an error code) compared to 6 in the [TCP](https://en.ilearned.eu.org/tcp.html) based versions of HTTP. The client starts by sending a "hello" to give different parameters about itself, then the server responds by sending directly the certificate and information to start the data exchange, the client then sends its request with the method. The client finally answers with the return code or the requested page.

![Comparison handshake HTTP vs HTTP/3](/static/img/http/http_handshake_vs.png)

QUIC works on [UDP](https://en.ilearned.eu.org/udp.html) as said above, it forces a certain level of security by imposing TLS in version 1.3, for the communications. It also offers a certain reliability that UDP does not have, remember, [UDP](https://en.ilearned.eu.org/udp.html) does not check anything. QUIC solves this problem by adding a layer which allows to manage a retransmission of packet in case this one would be lost on the way, it also allows a control of the congestion, the congestion in network it is the saturation of the network in itself, that causes a slowdown or a loss of packet in the extreme cases, the protocol is thus not far from [TCP](https://en.ilearned.eu.org/tcp.html) on the reliability.

On a single channel [UDP](https://en.ilearned.eu.org/udp.html), QUIC allows to place several flows simultaneously.

![QUIC channel](/static/img/http3/quic.png)

For the moment, we have seen mainly QUIC, the reason is that HTTP/3 does not bring much, it is HTTP/2 adapted to go over QUIC, there are some minor differences like the compression of the headers which is adapted to the protocol, but the modifications are minor and come especially adapted [HTTP](https://en.ilearned.eu.org/http.html) for QUIC. The connection with HTTP/2 is rather logical if we look at the chronology the work on HTTP/3 started in the same period.

HTTP/3 layer](/static/img/http/couche_http3.png)

A useful point to address is how the client knows whether it should communicate in HTTP/3 or not. Older versions of HTTP use [TCP](https://en.ilearned.eu.org/tcp.html), while HTTP/3 uses [UDP](https://en.ilearned.eu.org/udp.html). To inform the browser of the presence of HTTP/3 the `Alt-Svc` header has been created, it indicates the [UDP](https://en.ilearned.eu.org/udp.html) port on which the client must go to see, one can also via the header indicate a different domain.

The improvement that HTTP/3 brings is relatively minor but is quite useful, on a stable connection with little packet loss the difference is not necessarily visible, but on a saturated network with a large number of losses not to send back the whole queue at each loss is a significant gain. An observation made by some is that HTTP/3 requires more CPU for the server, it can be a brake for the deployment. It is also important to keep in mind that QUIC is quite new, the implementations are not yet perfect, time will tell if this protocol is worth it or not.

In terms of performance, HTTP/3 brings a gain in latency thanks to the reduced handshake, in terms of loading speed, the prioritization of streams, and the possibility to send on several streams simultaneously allows to gain a little. According to [Cloudflare](https://blog.cloudflare.com/http-3-vs-http-2/) HTTP/3 improves the time to first connection by 12.4%, as for the loading of a page, here their own blog, the time decreases between 1 and 4%, it is ultimately quite small, but on a slow connection a few percent is not negligible.

If you look a little bit in detail at your browser you will notice that HTTP/3 is not yet activated by default, indeed this protocol although promising is not yet standardized and is very minority. If by curiosity you still want to activate in `about:config` on your firefox you can change the configuration `network.http.http3.enabled` to `true`. However, you should know that sites like Cloudflare or Google already integrate HTTP/3! 

I hope this article will be more interesting for you :), see you tomorrow to talk about **radius.**

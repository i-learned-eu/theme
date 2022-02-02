Author: Eban 
Date: 2021/05/30
Keywords: réseau, sécurité, tls
Slug: tls
Summary: TLS is a protocol that we use on a daily basis, it is notably used in HTTPS to secure the connection, let's explore the mechanism of this particular protocol.
Title: How does the TLS protocol work
Translator: MorpheusH3x
Status: draft

TLS is a protocol we use every day, it is used in `HTTPS` to secure the connection. TLS is the successor of SSL, we will see shortly why SSL was abandoned in favor of TLS. In this article, we will study TLS1.3 which is the latest version of the protocol released in 2018. TLS is based on both asymmetric and symmetric encryption. A key exchange (called handshake) takes place at the beginning of the connection, a secret key is exchanged asymmetrically, this key is then used to encrypt the data (symmetric encryption). Let's see in more detail how a handshake with TLS1.3 works. 

![Diagram of a TLS1.3 handshake](/static/img/tls/handshake.png)

The client sends a `**Client Hello**` which contains among other things :

- The different cryptographic protocols (for asymmetric and symmetric encryption) that it supports.
- Key Share` which corresponds to the client's public key, you may wonder how the client can send its public key if it doesn't know which protocols the server supports, this is a major difference compared to TLS 1.2, with TLS 1.3 the client assumes that the server supports a certain number of protocols and sends its public key for one of these protocols, if it turns out that it doesn't, the server will send back a `HelloRetryRequest` as well as the protocols that it supports.

The server then replies with a `**Server Hello**` which contains among other things:

- The TLS Certificate which ensures the authenticity of the server.
- The `Certificate Verify` which corresponds to the signature of the handshake, it is used to ensure that the handshake has not been modified en route (in the case of a [Man In The Middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) for example).
- `Change Cipher Spec` tells the other participant to switch to a symmetric cipher mode.
- In `Key Share` the server indicates its public key
- `Finished` indicates the end of the handshake for the client.

The client finally sends a `Change Cipher Spec` and `Finished`. You will find [here](/static/misc/tls/tls_1_3.pcapng) a pcap of a request with TLS 1.3.

By browsing you will see that the version of TLS displayed is TLS 1.2, *it's not a bug, it's a feature* it's actually to avoid that some middleboxes <s>shit 😡</s>, used in particular in company to spy on the traffic, block the traffic for version of TLS above TLS 1.2.

Public/private key pairs are derived from a secret key in order to symmetrically encrypt exchanges. We will soon detail this operation through ECDH.

You will surely have noticed that the domain name is in clear in the requests, basically a feature called ESNI (Encrypted Server Name Indication) which allows to encrypt the domain name in the requests should have been implemented in TLS 1.3 but it is not yet the case, ESNI is only in the state of [draft](https://www.ietf.org/archive/id/draft-ietf-tls-esni-10.html)... 😕

Another important feature in TLS 1.3 is the 0 RTT, it is a very controversial feature because it does not respect the `forward-secrecy` principle, if an attacker manages to find the key used for symmetric encryption, he will be able to decrypt all the next requests. It consists, to make it simple, in keeping the same symmetric key for several exchanges in order to resume an exchange without having to make a handshake, but this functionality is a false good idea...

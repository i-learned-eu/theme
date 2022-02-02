Author: Eban
Date: 2021/12/10
Keywords: mail
Slug: pop3
Summary: Nous avons vu dans une série de trois précédents articles le protocole SMTP et tous (ou presque 😉) les processus autour de l'envoi de mails. Maintenant qu'on sait envoyer des mails, ce serait intéressant de pouvoir les lire n'est-ce pas ? 😄 Cet article s'intéressera au protocole POP3 qui a été conçu à cet effet, un autre sera dédié à IMAP.
Title: Comment fonctionne POP3 ?

Nous avons vu dans une série de trois précédents articles [¹](https://ilearned.eu/smtp.html) [²](https://ilearned.eu/secu_smtp.html) [³](https://ilearned.eu/spoofing_email.html) le protocole SMTP et tous (ou presque 😉) les processus autour de l'envoi de mails. Maintenant qu'on sait envoyer des mails, ce serait intéressant de pouvoir les lire n'est-ce pas ? 😄 Cet article s'intéressera au protocole POP3 qui a été conçu à cet effet, un autre sera dédié à IMAP.

POP3 (Post Office Protocol version 3) tout comme SMTP, POP3 est une protocole plutôt simple. 

Un échange typique ressemble à cela :

```
S: <wait for connection on TCP port 110>
C: <open connection>
S:    +OK POP3 server ready <1896.697170952@dbc.mtview.ca.us>
C:    APOP mrose 682949bee6805d9b611b82395e342cad
S:    +OK mrose's maildrop has 2 messages (320 octets)
C:    STAT
S:    +OK 2 320
C:    LIST
S:    +OK 2 messages (320 octets)
S:    1 120
S:    2 200
S:    .
C:    RETR 1
S:    +OK 120 octets
S:    <the POP3 server sends message 1>
S:    .
C:    DELE 1
S:    +OK message 1 deleted
C:    RETR 2
S:    +OK 200 octets
S:    <the POP3 server sends message 2>
S:    .
C:    DELE 2
S:    +OK message 2 deleted
C:    QUIT
S:    +OK dewey POP3 server signing off (maildrop empty)
C:  <close connection>
S:  <wait for next connection>
```

Détaillons les différentes commandes utilisées ici :

- APOP : permet au client de s'authentifier, il est composé du nom d'utilisateur (ici mrose) ainsi que du hash d'un timestamp ainsi que d'un mot de passe, il correspond ici à `<1896.697170952@dbc.mtview.ca.us>mrosepass`.
- STAT : indique le nombre de message et leur taille
- LIST : liste les différents messages en indiquant leur taille et leur ID
- RETR : permet de télécharger un mail en précisant son ID
- DELE : permet de supprimer un mail en précisant son ID
- QUIT : ferme la session

Comme vous pouvez le voir, à l'instar de SMTP, POP3 est un protocole vraiment simple dans son fonctionnement. Afin d'ajouter une couche de sécurité supplémentaire, supporte STARTTLS, mais tout comme avec SMTP, STARTTLS pose un problème, il est dit "opportuniste". Ceci signifie que quand STARTTLS est présent, il ne rend pas obligatoire l'utilisation de TLS. 

La simplicité de POP3 est à la fois une force, et une tare, une force en ce qu'elle permet aux implémentations de ce protocole d'être légères, et une tare car ce protocole ne correspond pas aux besoin des utilisateurs une utilisation plus poussées des mail, cette simplicité apporte aussi un niveau de sécurité critiquable. Au vu de ces éléments un protocole alternatif a été créé, IMAP, que nous verrons de plus près dans un prochain article.
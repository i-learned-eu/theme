lang: fr
Author: Eban
Date: 2021/12/12
Keywords: mail
Slug: imap
Summary: Dans un précédent article, nous avions étudié le fonctionnement du protocole POP3. Cet article sera dédié à un protocole alternatif à POP3, IMAP.
Title: Comment fonctionne le protocole IMAP ?
Category: Réseau/Mail

Dans [un précédent article](https://ilearned.eu/smtp.html), nous avions étudié le fonctionnement du protocole POP3. Cet article sera dédié à un protocole alternatif à POP3, IMAP.

IMAP (Internet Message Access Protocol) est un protocole créé pour des usages plus avancés que POP3. Il intègre nativement le support des dossiers de mail par exemple. Ci-dessous, un exemple d'échange IMAP4 issu de [la RFC](https://datatracker.ietf.org/doc/html/rfc9051) que nous allons détailler.

```
S:   * OK [CAPABILITY STARTTLS AUTH=SCRAM-SHA-256 LOGINDISABLED
         IMAP4rev2] IMAP4rev2 Service Ready
C:   a000 starttls
S:   a000 OK Proceed with TLS negotiation
    <TLS negotiation>
C:   A001 AUTHENTICATE SCRAM-SHA-256 biwsbj11c2VyLHI9ck9wck5HZndFYmVSV2diTkVrcU8=
S:   + cj1yT3ByTkdmd0ViZVJXZ2JORWtxTyVodllEcFdVYTJSYVRDQWZ1eEZJbGopaE5sRiRrMCxzPVcyMlphSjBTTlk3c29Fc1VFamI2Z1E9PSxpPTQwOTY=
C:   Yz1iaXdzLHI9ck9wck5HZndFYmVSV2diTkVrcU8laHZZRHBXVWEyUmFUQ0FmdXhGSWxqKWhObEYkazAscD1kSHpiWmFwV0lrNGpVaE4rVXRlOXl0YWc5empmTUhnc3FtbWl6N0FuZFZRPQ==
S:   + dj02cnJpVFJCaTIzV3BSUi93dHVwK21NaFVaVW4vZEI1bkxUSlJzamw5NUc0PQ==
C:
S:   A001 OK SCRAM-SHA-256 authentication successful
C:   babc ENABLE IMAP4rev2
S:   * ENABLED IMAP4rev2
S:   babc OK Some capabilities enabled
C:   a002 select inbox
S:   * 18 EXISTS
S:   * FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
S:   * OK [UIDVALIDITY 3857529045] UIDs valid
S:   * LIST () "/" INBOX ("OLDNAME" ("inbox"))
S:   a002 OK [READ-WRITE] SELECT completed
C:   a003 fetch 12 full
				S:   * 12 FETCH (FLAGS (\Seen) INTERNALDATE
      "17-Jul-1996 02:44:25 -0700" RFC822.SIZE 4286 ENVELOPE (
      "Wed, 17 Jul 1996 02:23:25 -0700 (PDT)"
      "IMAP4rev2 WG mtg summary and minutes"
      (("Terry Gray" NIL "gray" "cac.washington.edu"))
      (("Terry Gray" NIL "gray" "cac.washington.edu"))
      (("Terry Gray" NIL "gray" "cac.washington.edu"))
      ((NIL NIL "imap" "cac.washington.edu"))
      ((NIL NIL "minutes" "CNRI.Reston.VA.US")
      ("John Klensin" NIL "KLENSIN" "MIT.EDU")) NIL NIL
      "<B27397-0100000@cac.washington.ed>")
      BODY ("TEXT" "PLAIN" ("CHARSET" "US-ASCII") NIL NIL "7BIT"
      3028 92))
S:    a003 OK FETCH completed
C:    a004 fetch 12 body[header]
S:    * 12 FETCH (BODY[HEADER] {342}
S:    Date: Wed, 17 Jul 1996 02:23:25 -0700 (PDT)
S:    From: Terry Gray <gray@cac.washington.edu>
S:    Subject: IMAP4rev2 WG mtg summary and minutes
S:    To: imap@cac.washington.edu
S:    cc: minutes@CNRI.Reston.VA.US, John Klensin <KLENSIN@MIT.EDU>
S:    Message-Id: <B27397-0100000@cac.washington.edu>
S:    MIME-Version: 1.0
S:    Content-Type: TEXT/PLAIN; CHARSET=US-ASCII
S:
S:    )
S:    a004 OK FETCH completed
C:    a005 store 12 +flags \deleted
S:    * 12 FETCH (FLAGS (\Seen \Deleted))
S:    a005 OK +FLAGS completed
C:    a006 logout
S:    * BYE IMAP4rev2 server terminating connection
S:    a006 OK LOGOUT completed
```

Ça fait beaucoup de choses 😅 Détaillons tout ça étape par étape

1. Ici, le serveur indique les extensions qu'il supporte ainsi que sa version.

    Le client lui répond ensuite en indiquant qu'il souhaite utiliser STARTTLS, un échange de clé TLS est initié. Vous avez peut-être remarqué le `a000` au début des commandes. Cet identifiant est appelé tag, le client doit en générer un à chaque commande, il permet d'identifier la commande.

```
S:   * OK [CAPABILITY STARTTLS AUTH=SCRAM-SHA-256 LOGINDISABLED
         IMAP4rev2] IMAP4rev2 Service Ready
C:   a000 starttls
S:   a000 OK Proceed with TLS negotiation
    <TLS negotiation>
```

2. Ici, le client s'authentifie auprès du serveur

```
C:   A001 AUTHENTICATE SCRAM-SHA-256
         biwsbj11c2VyLHI9ck9wck5HZndFYmVSV2diTkVrcU8=
S:   + cj1yT3ByTkdmd0ViZVJXZ2JORWtxTyVodllEcFdVYTJSYVRDQWZ1eEZJbGopaE5sRiRrMCxzPVcyMlphSjBTTlk3c29Fc1VFamI2Z1E9PSxpPTQwOTY=
C:   Yz1iaXdzLHI9ck9wck5HZndFYmVSV2diTkVrcU8laHZZRHBXVWEyUmFUQ0FmdXhGSWxqKWhObEYkazAscD1kSHpiWmFwV0lrNGpVaE4rVXRlOXl0YWc5empmTUhnc3FtbWl6N0FuZFZRPQ==
S:   + dj02cnJpVFJCaTIzV3BSUi93dHVwK21NaFVaVW4vZEI1bkxUSlJzamw5NUc0PQ==
C:
S:   A001 OK SCRAM-SHA-256 authentication successful
```

Tous les champs ci-dessus sont encodés en base 64, la version décodée est ci-dessous

```
C:   A001 AUTHENTICATE SCRAM-SHA-256 n,,n=user,r=rOprNGfwEbeRWgbNEkqO
S:   + r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,s=W22ZaJ0SNY7soEsUEjb6gQ==,i=4096
C:   c=biws,r=rOprNGfwEbeRWgbNEkqO%hvYDpWUa2RaTCAfuxFIlj)hNlF$k0,p=dHzbZapWIk4jUhN+Ute9ytag9zjfMHgsqmmiz7AndVQ=
S:   + v=6rriTRBi23WpRR/wtup+mMhUZUn/dB5nLTJRsjl95G4=
C:
S:   A001 OK SCRAM-SHA-256 authentication successful
```

Ici le protocole utilisé pour l'authentification est SCRAM-SHA-256, celui ci ne sera pas plus détaillé dans cet article, mais il le sera dans un prochain ;).

3. Le client indique simplement quelle version d'IMAP il souhaite utiliser

```
C:   babc ENABLE IMAP4rev2
S:   * ENABLED IMAP4rev2
```

4. Le client sélectionne la boite mail qu'il souhaite consulter, ici, c'est "inbox". Le serveur répond en indiquant, entre autre, les différents "flag" autorisés. Ces derniers peuvent changer d'une implémentation à l'autre, mais aussi le nombre de messages présents sur le serveur (ici, 18).

```
C:   a002 select inbox
S:   * 18 EXISTS
S:   * FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
S:   * OK [UIDVALIDITY 3857529045] UIDs valid
S:   * LIST () "/" INBOX ("OLDNAME" ("inbox"))
S:   a002 OK [READ-WRITE] SELECT completed
```

5. Ici, le client va demander au serveur de lui envoyer le message qui a pour ID 12.

Le serveur répond en indiquant, dans l'ordre, les différents Flags, la date, la taille du message en octets, l'enveloppe (qui contient toutes les "métadonnées" du mail, le destinataire, l'objet, la date d'envoi etc.) et le corps du message.

```
C:   a003 fetch 12 full
S:   * 12 FETCH (
      FLAGS (\Seen)
      INTERNALDATE 17-Jul-1996 02:44:25 -0700"
      RFC822.SIZE 4286
      ENVELOPE (
	      "Wed, 17 Jul 1996 02:23:25 -0700 (PDT)"
	      "IMAP4rev2 WG mtg summary and minutes"
	      (("Terry Gray" NIL "gray" "cac.washington.edu"))
          (("Terry Gray" NIL "gray" "cac.washington.edu"))
   	      (("Terry Gray" NIL "gray" "cac.washington.edu"))
          ((NIL NIL "imap" "cac.washington.edu"))
          ((NIL NIL "minutes" "CNRI.Reston.VA.US")
          ("John Klensin" NIL "KLENSIN" "MIT.EDU")) NIL NIL
          "<B27397-0100000@cac.washington.ed>"
      )
      BODY (
          "TEXT" "PLAIN" ("CHARSET" "US-ASCII") NIL NIL "7BIT" 3028 92)
      )
S:    a003 OK FETCH completed
```

Dans la requête suivante, le client demande au serveur de voir le header, le serveur lui renvoie en fait l'enveloppe mais affichée d'une manière différente

```
C:    a004 fetch 12 body[header]
S:    * 12 FETCH (BODY[HEADER] {342}
S:    Date: Wed, 17 Jul 1996 02:23:25 -0700 (PDT)
S:    From: Terry Gray <gray@cac.washington.edu>
S:    Subject: IMAP4rev2 WG mtg summary and minutes
S:    To: imap@cac.washington.edu
S:    cc: minutes@CNRI.Reston.VA.US, John Klensin <KLENSIN@MIT.EDU>
S:    Message-Id: <B27397-0100000@cac.washington.edu>
S:    MIME-Version: 1.0
S:    Content-Type: TEXT/PLAIN; CHARSET=US-ASCII
S:
S:    )
S:    a004 OK FETCH completed
```

6. Enfin, le client ajoute le flag deleted au message d'ID 12, ce qui le place donc dans la corbeille. (ici on ajoute des flags avec +flags, et si on voulait enlever le flag deleted du message 12, on ferait -flags).

```
C:    a005 store 12 +flags \deleted
S:    * 12 FETCH (FLAGS (\Seen \Deleted))
S:    a005 OK +FLAGS completed
```


Voilà cet échange déchiffré, comme vous avez pu le voir, IMAP embarque des fonctionnalités supplémentaires par rapport à POP3, comme les Flags. Niveau sécurité, IMAP propose en plus de STARTTLS un port dédié aux communications chiffrées, le port 993, un sysadmin soucieux de la confidentialité des mails échangés sur son réseau pourrait donc bloquer le port 143 (port par défaut d'IMAP) pour forcer à passer par le port 993, et donc par une communication chiffrée. Une telle pratique peut néanmoins poser d'évidents problèmes de compatibilité. Il n'existe pas avec IMAP de mécanisme semblable avec DMARC pour qu'un serveur puisse forcer ses clients à utiliser une connexion chiffrée.

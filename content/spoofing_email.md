Author: Eban
Date: 2021/12/07
Keywords: cryptographie, mail, sécurité
Slug: spoofing_email
Summary: Dans un précédent article, nous avions vu comment fonctionne SMTP, mais aussi comment sécuriser les échanges entre les appareils qui utilisent ce protocole. Aujourd'hui nous regarderons comment empêcher l'usurpation (spoofing) d'adresse email avec SMTP.
Title: Empêcher l'usurpation d'adresse mail avec DKIM et SPF

Dans un précédent article, nous avions vu [comment fonctionne SMTP](https://ilearned.eu/smtp.html), mais aussi [comment sécuriser](https://ilearned.eu/secu_smtp.html) les échanges entre les appareils qui utilisent ce protocole. Aujourd'hui nous regarderons comment empêcher l'usurpation (spoofing) d'adresse email avec SMTP.

# DKIM

DKIM (DomainKeys Identified Mail) est sûrement le protocole le plus connu quand on parle d'empêcher l'usurpation d'adresse mail. C'est un protocole qui s'appuie sur la cryptographie asymétrique (le plus souvent [RSA](https://ilearned.eu/rsa.html)) afin de signer certaines parties d'un mail.

Un header DKIM ressemble à ça : 

```bash
DKIM-Signature: 
	v=1; 
	a=rsa-sha256; 
	c=relaxed/relaxed; 
	d=ilearned.eu; 
	s=gm1;
	t=1637402778;
	h=from:from:reply-to:subject:subject:date:date:message-id:message-id:
	 to:to:cc:mime-version:mime-version:content-type:content-type:
	 content-transfer-encoding:content-transfer-encoding;
	bh=jkYhN5eG70Kk/sFVzVJcKR3X2zwf3jR4Ui9PYcA/0b0=;
	b=ky1aAlPLJLL7xDCTgvPe+KMvtqBovXeKl6vzcT3vTd/uQAndwkzYegVvrKVdI2JxdGSVJ8
	otZ2ksJ+x6yUvPGwwN9tGcLq5cMmYNM6D8uYR7vYIm7gR8YnLohASnPFs87EpLAH0ue32L
	FDbnjbMh7eNZNK6WWrfRzATKYGFqMAyBiJOKPy8KybqulFtpII5V4rHbahpL+zI6EfDBXP
	Hro15OxGwfgp6oGUeu+1tyEEwu845h/Ftw4LP2vywMvPNS5PwTMEaytXrRfop7MX7Min4B
	y80e2ySYjAFI098fOoYTHeS6afLWbC7jRhBZ291BghmeADX8JUn853dsMekqdQ==

```

- `v` correspond à la version utilisée
- `a` correspond à l'algorithme utilisé
- `d` au nom de domaine pour lequel l'authentification a été validée
- `s` est le sélecteur, c'est en cherchant un enregistrement TXT pour `s`._domainkey.`d` (ici `gm1._domainkey.ilearned.eu`) que l'on trouve la clé publique du serveur qui a validé le mail.
    
```bash
╰─$ dig gm1._domainkey.ilearned.eu TXT                                                                                                                                                                                                    
;; ANSWER SECTION:
gm1._domainkey.ilearned.eu. 10800	IN	CNAME	gm1.gandimail.net.
gm1.gandimail.net.	1800	IN	TXT	"v=DKIM1; h=sha256; k=rsa;" "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAp8Mks4TXRqy7GjW3uIN2pfL+lnTNzEBYnYvoh9WbYseieVQIysX3tAPFz3oCoPlANa31gj/slInQVi" "B6tVb59Sw2loR1MS7HGp8g/5LaNI7KIdojiTDalLJCi4VK4Kw6eOIE/dAM/qKe3KrvU2EvSfVeU/emXU/B483vgWLWbakyiMekQN6mc+JZkegcmefambtVxrYqLswQLM9EwQ4fQPI/x8H067cOZfOe" "jPF3+a+uwbjOC8x5xVfAsNMjFmNDYoKaSjxcrX0fw54p/+5N1ciKdN7mCqsXrtb3ZRwn6TddzJR6ji0ID8fV4Y8/nUhLftsD4FRw54p7Hd3Ds1UseQIDAQAB"
```
    
- `h` correspond aux entêtes (headers) qui ont été signés
- `bh` correspond au hash du corps du message
- `b` correspond enfin au corps du courriel ainsi que les entêtes signés

Quand le serveur SMTP de destination reçoit le courriel, il vérifie avec la clé publique présente dans l'enregistrement DNS vu ce-dessus que la signature est correcte. Si elle ne l'est pas, il peut décider de simplement supprimer le message, ou de le placer dans les spams.

# SPF

SPF (Sender Policy Framework) est un protocole plus simple dans son fonctionnement que DKIM mais qui propose aussi un niveau de protection contre l'usurpation d'adresse mail satisfaisant. Avec SPF, un enregistrement DNS TXT est publié dans la zone du nom de domaine d'envoi. Ce record contient une liste d'adresses IPs (de [MTA](https://ilearned.eu/smtp.html)) autorisées à envoyer des courriels. Voici par exemple l'enregistrement pour la zone eff.org

```bash
eff.org.		7200	IN	TXT	"v=spf1 mx ip4:173.239.79.202 include:spf1.eff.org include:spf2.eff.org include:spf.protection.outlook.com include:salsalabs.org -all"
```

Plusieurs règles sont définies ici

- `mx` Autorise si le nom de domaine contient un enregistrement MX pointant vers l'adresse IP de l'expéditeur. Ici l'enregistrement MX correspond à eff-org.mail.protection.outlook.com qui renvoie vers l'IP 104.47.55.138, cette IP est donc autorisée à envoyer des mails @eff.org.
- `ip4` Autorise si l'adresse de l'expéditeur correspond à 173.239.79.202 dans notre cas.
- `include` inclue les règles contenues dans le domaine indiqué.
    
```bash
spf1.eff.org.		7200	IN	TXT	"v=spf1 ip4:50.28.103.180 ip4:50.28.103.181 ip4:67.212.170.242 ?ip4:128.199.236.247 ?ip4:38.229.72.13 ?ip4:165.117.251.93 ?ip4:38.99.228.141 ?ip4:78.47.153.197 -all"
```
    
```bash
spf2.eff.org.		7200	IN	TXT	"v=spf1 ?include:amazonses.com -all"
```
   
```bash
salsalabs.org.		300	IN	TXT	"v=spf1 ip4:204.28.10.0/23 ip4:69.174.82.0/23 ip4:147.253.0.0/16 ip4:192.174.0.0/16 ip4:156.70.0.0/16 -all"
```
    
Comme on peut le voir, en allant interroger les différents noms de domaines inclus, de nombreuses autres adresses IPv4 sont autorisées, et on trouve une autre inclusion vers amazonses.com
    
```bash
amazonses.com.		900	IN	TXT	"v=spf1 ip4:199.255.192.0/22 ip4:199.127.232.0/22 ip4:54.240.0.0/18 ip4:69.169.224.0/20 ip4:23.249.208.0/20 ip4:23.251.224.0/19 ip4:76.223.176.0/20 ip4:54.240.64.0/19 ip4:54.240.96.0/19 ip4:52.82.172.0/22 -all"
```
    
Et voilà, nous avons remonté l'ensemble des adresses IPs autorisées pour le domaine [eff.org](http://eff.org) 😅.
    
- `-all` indique que si l'adresse IP ne correspond pas, le mail doit être rejeté. D'autres signes avant le `all` auraient pu indiquer d'autres actions
    - `+` : laisser passer le mail
    - `?` : résultat neutre, comportement différent selon les logiciels utilisés
    - `~` : c'est le *softfail* les messages qui retournent un softfail sont acceptés, cet échec est cependant indiqué par le client mail
    - `-` : le mail est rejeté, c'est ce qui est utilisé ici avec le `-all`

# DMARC

L'utilisation de SPF et de DKIM n'a cessé de croitre ces dernières années, et afin d'homogénéiser l'utilisation de ces deux protocoles, et la réponse en cas de non-satisfaction de ceux-ci, un nouveau standard a été créé. DMARC (Domain-based Message Authentication, Reporting and Conformance) est un enregistrement DNS TXT dans _dmarc.NDD qui spécifie ces différents comportements. Reprenons notre exemple avec [eff.org](http://eff.org) : 

```bash
_dmarc.eff.org.		7200	IN	TXT	"v=DMARC1; p=none; rua=mailto:dmarc_rua@eff.org; ruf=mailto:dmarc_ruf@eff.org;"
```

- `p` : que faire en cas d'échec de SPF/DKIM
    - `none` : aucune action de la part du receveur n'est requise.
    - `quarantine` : le receveur doit traiter ce message comme "suspicieux" en le plaçant dans les spams par exemple.
    - `reject` : le receveur doit rejeter le message.
- `rua` correspond à l'URI où un rapport doit être envoyé en cas d'échec de SPF/DKIM.
- `ruf` correspond à l'URI où un rapport détaillé doit être envoyé.

C'est sur cet article que s'achève notre série de trois articles dédiés à l'envoi de mails, j'espère qu'ils vous auront plu. Si vous avez des questions/remarques, n'hésitez pas à nous en faire part dans l'espace commentaire ci-dessous.

Author: Eban 
Date: 2021/07/22
Keywords: ssh, sécurité
Slug: ca-ssh
Summary: SSH est un protocole très répandu sur internet, il est utilisé par des millions d'entreprises et de particuliers chaque jour, mais bien souvent de façon peu sécurisée. Pour remédier à cela il existe une solution que nous allons étudier dans cet article, les autorités de certification SSH.
Title: Comment faire une autorité de certification (CA) SSH ?

SSH est un protocole très répandu sur internet, il est utilisé par des millions d'entreprises et particuliers chaque jour, mais bien souvent de façon peu sécurisée. Vous connaissez peut-être les clés SSH qui permettent une meilleure sécurité que les mots de passe, mais ces clés posent un problème, et notamment en entreprise, imaginez une entreprise avec 500 ingénieurs, il faudrait, sur chaque serveur SSH, mettre les 500 clés publiques des 500 ingénieurs ! Pour remédier à cela il existe une solution que nous allons étudier dans cet article, les autorités de certification SSH.

# La théorie

Le système de certificats de SSH est relativement similaire à celui de TLS (x509), une première paire de clés publiques/privées est générée, elle servira d'**autorité de certification**, le clé privée de cette autorité de certification doit bien évidemment rester ultra confidentielle. On va ensuite générer une autre paire de clé sur chaque client. On pourra ensuite, avec la clé privée de notre autorité de certification, signer la publique des clients afin de générer un certificat. Ainsi, n'importe quel certificat signé par notre autorité de certification peut être considérée comme "de confiance".

![Principe d'une autorité de certification](/static/img/ca-ssh/CA_principe(1).png)

# Signer les clés hôte

Lors de la première connexion à un serveur SSH, le serveur envoie sa clé publique (appelée clé hôte) au client et le client doit approuver, ou non, l'authenticité de la clé envoyée par le serveur, c'est le fameux message

```bash
The authenticity of host 'XXXXX' can't be established.
ED25519 key fingerprint is SHA256:JxfJl38mBVY2jX0h/LWDuB1OtgYfgLBr3nJw/lw5GFE.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? 
```

Nous avons tous pour (mauvaise) habitude de simplement entrer `yes` sans se poser plus de questions, mais cette habitude est très dangereuse, un attaquant pourrait usurper le serveur SSH auquel nous essayons de nous connecter ! Pour remédier à cela il existe plusieurs solutions comme [SSHFP](https://fr.wikipedia.org/wiki/Enregistrement_DNS_SSHFP) (qui est relativement similaire à [TLSA](https://ilearned.eu.org/dane.html), mais avec SSH) ou les autorités de certification (CA) c'est ce que nous allons détailler ici.

La première étape est donc de créer une paire de clés pour notre autorité de certification avec la commande

```
ssh-keygen -a 1000 -t ed25519 -f /etc/ssh/ca/id_ed25519 -C "contact+ca@eban.bzh"
```

L'option `-a` indique le nombre de tours KDF (fonction de dérivation de la clé), plus ce nombre est élevé, plus la vérification du mot de passe sera lente, mais plus la clé sera résistante au bruteforce.

`-t` indique l'algorithme à utiliser pour la clé, ici c'est ed25519, l'algorithme de chiffrement [le plus sécurisé à ce jour](https://nbeguier.medium.com/a-real-world-comparison-of-the-ssh-key-algorithms-b26b0b31bfd9) supporté par SSH.

Une fois cette première paire de clé créée, nous allons pouvoir l'utiliser pour signer les clés hôtes publiques de nos serveurs SSH, la première étape est donc d'aller cherche ces clés hôtes, elles sont, sur chaque serveur SSH, dans le répertoire /etc/ssh, ici je ne génèrerait qu'un certificat en `ed25519` mais la même démarche est possible avec n'importe quel algorithme supporté par OpenSSH. La clé publique hôte est donc disponible sous le chemin `/etc/ssh/ssh_host_ed25519_key.pub` copions-là dans le répertoire `/etc/ssh/ca` de la machine sur laquelle nous avons généré l'autorité de certification. On peut ensuite lancer la commande

```
ssh-keygen -h -s /etc/ssh/ca/id_ed25519 -n pi01,pi01.infra.eban.bzh -I pi01 -V +3650d ssh_host_ed25519_key.pub
```

L'option `-n` correspond aux `principals`, dans le cas d'une clé hôte, elle doit correspondre aux différents noms de domaine auxquelles la clé pourrait être associée.

`-I` correspond à l'`ID`, un identifiant unique attribué à la clé, c'est simplement son "nom".

Une fois la clé publique signée, il ne nous reste plus qu'à copier le certificat qui aura été généré dans le répertoire `/etc/ssh/ca/ssh_host_ed25519_key-cert.pub` sur le serveur SSH (ici nous le mettrons à l'emplacement `/etc/ssh/ssh_host_ed25519_key-cert.pub`) et à ajouter la ligne suivante à la fin du fichier `/etc/sshd_config`.

```
HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub
```

On redémarre ensuite le démon ssh avec la commande `systemctl restart sshd`.

Dernière étape, on va indiquer à tous les clients SSH de faire confiance aux certificats hôtes signés par notre autorité de certification en utilisant la commande

```bash
echo "@cert-authority * $(cat /etc/ssh/ca/id_ed25519.pub)" >> ~/.ssh/known_hosts
```

Et voilà ! Notre autorité de certification est maintenant configurée sur le serveur SSH.

# Signer les clés clients

La procédure pour signer les clés des clients est relativement similaire, après avoir généré une paire de clés pour l'autorité de certification (on gardera la même que celle générée dans la partie précédente), on lance la commande

```
ssh-keygen -s /etc/ssh/ca/id_ed25519 -n pi -I pc01@eban.bzh -V +30d -z 1 /home/USERNAME/.ssh/id_ed25519.pub
```

N'oubliez pas de changer `USERNAME` par votre nom d'utilisateur.

Si vous obtenez une erreur, c'est probablement que n'avez pas déjà une paire de clé SSH en `ed25519` vous pouvez en générer une avec la commande

```
ssh-keygen -t ed25519
```

Une fois la paire de clé générée, vous pouvez relancer la première commande.

Ici l'option `-n` correspond au⋅x **nom**⋅s **d'utilisateur distant** (= sur le serveur SSH) pour lesquels vous souhaitez autoriser que cette clé soit valide, cette clé ne sera donc valide que pour le nom d'utilisateur distant  `pi`.

`-z` correspond au `serial` de ce certificat, c'est un nombre que vous devrez incrémenter si vous régénérez la clé après la durée d'expiration (ici mise à 30 jours).

Une fois cela fait, il ne nous reste plus qu'à copier la clé publique de notre autorité de certification (contenue dans `/etc/ssh/ca/id_ed25519.pub`) sur notre serveur SSH, ici nous la mettrons dans le fichier `/etc/ssh/ca.pub` et à ajouter la ligne `TrustedUserCAKeys /etc/ssh/ca.pub` à la fin du fichier `/etc/ssh/sshd_config`. On termine par redémarrer le service SSH, `sudo systemctl restart sshd`.

Nous avons maintenant mit en place notre autorité de certification ! On peut simplement la tester en se connectant via SSH au serveur, vous ne devriez pouvoir vous connecter sans mot de passe et n'avoir aucune demande de validation de la clé publique de la machine hôte. J'espère que cet article vous aura été utile, si vous avez des questions n'hésitez pas à nous les poser en commentaire ou sur [Twitter](https://twitter.com/ilearned_eu).

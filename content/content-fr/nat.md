Title: NAT/PAT
Description: Au début d'internet, chaque machine avait sa propre IPv4 (comme aujourd'hui en IPv6), Internet qui de base était un projet au public limité à commencé à grandir et le nombre totale d'IPv4 commençait à montrer ses limites. Plusieurs solutions ont été pensées, l'une d'entre elles est le NAT.
slug: nat
Author: Ramle 
Date: 2021-12-02
Keywords: réseau, nat, pat

Au début d'internet, chaque machine avait sa propre IPv4 (comme aujourd'hui en IPv6), Internet qui de base était un projet au public limité à commencé à grandir et le nombre totale d'IPv4 commençait à montrer ses limites. Plusieurs solutions ont été pensées, l'une d'entre elles est le NAT.

Derrière l'acronyme NAT (network adress translation) plusieurs méthodes existent.

# PAT

PAT est l'acronyme de port adress translation, c'est la méthode la plus courante. Cette méthode permet de n'utiliser qu'une seule IP pour plusieurs machines.

Pour fonctionner il faudra un réseau avec des adresses non routable sur internet, appelées IP privée, et un routeur qui possède lui une IP routable sur internet.

Quand un appareil local va vouloir établir une connexion avec l'extérieur le routeur va s'occuper de remplacer l'IP source du paquet par la sienne et le port par un port aléatoire que le routeur va retenir. Quand la destination va vouloir répondre, le routeur va regarder le port où le paquet arrive et rediriger le paquet vers l'IP locale qui l'a initialisé.

![Schema PAT](/static/img/nat/pat.webp)

Un problème de cette méthode est vite visible, si on veut héberger un service public sur une des machines du réseau, les gens sur internet ne pourront pas le joindre vu qu'il ne possède qu'un IP privée. Une solution existe à ça, une redirection permanente de port. Le principe de ce mécanisme est de dire au routeur que si un paquet arrive sur l'IP public, sur un port précis il faut toujours rediriger vers une IP locale définie.

![Port Forward schema](/static/img/nat/port_forward.webp)

Un problème majeur de ce type de NAT est que le routeur oublie au bout d'un certains temps qu'une connexion a été établie, un certain nombre d'applications cassent à cause de ce mécanisme. Une solution parfois mise en œuvre pour ne pas se faire oublier est d'envoyer régulièrement du trafic.

# CG-NAT

Un autre processus se répand de plus en plus, le CG-NAT (Carrier-grade NAT), il est aussi parfois appelé NAT444. C'est un mécanisme qui permet aux opérateurs d'économiser plus d'adresse IP. Le routeur du client recevra une adresse IP privée et sa passerelle par défaut sera aussi une IP privée. Le routeur coté opérateur va s'occuper de remplacer l'IP privée du client par la sienne, cela permet de mettre plusieurs clients sur une seule IP.

Le routeur du client lui, fait du NAT classique, mais avec une IP privée en tant qu'IP public.

Cette méthode pose encore plus de problème que le simple NAT. Par exemple, il rend compliqué l'hébergement de service chez soi. L'opérateur peut permettre la redirection de port via divers mécanismes, cependant c'est comme l'IP est partagée entre plusieurs il faut qu'aucun des autres clients n'utilise le port que l'on veut.

Un autre souci de taille est que pas mal de protocoles ne fonctionnent plus, ou mal, avec ce mécanisme.

# NAT64

Une autre méthode pour économiser des adresses IPv4 (les deux normes ci-dessus sont en théorie compatible avec IPv6 cependant, c'est une mauvaise pratique) est tout simplement de ne pas en donner au client (ni privée, ni publique).

Le souci qui se pose dans ce cas-là est qu'une partie assez importante d'internet n'est pas encore passé à IPv6.

La solution apportée à ce manque est de disposer d'un résolveur spécial qui fait du DNS64, et un routeur ou serveur qui s'occupe de traduire les IPv6 donnée par le résolveur vers l'IPv4 cible.

Par exemple Alice veut accéder au serveur web de Bob, mais Alice n'a pas d'IPv4, et Bob n'a pas d'IPv6. Le réseau où est Alice a instauré du NAT64 et un résolveur configuré pour, en allant sur `https://bob.example` ou l'enregistrement de type A est 192.0.2.42 son résolveur va en réalité lui retourner 64:ff9b::c000:022a (souvent écrit 64:ff9b::192.0.2.42 qui est en réalité la même chose, le premier étant en hexadécimal), le préfixe, ici 64:ff9b::, n'est pas important, seule la fin est utile, elle contient l'IPv4. Le préfixe doit être routé vers un serveur qui s'occupera de translater l'IPv6 et IPv4, ce serveur doit donc posséder une IPv4 (toutefois, cette dernière peut être mutualisée pour un grand nombre de clients).

Cette méthode pose cependant un certain nombre de problèmes. La communication avec une IP directement (sans nom de domaine) n'est par exemple pas possible (mais des méthodes comme 464XLAT existent). Comme pour toutes les autres méthodes ci-dessus, certains protocoles ne sont pas compatibles avec NAT64. DNSSEC ne fonctionne pas non plus.

![NAT64/DNS64 schema](/static/img/nat/nat64.webp)

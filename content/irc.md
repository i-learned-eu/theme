Title: Le protocole IRC
Keywords: irc, chat
Date: 2021-05-05
Author: Ramle
Summary: Bonjour, hier nous avions vu le protocole TCP, aujourd'hui nous allons en reparler en l'appliquant concrètement. :)
Slug: irc

Hier nous avions vu le protocole TCP, aujourd'hui nous allons en reparler en l'appliquant concrètement. Le protocole que nous allons voir est IRC qui est très simple dans sa conception, ce qui permet de l'utiliser à la main sans se prendre trop la tête.

IRC est l'acronyme d'Internet Relay Chat (traduit littéralement par relai de discussion internet), comme son nom l'indique, le serveur ne fait que relayer les messages, il ne les stocke pas contrairement à de nombreux autres protocoles de chat.

Comme sous entendu juste au dessus, IRC fonctionne dans un mode client serveur, le client est identifié par un "nick" (diminutif de nickname, pseudo), personne n'aura donc le même nick sur un serveur IRC. Le nick est le seule moyens d'identification d'un client, pour éviter de se le faire voler il faut laisser un client tourner en continu. Ce fonctionnement n'est pas forcément pratique et facilite l'usurpation, pour palier à ça beaucoup de serveur donnent la possibilité de s'authentifier à l'aide d'un mot de passe soit via un bot à qui on doit envoyer un message spécifique contenant le secret, soit via un système appelé SASL qui permet d'envoyer directement le mot de passe durant la phase de connexion au serveur. Pour ce qui est de l'usage principal de IRC, c'est à dire les messages, on fonctionne via des canaux, un peu comme discord, identifiés par une chaine de texte commençant par "#", chaque canal peut posséder une description (cela reste facultatif).

Pour essayer IRC on peut utiliser telnet qui est un outil qui permet d'établir des connexions TCP, on peut se connecter via la suite de commande :

```bash
telnet irc.example.org 6667 
USER utilisateur * * :Une description
NICK utilisateur #Définit le fameux nick
JOIN \#canal #Pour joindre un canal
PRIVMSG \#canal Un message #Envoi "Un message" dans #canal
# Le serveur réponds par le "MOTD" (messaye of the day, ou message du jour en français)
```

Ce qui donnera la sortie :

```bash
% telnet irc.lab.rameul.eu 6667
Trying 172.17.0.2...
Connected to irc.lab.rameul.eu.
Escape character is '^]'.
:irc.lab.rameul.eu NOTICE Auth :*** Looking up your hostname...
:irc.lab.rameul.eu NOTICE Auth :*** Could not resolve your hostname: Domain name not found; using your IP address (172.17.0.1) instead.
USER ramle * * :
NICK ramle
:irc.lab.rameul.eu NOTICE Auth :Welcome to rml-lab!
:irc.lab.rameul.eu 001 ramle :Welcome to the rml-lab IRC Network ramle!ramle@172.17.0.1
:irc.lab.rameul.eu 002 ramle :Your host is irc.lab.rameul.eu, running version InspIRCd-2.0
:irc.lab.rameul.eu 003 ramle :This server was created on Debian
:irc.lab.rameul.eu 004 ramle irc.lab.rameul.eu InspIRCd-2.0 iosw biklmnopstv bklov
:irc.lab.rameul.eu 005 ramle AWAYLEN=200 CASEMAPPING=rfc1459 CHANMODES=b,k,l,imnpst CHANNELLEN=64 CHANTYPES=# CHARSET=ascii ELIST=MU FNC KICKLEN=255 MAP MAXBANS=60 MAXCHANNELS=20 MAXPARA=32 :are supported by this server
:irc.lab.rameul.eu 005 ramle MAXTARGETS=20 MODES=20 NETWORK=rml-lab NICKLEN=32 PREFIX=(ov)@+ STATUSMSG=@+ TOPICLEN=307 VBANLIST WALLCHOPS WALLVOICES :are supported by this server
:irc.lab.rameul.eu 042 ramle 476AAAAAK :your unique ID
:irc.lab.rameul.eu 375 ramle :irc.lab.rameul.eu message of the day
:irc.lab.rameul.eu 372 ramle :- 
:irc.lab.rameul.eu 372 ramle :-  _ __ _ __ ___ | |      _ __   ___| |_ 
:irc.lab.rameul.eu 372 ramle :- | '__| '_ ` _ \| |_____| '_ \ / _ \ __|
:irc.lab.rameul.eu 372 ramle :- | |  | | | | | | |_____| | | |  __/ |_ 
:irc.lab.rameul.eu 372 ramle :- |_|  |_| |_| |_|_|     |_| |_|\___|\__|
:irc.lab.rameul.eu 372 ramle :- 
:irc.lab.rameul.eu 372 ramle :- Description : Lab
:irc.lab.rameul.eu 372 ramle :- NetAdmin : ramle
:irc.lab.rameul.eu 372 ramle :- 
:irc.lab.rameul.eu 376 ramle :End of message of the day.
:irc.lab.rameul.eu 251 ramle :There are 1 users and 0 invisible on 1 servers
:irc.lab.rameul.eu 254 ramle 0 :channels formed
:irc.lab.rameul.eu 255 ramle :I have 1 clients and 0 servers
:irc.lab.rameul.eu 265 ramle :Current Local Users: 1  Max: 2
:irc.lab.rameul.eu 266 ramle :Current Global Users: 1  Max: 2
JOIN #article
:ramle!ramle@172.17.0.1 JOIN :#article
:irc.lab.rameul.eu 353 ramle = #article :ramle @ramle2 
:irc.lab.rameul.eu 366 ramle #article :End of /NAMES list.
PRIVMSG #article o/
:ramle2!ramle2@172.17.0.1 PRIVMSG #article :o/
```

~~Pour ceux qui souhaiteraient tester par eux même avec telnet, le serveur IRC ne sera up qu'à partir de 21h30 ;).~~ Il est en ligne.

On peut voir dans ce court exemple plusieurs choses, déjà la simplicité du protocole, en seulement 3 commande on rejoint un canal. Un autre fait qui peut être noté, c'est la commande envoyée pour définir le nom d'utilisateur :  `USER ramle * * :`, il n'y a en effet pas de description, c'est une option facultative. Un autre point important est le symbole "@" devant l'utilisateur "ramle2", ce caractère signifie qu'il est "op" c'est à dire avec les permissions complète sur le canal, il peut donc expulser un membre, le bannir ou modifier des paramètres sur le canal, il ne peut par contre pas supprimer de messages vu que le serveur ne stocke rien, il ne sert que de relai entre les utilisateurs.

![IRC%2021507d67dcf84cbba48c88b9daad068c/Frame_30.png](/static/img/irc/Frame_30.png)

Sur la capture réseau, on peut observer le peu de requête pour chaque étape, l'envoi du contenu en lui même et l'accusé. Si vous voulez observer par vous même, le fichier est ici 

[irc.pcap](/static/misc/irc/irc.pcap)

C'est tout pour IRC, j'espère que ça vous aura plus. N'hésitez pas à poster en commentaire si vous avec des remarques, des questions, on se retrouve demain pour Gemini :)

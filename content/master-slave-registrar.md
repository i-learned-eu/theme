Title: Le principe de Master/Slave - Le rôle du registrar 
Keywords: DNS, Domain Name System, NS, knot, bind, apprendre, bases DNS, DNS simple
Summary: Pour ce second post dans la catégorie Today I Learned, on regarde le principe de registrar et Master/Slave appliqué au monde du DNS.
Date: 2021-04-25
Author: Ramle
Slug: master-slave-registrar

Aujourd'hui, on parle du rôle d'un Registrar puis dans une seconde partie du principe de Master/Slave dans le cadre de serveur DNS autoritaire.

Les registrars ou bureaux d'enregistrement en français sont des organisations qui gèrent les domaines de premier niveau (TLD). On peut citer par exemple EURid qui gère le `.eu`, DNS Belgium pour le `.be` ou encore l'AFNIC pour le `.fr`. 

Ces registrars obtiennent leurs domaines de premier niveau auprès de l'IANA. *je suppose que vous vous demandez ce qu'est l'IANA ?* L'IANA est une branche de l'iCANN, c'est la branche qui gère l'attribution de ressource comme les blocs d'IP ou les TLD.

Pour ce qui est de la revente de domaines, souvent les bureaux d'enregistrements passent par des sous-traitants, ces sous-traitants doivent respecter certaines règles comme par exemple un prix fixe reversé au registrar, ou des restrictions géographiques.

# Le principe de Master/Slave

Le principe de master et de slave est assez important dans le monde du DNS et de l'informatique en général, il permet, dans le cadre du DNS, de redonder facilement une zone sur plusieurs serveurs autoritaires.

Le serveur dit `master` (maître) est celui qui contrôle la zone, il possède le fichier "original".

Dans certains contextes, comme pour éviter la corruption de tous les serveurs en cas d'erreur sur le maître, on utilise plusieurs serveurs masters, il n'y a plus une seule zone "original " mais plusieurs, le désavantage d'un tel système c'est qu'on est obligé de mettre à jour chaque serveurs master *manuellement*.

Le serveur dit `slave` (esclave) est celui qui reçoit la zone depuis un serveur master, ce transfert de zone DNS **utilise des protocoles comme AXFR ou IXFR *mais ça c'est pour demain 😉.*

Ce concept de master/slave permet de redonder une zone bien plus facilement que si on le faisait manuellement.

![Schéma sur le fonctionnement master/slave](/static/img/master-slave-registrar/schema-master-slave.png)

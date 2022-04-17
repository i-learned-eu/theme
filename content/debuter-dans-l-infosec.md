lang: fr
Title: Debuter dans l'infosec 👨‍💻
Keywords: [Debuter, infosec, hacking, pentesting, commencer, comment, eban]
Summary: Dans ce nouvel article, nous allons traiter de la fameuse question ''La sécurité informatique, ca m'intéresse, mais par où commencer ?'' Par où commencer, la question est vaste mais voici un petit résumé des prérequis nécessaires pour commencer dans l'Infosec.
Image: https://images.unsplash.com/photo-1541728472741-03e45a58cf88?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1000&q=80
Date: 2020-07-10
Author: Eban
Category: Cybersécurité/Blue Team

Dans ce nouvel article, nous allons traiter de la fameuse question

> La sécurité informatique, ca m'intéresse, mais par où commencer ?

Par où commencer, la question est vaste mais voici un petit résumé des prérequis nécessaires pour commencer dans l'Infosec :

Pour commencer dans le monde de la cybersecurité, il est recommandé d'apprendre un language de scripting tel que le python ( voici un très bon cours venant du site de [zeste de savoir](https://zestedesavoir.com/tutoriels/799/apprendre-a-programmer-avec-python-3/), les bases des languages web sont aussi quasi-indispensables ([ici](https://apprendre-html.3wa.fr/courses) ou [là](https://openclassrooms.com/fr/courses/918836-concevez-votre-site-web-avec-php-et-mysql) vous pourrez trouver un cours sur le html, le css, le js ainsi que le php) il est aussi important d'apprendre les bases du fonctionnement des protocoles réseaux les plus courants (voici [un cours](https://openclassrooms.com/fr/courses/857447-apprenez-le-fonctionnement-des-reseaux-tcp-ip) qui peut vous aider à comprendre ces protocoles), pour finir, je recommanderais de passer sous une distribution Linux comme Ubuntu ou Arch pour les plus téméraires et de vous familiariser avec cet OS et au terminal linux.

Une fois tout ces prerequis validés, vous pourrez vous entrainer sur Root-Me

## Spécialisation

Après avoir découvert les bases de ce milieu, vous pourrez vous spécialiser dans certains domaines spécifiques

#### Le RE(Reverse Engineering / Rétro Ingénerie)

Le Reverse Engineering est le fait d'étudier le fonctionnement d'un programme pour en comprendre le fonctionnement sans avoir le code source de celui-ci.
Pour débuter dans ce domaine, il est indispensable de connaitre le [language C](https://zestedesavoir.com/tutoriels/755/le-langage-c-1/) ainsi que de [l'assembleur](https://www.youtube.com/watch?v=yxzUi8MdOAA&list=PLcT0DaY68xGzzmj47WSbb8XaIwWFjVlKz) (de préférence x86_64).
Vous pourrez alors vous entraîner sur des crackme, si vous voulez de l'aide ou seulement discuter de ces sujets, je vous invite à rejoindre l'un des serveurs discord listés ci-dessous.

#### Les Boxs

Les Boxs consistent en un machine faite pour être *piratée*, le but est de devenir administrateur (ou *root*) de la machine en utilisant plusieurs failles informatiques. Pour vous entrainer à cela, je vous invite à aller sur [HackTheBox](https://hackthebox.eu) ainsi que sur [Vulnhub](https://vulnhub.com).

#### Les CTF

Les CTF (Capture The Flag) sont des compétitions où l'on se penche seul ou en équipe sur une multitude d'épreuves appartenant à des catégories diverses (Reverse Engineering, Pwn, Crypto(graphy), OSINT (OpenSource Information Gatering)) consistent en un machine faite pour être *piratée*, le but est de devenir administrateur (ou *root*) de la machine en utilisant plusieurs failles informatiques. Pour vous entrainer à cela, je vous invite à aller sur [HackTheBox](https://hackthebox.eu) ainsi que sur [Vulnhub](https://vulnhub.com).

## Bonus : Ressources
Voici une liste non exhaustive de ressources qui pourraient vous aider :

- [exrs](https://github.com/wapiflapi/exrs) (Exercices de RE)
- [challenges.re](https://challenges.re/) (Exercices de RE allant avec le livre "Reverse Engineering for Beginners" de Dennis Yurichev (c.f [beginners.](https://beginners.re) )
- [crackmes.one](https://crackmes.one/) (Collection communautaire de crackmes par [sar](https://twitter.com/sar5430) 🇫🇷)
- [root-me](https://root-me.org/) (Challenges toutes catégories - FR)
- [newbiecontest](https://www.newbiecontest.org/) (Challenges toutes catégories)
- [theblackside](https://www.theblackside.fr/) (Challenges toutes catégories - FR)
- [brainshell](https://brainshell.fr/) (Challenges toutes catégories & CTF - FR)
- [hackthebox](https://www.hackthebox.eu/) (Propose des challenges, des machines, des attack/defence (seul ou en équipe) et des "Pro Labs" (Formation interactive au piratage dans des environnements d'entreprise réalistes) )
- [vulnhub](https://www.vulnhub.com/) (VM vulnérables)
- [tryhackme](https://tryhackme.com/) (enseigne la cybersécurité par le biais de laboratoires concrets et ludiques et propose des réseaux virtuels vulnérables)
- [dailysecurity](https://www.dailysecurity.fr/) (Blog de Geluchat)
- [hackndo](https://beta.hackndo.com/) (Blog de pixis)
- [hacktion](https://www.hacktion.be/) (Blog de Que20)
- [inf0sec](https://inf0sec.fr/) (Blog de Unknow101, orienté test d'intrusion windows)
- [sideway.re](https://sideway.re/) (Blog de @SideWay'CSS )
- [inshallhack](https://inshallhack.org/) (Blog de l'équipe française de CTF [Inshall'hack] (https://ctftime.org/team/44256))
- [Google](https://www.google.fr/) (RTFM, la base avant toute question.)
- [exploit.education](https://exploit.education/) (Un bon site pour débuter en pwn)
- [Rainbow](https://discord.gg/heAw9mZ) (Serveur discord parlant d'infosec mais aussi de programmation.)
- [ret2school](https://discord.gg/gFws9jH) (Serveur discord de [@nasm_re](https://twitter.com/nasm_re) et de l'équipe de CTF, [ret2school](https://twitter.com/ret2school_fr))

#### Remerciements :

Merci à SoEasY de m'avoir aidé pour la définition du RE.

Merci à MorpheusH3x pour la liste des ressources.

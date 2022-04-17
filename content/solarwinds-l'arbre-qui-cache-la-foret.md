lang: fr
Title: SolarWinds, l'arbre qui cache la forêt 👾
Keywords: [solarwinds, hacking, fireeye, APT]
Summary: Le 8 décembre 2020, Kevin Mandia, PDG de la société FireEye poste un communiqué nommé FireEye Shares Details of Recent Cyber Attack, Actions to Protect Community dans lequel il informe que la société a été victime d'une cyberattaque de la part d'un "acteur hautement sophistiqué" et que ce dernier avait accédé à leur réseau interne et volé un grand nombre d'outils de Red Team de l'entreprise...
Image: https://i.postimg.cc/gjxw1v0r/maxresdefault.jpg
Date: 02-06-2021
Author: Eban
Category: Cybersécurité/Red Team

## Avant propos

Cet article a pour but de retracer les évènements à propos de la récente attaque dont SolarWinds a été victime, ces actualités étant relativement récentes à l'heure où j'écris cet article (07/02/2021) des mises à jour seront sûrement apportées à ce dernier.

## Signal d'alarme

Le 8 décembre 2020, Kevin Mandia, PDG de la société FireEye poste un communiqué nommé [FireEye Shares Details of Recent Cyber Attack, Actions to Protect Community](https://www.fireeye.com/blog/products-and-services/2020/12/fireeye-shares-details-of-recent-cyber-attack-actions-to-protect-community.html) dans lequel il informe que l'entreprise a été victime d'une cyberattaque de la part d'un "acteur hautement sophistiqué" et que ce dernier avait accédé à leur réseau interne et volé un grand nombre d'outils de Red Team de la société. Ce communiqué fait aussi part du fait que

> sa discipline, sa sécurité opérationnelle et ses techniques nous conduisent à penser que [l'acteur malveillant derrière cette attaque] était soutenu par un état

Matt Gorham le directeur adjoint de la division cyber du FBI indique dans la foulée

> Le FBI enquête sur l'incident  et les premières constatations montrent un acteur avec un haut niveau de sophistication conforme à un État-nation

Ce qui semble donc confirmer les dires de FireEye.

Le 08 décembre 2020 à 20h11, dans [un article](https://www.nytimes.com/2020/12/08/technology/fireeye-hacked-russians.html) le New York Times suppute que

> Ce piratage soulève la possibilité que les agences de renseignement russes aient vu un avantage à monter l'attaque alors que l'attention américaine - y compris celle de FireEye - était concentrée sur la sécurisation du système des élections présidentielles.

Sans pour autant apporter de preuve tangible.

Le 13 décembre 2020, coup de tonnerre, FireEye indique dans [ce communiqué](https://www.fireeye.com/blog/products-and-services/2020/12/global-intrusion-campaign-leverages-software-supply-chain-compromise.html) que l'attaque qu'ils ont subi a été propagée par le système de mise à jour d'Orion, un logiciel de gestion de réseau édité par SolarWinds, un cheval de Troie nommé Sunburst avait été inséré dans les version 2019.4 HF 5, 2020.2 et 2020.2 HF 1 d'Orion. Microsoft, les départements américains du Commerce, du Trésor, de l'Énergie et plus encore ont déclaré avoir été victimes de cette cyberattaque.

## Un peu de reverse engineering

Ce travail d'analyse est en grande partie basé sur les travaux de [Colin Hardy.](https://www.youtube.com/channel/UCND1KVdVt8A580SjdaS4cZg)

Ce malware a été conçu pour être le plus discret possible, lors de la première exécution, le code malveillant commence par attendre 12 à 14 jours avant de s'exécuter. ![Screenshot de la fonction](https://i.postimg.cc/Y2ZNCqJc/Group-1-1.webp)

Puis, il vérifie si le hostname de la machine contient *"solarwinds"* ou *"test"*, ou s'il correspond à une liste de noms d'hôte qui contient, par exemple, swdev.dmz, swdev.local, on peut donc imaginer que l'attaquant a eu accès au réseau local de SolarWinds et a pu collecter ces noms d'hôte... Tout cela dans le but d'éviter que le malware ne se déclenche sur un émulateur d'un AV et qu'il soit détecté.

![Deuxième screenshot](https://i.postimg.cc/d0V8cwKf/Group-2-6.webp)

Le malware va ensuite vérifier si, dans la liste des processus actifs sur la machine, un ou plusieurs correspond à une liste qui contient les noms de processus d'antivirus (f-secure gatekeeper, carbonblack), de Command and Control (csagent, csfalconcontainer) - probablement afin de ne pas infecter une machine qui le serait déjà - de logiciels de virtualisation (vboxservice) et même d'analyse réseau (wireshark, tcpdump). Tout cela dans la but de rester le plus discret possible.

Puis, un userID est créé, il est généré à partir du hostname de la machine, du MachineGuid et de l'adresse MAC

[![Group-3.webp](https://i.postimg.cc/htfSk55r/Group-3.webp)](https://postimg.cc/SnbF8Dq2)

Le code malveillant fait ensuite appel au domaine *avsvmcloud.com*, il génère une URL avec la fonction suivante

![Group-5.webp](https://i.postimg.cc/NFngF8yT/Group-5.webp)

Cette URL est composée du domaine *eu-west-1.appsync-api.avsvmcloud.com* (la *eu-west-1* peut aussi être *us-west-2*, *us-east-1* ou *us-east-2*, le choix est fait aléatoirement) et d'un sous domaine qui est généré par la fonction DecryptShort à partir du UserID généré plus tôt et du hostname de la machine. C'est à partir de ce sous-domaine que la machine communique avec le C2.

Je n'irais pas plus loin dans l'analyse de ce malware, la partie communication avec le C2 étant relativement complexe et peu intéressante selon moi.

## Conclusion

Le 10 juin 2021, le spécialiste en cybersécurité Kaspersky publie un article dans lequel il indique que la backdoor de Sunburst a beaucoup de similitude avec une autre nommée Kazuar, une backdoor qui a été attribuée à la Russie. Cette attaque pourrait donc etre appuyée par le FSB. Le 29 janvier 2021, Brandon Wales, dirigeant du CISA a révélé dans le [Wall Street Journal](https://www.wsj.com/articles/suspected-russian-hack-extends-far-beyond-solarwinds-software-investigators-say-11611921601) que 30 % des victimes de l’attaque ne seraient pas clientes de SolarWinds, cette attaque pourrait donc etre seulement la face visible d'une grande opération de cyberespionnage.

Merci beaucoup d'avoir lu cette article, si vous avez des questions / remarques, n'hésitez pas à m'en faire part [ici](https://twitter.com/eban_non/status/1358429605376458752) ou par mail à [contact@eban.bzh](mailto:contact+blog@eban.bzh)

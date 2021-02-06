# SolarWinds, l'arbre qui cache la forêt 1/2

## Avant propos

Cet article a pour but de retracer les évènements à propos de la récente attaque dont SolarWinds a été victime, les évènements étant relativement récents à l'heure où j'écris cet article (06/02/2021) des mises à jour seront sûrement apportées à cet article.

## Signal d'alarme

Le 08 décembre 2020, Kevin Mandia, PDG de la société FireEye poste un communiqué nommé [FireEye Shares Details of Recent Cyber Attack, Actions to Protect Community](https://www.fireeye.com/blog/products-and-services/2020/12/fireeye-shares-details-of-recent-cyber-attack-actions-to-protect-community.html) dans lequel il informe que l'entreprise a été victime d'une cyberattaque de la part d'un "acteur hautement sophistiqué" et que ce dernier avait accédé à leur réseau interne et volé un grand nombre d'outils de Red Team de la société. Ce communiqué fait aussi part du fait que 

> sa discipline, sa sécurité opérationnelle et ses techniques nous conduisent à penser que [l'acteur malveillant derrière cette attaque] était soutenu par un état

Matt Gorham le directeur adjoint de la division cyber du FBI indique dans la foulée

> Le FBI enquête sur l'incident  et les premières constatations montrent un acteur avec un haut niveau de sophistication conforme à un État-nation

Ce qui semble donc confirmer les dires de FireEye.

Le 08 décembre 2020 à 20h11, dans [un article](https://www.nytimes.com/2020/12/08/technology/fireeye-hacked-russians.html) le New York Times suppute que 

> Ce piratage soulève la possibilité que les agences de renseignement russes aient vu un avantage à monter l'attaque alors que l'attention américaine - y compris celle de FireEye - était concentrée sur la sécurisation du système des élections présidentielles.

Sans pour autant apporter de preuve tangible.

Le 13 décembre 2020, coup de tonnerre, FireEye indique dans [ce communiqué](https://www.fireeye.com/blog/products-and-services/2020/12/global-intrusion-campaign-leverages-software-supply-chain-compromise.html) que l'attaque qu'ils ont subi a été propagée par le système de mise à jour d'Orion, un logiciel de gestion de réseau édité par SolarWinds, un cheval de Troie nommé Sunburst avait été inséré dans les version 2019.4 HF 5, 2020.2 et 2020.2 HF 1 d'Orion. Microsoft, les départements américains du Commerce, du Trésor, de l'Énergie et plus encore ont déclaré avoir été victimes de cette cyberattaque.

## Un peu de reverse engineering

Si vous n'êtes pas intéressé par la partie technique, cliquez ici.

Ce travail d'analyse est en grande partie basé sur les travaux de [Colin Hardy.](https://www.youtube.com/channel/UCND1KVdVt8A580SjdaS4cZg)

Ce malware a été conçu pour être le plus discret possible, lors de la première exécution, le code malveillant commence par attendre 12 à 14 jours avant de s'exécuter. ![Screenshot de la fonction](https://i.postimg.cc/Y2ZNCqJc/Group-1-1.png)

Puis, il vérifie si le hostname de la machine contient `solarwinds` ou `test` ou si il correspond à une liste de noms d'hôte qui contient, par exemple, swdev.dmz, swdev.local, on peut donc imaginer que l'attaquant a eu accès au réseau local de SolarWind et a pu collecter ces noms d'hôte... Tout cela dans le but d'éviter que le malware ne se déclenche sur une machine de test et qu'il soit détecté. 

![Deuxième screenshot](https://i.postimg.cc/q7kPmdXR/Group-2-5.png)

Le malware va ensuite vérifier si, dans la liste des processus actifs sur la machine, un ou plusieurs correspond à une liste qui contient les noms de processus d'antivirus (f-secure gatekeeper, carbonblack), de Command and Control (csagent, csfalconcontainer) - probablement dans le but de ne pas infecter une machine qui le serait déjà - de logiciel de virtualisation (vboxservice) et même d'analyse réseau (wireshark, tcpdump). Tout cela dans la but de rester le plus discret possible.

Le code malveillant fait ensuite un appel au domaine `avsvmcloud.com`, domaine que nous analyserons de plus près dans un prochain article qui paraîtra la semaine prochain, nous verrons aussi le fonctionnement de SUPERNOVA, une autre backdoor implémentée dans le logiciel Orion.

Merci beaucoup d'avoir lu cet article, si vous avez des questions, des remarques à apporter n'hésitez pas à le faire [ici](https://twitter/blablabla)

sources: https://www.nytimes.com/2020/12/08/technology/fireeye-hacked-russians.html https://www.fireeye.com/blog/products-and-services/2020/12/fireeye-shares-details-of-recent-cyber-attack-actions-to-protect-community.html

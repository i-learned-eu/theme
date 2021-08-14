Author: Eban 
Date: 2021/08/12
Keywords: sécurité
Slug: pegasus
Summary: Le 18 juillet 2021 à 19h, Amnesty International révèle dans une enquête en collaboration avec Forbidden Stories que le logiciel Pegasus, édité par la société israélienne NSO Group, a été utilisé à des fins d'espionnage contre des militants politiques, des journalistes, des membre d'ONG etc. Nous analyserons dans cet article l'aspect technique du spyware Pegasus dans sa version pour iOS.
Title: Pegasus, à la croisée du technique et du politique

Le 18 juillet 2021 à 19h, [Amnesty International](https://www.amnesty.org/en/) révèle dans une enquête en collaboration avec [Forbidden Stories](https://forbiddenstories.org/) que le logiciel Pegasus, édité par la société israélienne [NSO Group](https://www.nsogroup.com/), a été utilisé à des fins d'espionnage contre des militants politiques, des journalistes, des membres d'ONG etc. On apprendra quelques jours plus tard que l'État marocain a acheté à NSO sa solution d'espionnage afin de placer sur écoute de nombreux ministres français, mais aussi Edwy Plenel, Eric Zemmour ou encore Emmanuel Macron. Ce logiciel avait déjà été mis sous le feu des projecteurs en 2016 par [Citizen Lab](https://citizenlab.ca/) pour dénoncer le même genre de pratiques. Nous analyserons dans cet article l'aspect technique du spyware Pegasus dans sa version pour iOS.

# Première révélations, 2016 − Trident

En 2016, la société Lookout publie [un whitepaper](https://info.lookout.com/rs/051-ESQ-475/images/lookout-pegasus-technical-analysis.pdf) détaillant le fonctionnement technique de Pegasus sur iOS. Le mode opératoire de ce spyware est relativement simple, un message contenant un lien est envoyé à la cible, lorsque la cible clique sur le lien une faille 0day est exploitée sur le téléphone de la victime, et le spyware s'installe. 

![Schéma montrant une infection par un lien vérolé.](/static/img/pegasus/Infection_via_clic_sms.png)

Afin d'infecter le téléphone de la victime, le malware Pegasus utilise trois vulnérabilités différentes, la première est la [CVE-2016-4657](www.phrack.org/papers/attacking_javascript_engines.html). − Une CVE est une faille de sécurité rendue publique, c'est l'acronyme de Common Vulnerabilities and Exposures. − Cette CVE consiste en une vulnérabilité dans la façon qu'a Webkit, le moteur de rendu de page web utilisé par iOS, d'interpréter le JavaScript, et plus particulièrement dans la fonction `arrayProtoFuncSlice` qui permet simplement de couper un array à un endroit précis. 

```diff
var a = [1, 2, 3, 4];
var s = a.slice(1, 3);
// s = [2, 3]
```

Grace à cette vulnérabilité que nous ne verrons pas en détail ici étant donné la complexité de son fonctionnement, un code JavaScript malveillant peut écrire à des endroits dans la mémoire auxquels il ne devrait pas avoir accès, ainsi un attaquant peut exécuter du code directement sur le système depuis une page web.

Une fois cette faille exploitée, Pegasus en utilise une seconde, la [CVE-2016-4655](https://jndok.github.io/2016/10/04/pegasus-writeup/).

Pour appréhender cette vulnérabilité, il est nécessaire de comprendre ce qu'est le `Kernel ASLR`. Lorsque l'on cherche à attaquer un système et plus spécifiquement lorsque l'on cherche à pivoter du [kernel land vers le userland](https://beta.hackndo.com/le-monde-du-kernel/), il peut être intéressant de connaitre la position (l'adresse) du [Kernel](https://fr.wikipedia.org/wiki/Noyau_de_syst%C3%A8me_d%27exploitation) dans la RAM, si cette adresse était statique il serait trivial de l'obtenir. Pour éviter cela, il existe une fonction appelée KASLR (Kernel Address Space Layout Randomization, littéralement randomisation de l'espace d'adressage du noyau). Avec KASLR, à chaque redémarrage de l'appareil, l'adresse du kernel est décalée d'une valeur aléatoire, appelée `kernel slide`, générée par le [bootloader](https://en.wikipedia.org/wiki/Bootloader). Cette fonctionnalité n'est pas spécifique à iOS, elle est aussi présente sous Linux, BSD (donc MacOS) et Windows.

La CVE-2016-4655 permet donc à un attaquant de calculer ce `kernel slide` et donc la position du Kernel en RAM, ce qui sera utile pour exploiter la dernière CVE de notre triptyque, la [CVE-2016-4656](https://jndok.github.io/2016/10/04/pegasus-writeup/).

Cette CVE est une vulnérabilité de type `Use-After-Free`, de référencer un endroit de la mémoire libéré, mais dont l’adresse serait encore présente dans le code. L'exploit arrive ensuite à écraser l'objet présent à cette adresse et forcer l'exécution d'un code malveillant, qui aura donc des privilèges élevés, en l'occurence, il sera niveau du Kernel. Une fois ces privilèges acquis, Pegasus peut pivoter afin d'obtenir des privilèges d'aministrateur, jailbreaker l'appareil, s'installer avec ces dits privilèges d'administrateur et ainsi pouvoir espionner les conversations de l'utilisateur.

![Schema montrant le principe d'une vulnérabilité UFA](/static/img/pegasus/Use_after_free(1).png)

Afin de rester le plus discret possible, l'adresse du C2 ([Command & Control](https://whatis.techtarget.com/fr/definition/Commande-et-controle), le serveur central chargé d'envoyer des commandes au téléphone et de recevoir les informations) est dissimulée dans un SMS apparemment anodin d'authentification d'un compte Google.

![Your Google Verification code is:5678429 http://gmail.com/?z=G&i=1:aalaan.tv:443,1:manoraonlinu.nut:443&s=Λ�=&�](/static/img/pegasus/SMS_C2.png)

On peut voir que dans le paramètre `i`, l'adresse du C2 est caché. D'après les analyses de Lookout, le dernier chiffre du code de vérification correspondrait au "numéro d'instruction", ici `9`. Ainsi, même en l'absence d'accès à internet il est possible pour NSO Group d’interagir avec un téléphone infecté.

Pour parvenir à ses fins, Pegasus utilise donc trois `0day` différentes ! Ceci démontre bien la sophistication avancée du logiciel de la firme israélienne. L'utilisation de trois failles `0day` montrent aussi que les moyens financiers  mis en place pour créer Pegasus sont extrêmement importants.

![La CVE-2016-4657 permet d'obtenir une RCE, puis la CVE-2016-4655 permet de trouver le kernel slide. Enfin, la CVE-2016-4656 permet de jailbreak l'appareil et d'installer Pegasus](/static/img/pegasus/Infection_Pegasus(1).png)

# Une affaire d'une ampleur tentaculaire, 2021 − Megalodon

Le 18 juin 2021 la cellule investigation d'Amnesty International révélait donc dans un [whitepaper](https://www.amnesty.org/en/latest/research/2021/07/forensic-methodology-report-how-to-catch-nso-groups-pegasus/) le nouveau mode opératoire de Pegasus, et en particulier l'existence de l'exploitation de failles dites `0click`. Cette vulnérabilité permet à un attaquant, par un simple iMessage, d'infecter un téléphone. Amnesty a pu récupérer depuis des sauvegardes iCloud un certain nombre d'[adresse mail](https://github.com/AmnestyTech/investigations/blob/master/2021-07-18_nso/emails.txt) correspondant aux compte iCloud utilisés pour infecter les téléphones cibles.

Pour se camoufler, Pegasus utilise pour le nom de ses processus des noms très similaires à ceux utilisés par iOS.

En voici quelques exemples

|Nom de processus utilisé par Pegasus|Nom de processus original       |
|---------------------------------------|--------------------------------|
|ABSCarryLog                            |ASPCarryLog                     |
|aggregatenotd                          |aggregated                      |
|ckkeyrollfd                            |ckkeyrolld                      |
|com.apple.Mappit.SnapshotService       |com.apple.MapKit.SnapshotService|
|com.apple.rapports.events              |com.apple.rapport.events        |
|CommsCenterRootHelper                  |CommCenterRootHelper            |

Le Security Lab d'Amnesty a aussi pu détecter que des applications comme Apple Music on été utilisées comme des vecteurs d'attaque.

vx-underground a publié [des fichiers](https://twitter.com/vxunderground/status/1418207502974525441?s=20) qui, selon leurs dires, seraient la version pour Android de Pegasus, cependant, la société [ZecOps](https://www.zecops.com/) a pu analyser ces fichiers qui, [selon eux](https://twitter.com/ZecOps/status/1418954109768531968?s=20), n'appartiendraient pas à Pegasus.

L'ensemble de ces nouvelles techniques restent relativement floues, en effet, Amnesty International n'a pas pu récupérer le binaire de Pegasus pour l'analyser, celui-ci étant chiffré. Sans cette rétro-ingénierie, aucune CVE n'a pu être publiée.

# Au delà de la technique

*Le paragraphe qui suit, plus politique, est un éditorial, il ne reflète que l'avis de son auteur.*

Au delà de l'aspect technique, cette affaire est avant tout politique. Elle montre une fois de plus qu'à l'ère d'un monde toujours plus informatisé, toujours plus mondialisé, il est aisé pour les services de renseignement d'états anti-démocratiques − comme celui du Maroc qui, [d'après Amnesty International](https://www.lemonde.fr/projet-pegasus/article/2021/07/22/projet-pegasus-emmanuel-macron-convoque-un-conseil-de-defense-exceptionnel_6089148_6088648.html) aurait acheté sa solution à NSO Group − d'espionner à peu près n'importe qui à l'autre bout de la planète. L'affaire Pegasus montre enfin que, malgré l'avis général de la population [contre](https://www.amnesty.org/fr/latest/news/2015/03/global-opposition-to-usa-big-brother-mass-surveillance/) la surveillance des communications électroniques, les gouvernements des différents pays continuent d'opérer ces pratiques dans le plus grand secret. Cette distance, entre l'avis de la majorité de la population et les décisions prises par nos gouvernements est le signe de la défaillance de nos systèmes politiques.

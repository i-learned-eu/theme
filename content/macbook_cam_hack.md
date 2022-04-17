lang: fr
Title: Comment pirater la webcam d'un macbook sans allumer la LED ?
Keywords: Macbook, WebCam, cam, led, driver, hacking, spying, électronique
Date: 2022/01/09
Author: Ownesis
Summary: Dans cet article, nous allons voir ensemble comment des chercheurs ont réussi à activer la Webcam d'un macbook sans avoir de témoin lumineux.
Slug: macbook_cam_hack
Category: Cybersécurité/Red Team

Aujourd'hui on va parler hacking, espionnage, électronique et Macbook.
Ça donne envie n'est-ce pas 👀 ?

- Est-ce que l'exploit de LUX dans la série STALK saison 1 est possible et ou a été réalisable ?
- Est-ce qu'Orelsan a bien raison de se méfier de [sa](https://www.youtube.com/watch?v=B9F0e5gUmxY) webcam ?
- Est-ce que Mark Zuckerberg fait bien de mettre du ruban adhésif sur son Macbook ?

Je ne vais pas vous expliquez par qui et quand et pourquoi est ce que cette faille a été découverte.
Je vous laisse regarder [cette vidéo de Micode](https://www.youtube.com/watch?v=5FNm4ZRNJMk) qui explique l'histoire et vulagarise la théorie de l'exploit.

Sur les MacBook de 2008, on retrouve une configuration bien particulière pour la gestion de la caméra et de sa LED (qui "témoigne" de son activité).

![Macbook camera schematic](static/img/macbook_cam_hack/schematic.webp)

On retrouve **4** éléments bien distinctifs :
 1. Un "Support de stockage" [EEPROM](https://fr.wikipedia.org/wiki/Electrically-erasable_programmable_read-only_memory)
 2. Le capteur de la caméra (MT9V112)
 3. Une [LED](https://fr.wikipedia.org/wiki/Diode_%C3%A9lectroluminescente)
 4. Un [micro contrôleur](https://fr.wikipedia.org/wiki/Microcontr%C3%B4leur) (EZ-USB)


### L'EEPROM
EEPROM signifie **E**lectrically-**E**rasable **P**rogrammable **R**ead-**O**nly **M**emory (Mémoire morte effaçable électriquement et programmable)

> Mémoire morte veut dire que ce qui est stocké dans cette mémoire, ne sera pas supprimé si celle ci n'est plus alimentée, contrairement à la mémoire vive (RAM) qui s'efface une fois qu'elle n'est plus alimenté

Pour être honnête je ne connais pas trop son utilité ici, probablement elle qui stock le code (firmware) du capteur (j'en doute car, ce n'est pas donnée d'effacer la mémoire d'une EEPROM pour en changer le contenu, mais le fait qu'il soit connecté avec le micro contrôleur USB, le doute m'habite, vous verrez plus tard pourquoi).

### Le capteur de la caméra
Ici, c'est le capteur, donc ce qui capte les images, etc.
Il a **5** E/S (**E**ntrée/**S**ortie) :

 - **SCL** (1) et **SDA** (2) sont les E/S du protocole [I2C](https://fr.wikipedia.org/wiki/I2C), c'est un protocole qui permet l'échange d'informations/de données entre micro contrôleur, etc.
 - **DOUT[7:0]** (3) Sont 8 PIN qui sont connectés avec le micro contrôleur USB, aucune idée de leur utilité, mais ils permettent aussi de configurer/échanger avec le micro contrôleur.
 - **RESET** (4) Surement pour réinitialiser les paramètres du capteur.
 - **STANDBY** (5) L'une des parties de la faille. Il permet de dire au capteur s'il doit se mettre en mode veille ou non.

Parlons plus en détail du fameux PIN "**STANDBY**" :
Lorsque celui-ci reçoit du courant, le capteur arrête la capture et l'envoie d'images, il se met en Standby (en veille).
Mais lorsque celui ci ne reçoit plus de courant, il commence la capture et envoie les images.

### La LED
Ce composant permet de diffuser une lumière d'une certaine couleur lorsque que du courant passe. Cette LED à sa propre source de courant, elle est reliée au micro contrôleur USB (qu'on verra plus tard) et au capteur.

### Le micro contrôleur
Lui, c'est le maitre de tous les composants qu'on vient de voir, c'est lui qui "contrôle" le capteur et la LED.
Il a aussi `5` E/S:

 - **SCL** (1) et **SDA** (2), ce sont la même chose que pour le capteur, sauf que c'est le micro contrôleur qui donne le "tempo" pour l'envoie et la réception de données, **SCL** c'est pour le cycle de l'horloge, c'est le micro contrôleur USB qui donne ce cycle à l'EEPROM et au capteur.
 - **FD[7:0]** (3), comporte 8 PIN et sont connecté aux 8 PINs de **DOUT** du capteur.
 - **PA0** (4), C'est lui qui "active" le **RESET** du capteur en envoyant ou non du courant.
 - **PD3** (5), Le PIN qui permet en plus d'activer ou de désactiver le mode veille (**STANDBY**) du capteur, permet aussi d'allumer ou non la LED.

Vu que la LED a sa propre source d'énergie et est "constamment alimentée", pour l'éteindre, il faut soit :

 1. Couper la source d'énergie
 2. Envoyer du courant à la cathode (au "MOINS") de la LED. *L'anode étant le "PLUS" qui est connecté à la fameuse source d'énergie.*

La solution `2` est utilisé ici.
> Si on envoie du courant des 2 cotés de la LED, les électrons ne pourront plus circuler donc la LED ne sera plus alimenté.
> *Pour faire court, un circuit électrique doit toujours être "bouclé", les électrons devront toujours, (dans le sens conventionnel du courant), aller du positive (PLUS '+') vers le négative (MOINS '-').*
> *Si on à du positive vers du positive ou négative vers négative, on "casse" cette boucle, donc le courant ne circulera plus et n'alimentera plus les composants.*

La cathode de la LED est relié aux broches "**STANDBY**" du capteur et "**PD3**" du contrôleur USB.
Donc, si le port **PD3** envoie du courant, ça aura pour effet d'**ETEINDRE** la LED, et d'activer le mode veille du capteur (donc ne plus capturer et partager les images).
Tandis que si le port **PD3** n'envoie pas de courant, alors, le circuit de la LED se "boucle", alors la LED s'**ALLUME** et le capteur n'est plus en veille.

> Pour ceux qui ont un peu fait d'Arduino, le port **PD3** et comme configuré en **OUTPUT**, et mit en **LOW** pour allumer la LED et sortir du mode veille; et mit en **HIGH** pour éteindre la LED et activer le mode veille

Du coup, parfait me diriez-vous, LED allumé si le capteur en activité et LED éteinte si le capteur est en veille.

SAUF QUE ! Le mode veille est géré "logiciellement", c'est le firmware du capteur qui prend en compte le courant qui arrive ou non sur ce port **STANDBY**, et c'est le code du firmware qui permet de rentrer en mode veille ou non (capturer ou non les images)

> Pour ceux qui ont fait de l'Arduino, c'est comme si le firmware faisait un `DigitalRead(STANDBY)`, si c'est **HIGH** alors on se met en veille, si c'est **LOW** on commence la capture/envoie des images.

Le firmware par défaut d'Apple respecte le mode veille.
Il faut donc réussir à modifier ce code, mais comment faire ?!

Et bien, c'est "plutôt simple", il faut les connaissances évidement, mais l'envoie du firmware malveillant est assez simple finalement. Je m'explique.
Le capteur et le micro contrôleur USB n'ont pas de stockage permanent pour leurs firmwares (c'est pour ça que je ne sais pas trop à quoi sert l'EEPROM du schéma, *surement des paramètres plus ou moins constante pour le calibrage la colorimétrie du capteur ?*)
Du coup, à chaque fois que le driver de la caméra est chargé, le MacBook télécharge le firmware du **contrôleur USB** qui permet de configurer le capteur.
Le capteur n'a pas beaucoup de possibilité concernant sa configuration, mais il en a une, **LA** fonctionnalité en question qui rend possible cet exploit, le fait de ne pas prendre en compte le port **STANDBY**, autrement dit, pas de mode veille, qu'il y a du courant qui arrive ou non sur ce port, la caméra capturera et enverra les images en continu.
Mais il ne faut pas oublier de quand même envoyer du courant sur ce port (pour éteindre la LED ;) ).

Il faut donc trouver l'emplacement de ce firmware qui sera téléchargé sur le contrôleur USB pour le remplacer avec notre firmware fait maison et la cerise sur le gâteau, le pompon sur la Garonne, il n'était pas nécessaire d'avoir des droits administrateur pour remplacer ce firmware.

Vous l'aurez compris le Graal de cet exploit est le firmware "facilement" remplaçable, car il n'est pas codé en dur et est téléchargé à chaque chargement du driver de la caméra et le fait que n'importe quel utilisateur peut remplacer le firmware.

Je n'arrive pas à savoir ce qu'est le plus grave dans cette histoire :

 - Le fait qu'un utilisateur autre que l'administrateur puisse remplacer le firmware ?
 - Le fait que la configuration du capteur permet d'ignorer la mise en veille ?
 - Que la LED ne soit pas branchée autre part, part exemple sur la broche qui alimente le capteur ou sur la broche qui envoie les images capturées ?

Il y a sûrement de bonnes explications à ces questions ou de bonnes raisons à ce pourquoi cela a été pensé comme cela à cette époque.

Il existe toujours des webcams bas de gamme (même qui proposent une bonne qualité d'image) qui ont une LED, mais qui peut être TRÈS, voire TROP facilement désactivable, comment en modifiant un [registre Windows](https://ilearned.eu/registre.html) ou fichier sous Linux.

Mais maintenant les webcams ou les ordinateurs portables de nos jours sont mieux pensé et mieux sécurisé sur ça.

Mais comme l'explique Micode dans sa vidéo, à présent certains logiciels malveillant peuvent accéder à la webcam en même temps que vous, bon d'accord les méchants bonhommes de la NSA ou le vilain hackeur qui veut vous espionner pendant que vous êtes en live sur Twitch, auront cependant les captures de ce moment-là, et pas les images de ce qui se passe avant ou après le lancement de votre facecam, mais tout de même...

J'espère que cet article, vous a plus, article un peu technique, en parlant d'électronique/électricité  ça change un peu.
Mais j'espère que j'ai réussi à vous faire comprendre le fonctionnement de la Webcam et de sa LED sur les anciens Macbook, ainsi que leurs vulnérabilités.

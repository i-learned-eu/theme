Author: Eban 
Date: 2021/07/09
Keywords: automatisation, domotique
Slug: mqtt
Summary: Si vous vous êtes déjà intéressé⋅e à la domotique, vous avez sûrement entendu parler du protocole MQTT (Message Queuing Telemetry Transport), MQTT est un protocole très utilisé pour faire de l'automatisation notamment, nous allons entrer plus en profondeur dans le fonctionnement d'MQTT dans cet article.
Title: MQTT, comprendre le standard de la domotique

Si vous vous êtes déjà intéressé⋅e à la domotique, vous avez sûrement entendu parler du protocole MQTT (Message Queuing Telemetry Transport), MQTT est un protocole très utilisé pour faire de l'automatisation notamment, nous allons entrer plus en profondeur dans le fonctionnement d'MQTT dans cet article à travers l'exemple d'une lampe connectée.

MQTT fonctionne sur le principe de `Topics` dans lesquels les différents appareils peuvent publier ou recevoir des messages. La fonctionnement de ce protocole est relativement simple, le client commence par s'authentifier auprès du serveur, puis il peut recevoir et/ou envoyer des messages au serveur, appelé `Broker`, voici un exemple de trame réseau.

![Trame réseau MQTT](/static/img/mqtt/MQTT_Trame_rseau.webp)

On peut donc voir que ce protocole est très simple de fonctionnement, et ce n'est pas un hasard qu'il soit très utilisé en domotique, bien souvent les appareils en domotique sont tout petits et n'ont pas la capacité d'implémenter des protocoles très lourd.

![Un exemple de communication avec MQTT](/static/img/mqtt/Exemple.webp)

Vous pouvez voir ci-dessus un exemple très simple d'utilisation du protocole MQTT, un téléphone publie un message au broker MQTT sur le topic `stat/phone` quand le réveil sonne, une lampe connectée est abonnée au topic `stat/phone`, quand un message indiquant qu'une alarme vient de sonner lui parvient, elle s'allume et indique par un message sur le topic `stat/lampe/POWER` qu'elle est allumée. Ce scénario est très simple mais il montre à quel point MQTT est modulable et peut permettre une automatisation poussée. Si vous êtes intéressé⋅e par la domotique, sachez qu'il existe des petits modules appelés modules [Sonoff](https://fr.aliexpress.com/item/33061230430.html) qui permettent de rendre "connecté" n'importe quel appareil électrique (une lampe de chevet par exemple) et qui, une fois un firmware (système d'exploitation) spécial appelé [Tasmota](https://tasmota.github.io/) flashé permettent aussi de publier des messages sur un broker MQTT. Si vous n'êtes pas un aficionado de la ligne de commande, il existe des logiciels comme [Node-RED](https://nodered.org/) ou [Automate](https://play.google.com/store/apps/details?id=com.llamalab.automate&hl=fr&gl=US) sur Android qui permettent de s'essayer à la domotique et l'automatisation facilement.

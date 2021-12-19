Author: Eban
Date: 2021/12/18
Keywords: réseau, sécurité
Slug: upnp
Summary: On entend souvent parler d'UPnP (Universal Plug and Play) comme étant un protocole représentant une faille de sécurité béante permettant de changer la configuration du NAT d'à peu près n'importe quel routeur, dans cet article nous détaillerons le fonctionnement de ce protocole afin de mieux comprendre son fonctionnement et la vulnérabilité qu'il représente.
Title: UPnP un protocole dangereux, vraiment ?

On entend souvent parler d'UPnP (Universal Plug and Play) comme étant un protocole représentant une faille de sécurité béante permettant de changer la configuration du NAT d'à peu près n'importe quel routeur, dans cet article nous détaillerons le fonctionnement de ce protocole afin de mieux comprendre son fonctionnement et la vulnérabilité qu'il représente.

Avant toute chose, il est important de savoir qu'UPnP est un protocole destiné à être utilisé dans les réseaux domestiques et de petites entreprises (les réseaux dits SOHO, Small Office Home Office). Il n'est donc bien souvent pas présent sur les routeurs moins grand publics.

UPnP a été créé afin de faciliter la découverte des différents services sur un réseau, comme les imprimantes, un partage de fichier en réseau etc. Quand un appareil se connecte à un réseau utilisant UPnP, tous ces services sont détectées automatiquement.

Avec UPnP, chaque appareil sur le réseau (appelé périphérique) contient une liste de services ainsi que leurs caractéristiques sous la forme d'un fichier XML. Les chromecast par exemple (petits appareils créés par Google pour pouvoir "envoyer" des vidéos sur sa TV) utilise UPnP pour annoncer sa présence. 

```xml
<root
	xmlns="urn:schemas-upnp-org:device-1-0">
	<specVersion>
		<major>1</major>
		<minor>0</minor>
	</specVersion>
	<URLBase>http://10.XXX.XXX.XXX:8008</URLBase>
	<device>
		<deviceType>urn:dial-multiscreen-org:device:dial:1</deviceType>
		<friendlyName>XXXXXXXXXX</friendlyName>
		<manufacturer>Google Inc.</manufacturer>
		<modelName>Eureka Dongle</modelName>
		<UDN>uuid:b9c125d5-XXXX-XXXX-XXXX-XXXXXXXXXXXX</UDN>
		<iconList>
			<icon>
				<mimetype>image/png</mimetype>
				<width>98</width>
				<height>55</height>
				<depth>32</depth>
				<url>/setup/icon.png</url>
			</icon>
		</iconList>
		<serviceList>
			<service>
				<serviceType>urn:dial-multiscreen-org:service:dial:1</serviceType>
				<serviceId>urn:dial-multiscreen-org:serviceId:dial</serviceId>
				<controlURL>/ssdp/notfound</controlURL>
				<eventSubURL>/ssdp/notfound</eventSubURL>
				<SCPDURL>/ssdp/notfound</SCPDURL>
			</service>
		</serviceList>
	</device>
</root>
```

On voit ici que le périphérique indique son nom, constructeur etc, mais aussi une liste de services, qui ici ne contient qu'un seul service qui ici est le "cast" appelé "dial-multiscreen-org". Comme vous l'avez peut-être remarqué, UPnP utilise HTTP pour récupérer le fichier XML.

Afin de permettre aux périphériques d'*annoncer* leurs différents services etc, le protocole SSDP est utilisé, ce protocole permet à un élément qu'on appelle le point de contrôle (control point en anglais) de maintenir une liste des différents périphériques UPnP pour que chaque nouvel appareil qui se connecte sur le réseau puisse obtenir l'ensemble des périphériques du réseau sans interroger tous les appareils.

![Le client demande au serveur la liste des services](/static/img/upnp/requestList.png)

Enfin, tout appareil du réseau compatible peut interagir avec les autres appareils à l'aide du langage SOAP (qui utilise du XML) en passant par le point de contrôle à chaque fois.

![Le client envoie au service une action au travers du serveur](/static/img/upnp/action.png)

Malgré sa praticité et sa relative simplicité, est décrié pour son manque de performance et de sécurité pour diverses raisons :

- L'authentification : C'est bien simple, il n'y en a pas de base dans UPnP. Certaines tentatives ont été faites pour apporter de l'authentification à UPnP, mais ces solutions sont peu implémentées par les routeurs grand publique qui embarquent UPnP.
- UPnP IGD (Internet Gateway Device) : La fonctionnalité IGD permet de contrôler la configuration NAT de certains routeurs, et ainsi de mapper des ports sur une machine infectée. Cette facilité à mapper des ports représente de toute évidence une vulnérabilité car elle permet à un attaquant d'exposer une backdoor sur Internet.
- Multicast : UPnP utilise UPnP pour chercher des appareils, ce qui induit une consommation de bande passant non négligeable, mais aussi des problèmes sur certains réseaux qui utilisent l'IGMP snooping, qui est une méthode qui permet d'optimiser la diffusion des trames multicast, mais qui peut dans ce cas précis apporter des problèmes.

À cause de ces différents problèmes, UPnP est aujourd'hui peu implémenté et souffre d'une mauvaise réputation.
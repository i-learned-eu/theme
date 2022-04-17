lang: fr
Title: Usage des VLAN
Keywords: VLAN, network, réseau
Date: 2021-05-02
author: Ramle
summary: Aujourd'hui, on va parler du principe des VLAN et de l'utilité de celle-ci.
slug: vlan
Category: Réseau/Routage & IP

Souvent pour des raisons de sécurité ou par nécessité de priorisation du flux de certains appareils,  il est nécessaire de séparer le réseau en différentes parties, pour par exemple, séparer un réseau d'administration de serveurs et du matériel réseau avec le réseau destiné aux machines d'une entreprise. Dans ce cas deux solutions sont possible, soit utiliser plusieurs interfaces réseaux, soit faire des VLANs.

Les VLANs permettent de gérer de manière plus aisée de la segmentation de réseaux, le principe est de par exemple permettre à un switch réseau en fonction du port sur lequel est branché une machine d'être sur une VLAN différente, chaque VLAN possède un ID numérique pour l'identifier.

Un autre concept intéressant des VLAN, c'est le trunk, cela permet de faire passer plusieurs VLAN sur un seul port en tagant les paquets. Ce tag est rajouté dans l'en-tête ethernet  il contient l'ID de la VLAN dans laquelle le trafic doit aller. On peut aussi avoir des VLANs dites untagged, c'est à dire qui ne demande pas la modification de l'en-tête ethernet. Une VLAN untagged ne demande pas de configuration spécifique sur le client, c'est la VLAN "par défaut", contrairement à une VLAN tagged qui demande que le client rajoute l'information dans l'en-tête on ne peut donc avoir qu'une seule VLAN untagged.

On peut prendre un exemple du quotidien, la box de votre FAI, si vous avez une box pour la TV par exemple, il y a de forte chance que ce soit une VLAN séparée, cela permet de prioriser le trafic de la box TV afin d'éviter des coupures si vous téléchargez de gros fichiers par exemple. Ici, VLAN 10 est un VLAN taged et VLAN 20 est untagged, tout les appareils passent de base par VLAN 20.

![Schéma VLAN](/static/img/vlan/vlan.webp)

lang: fr
Author: Eban
Date: 2021/12/20
Keywords: Décentralisation
Slug: fediverse
Summary: Si vous vous êtes déjà intéressé à la décentralisation, vous avez sûrement déjà entendu parler du Fediverse, vendu par certain-e-s comme le futur des réseaux sociaux et décrit comme une invention de barbus par d'autres ; nous tenterons de faire la lumière sur ce qu'est le Fediverse dans cet article.
Title: Comment fonctionne le Fediverse ? Introduction à ActivityPub
Category: Pensées du libre

Si vous vous êtes déjà intéressé à la [décentralisation](https://ilearned.eu/decentralisation.html), vous avez sûrement déjà entendu parler du Fediverse, vendu par certain-e-s comme le futur des réseaux sociaux et décrit comme une invention de barbus par d'autres ; nous tenterons de faire la lumière sur ce qu'est le Fediverse dans cet article.

Le Fediverse est un ensemble de réseaux interconnectés à l'aide du protocole ActivityPub notamment.

![Il existe de nombreux services qui utilisent le Fediverse. Ils sont tous reliés entre eux par le protocole ActivityPub](/static/img/fediverse/overview.jpg)

*Image par Imke Senst, Mike Kuketz et RockyIII, CC-BY-SA 4.0*

Cette interconnexion a plusieurs avantages, premièrement, elle permet une décentralisation très importante, si un serveur Pleroma vient à être down, tous les autres contenus resterons accessibles. Alors qu'aujourd'hui, et on l'a bien vu récemment avec la panne de Facebook, si un gros acteur tombe, un pan entier d'internet devient inaccessible.

Le second avantage, est que si je commente une photo sur Pixelfed par exemple, mon commentaire sera visible depuis une instance Mastodon. Les contenus sont partagés entre les différentes instances du Fediverse, même si elles n'utilisent pas le même logiciel.

Le protocole permettant cette interconnexion est **ActivityPub** ce protocole permet l'échange d'informations entre les instances en exploitant le format **ActivityStream**.

## 📁 ActivityStream

Le format ActivityStream est un standard basé sur le format JSON permettant de déclarer des **objets**. Par exemple, ci-dessous un objet Person qui correspond à un profil utilisateur sur Mastodon.

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "PropertyValue": "schema:PropertyValue",
      "value": "schema:value"
    }
  ],
  "id": "https://mastodon.social/users/Gargron",
  "type": "Person",
  "attachment": [
    {
      "type": "PropertyValue",
      "name": "Patreon",
      "value": "<a href=\"https://www.patreon.com/mastodon\" rel=\"me nofollow noopener noreferrer\" target=\"_blank\"><span class=\"invisible\">https://www.</span><span class=\"\">patreon.com/mastodon</span><span class=\"invisible\"></span}"
    },
    {
      "type": "PropertyValue",
      "name": "Homepage",
      "value": "<a href=\"https://zeonfederated.com\" rel=\"me nofollow noopener noreferrer\" target=\"_blank\"><span class=\"invisible\">https://</span><span class=\"\">zeonfederated.com</span><span class=\"invisible\"></span}"
    }
  ]
}
```

Et ici un objet encore plus classique appelé "Note", il est accepté par un grand nombre de services du Fediverse.

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "toot": "https://joinmastodon.org/ns#",
    }
  ],

  "id": "https://example.com/@alice/hello-world",
  "type": "Note",
  "content": "Hello world"
}
```

Comme vous pouvez le voir, certaines propriétés prennent en valeur des balises HTML (🤮). Le fonctionnement du format ActivityStream est vraiment trivial.

## 🌐 ActivityPub

Avoir un format de fichiers, c'est bien beau, mais encore faut-il pouvoir partager ces fichiers.

ActivityPub normalise certains objets, comme l'objet Person qui se voit affublé de nombreuses valeurs comme les followers, l'image de profil, etc.

```json
{
  "@context": ["https://www.w3.org/ns/activitystreams",
               {"@language": "ja"}],
  "type": "Person",
  "id": "https://kenzoishii.example.com/",
  "following": "https://kenzoishii.example.com/following.json",
  "followers": "https://kenzoishii.example.com/followers.json",
  "liked": "https://kenzoishii.example.com/liked.json",
  "inbox": "https://kenzoishii.example.com/inbox.json",
  "outbox": "https://kenzoishii.example.com/feed.json",
  "preferredUsername": "kenzoishii",
  "name": "石井健蔵",
  "summary": "この方はただの例です",
  "icon": [
    "https://kenzoishii.example.com/image/165987aklre4"
  ]
}
```

ActivityPub normalise aussi bien les communications client/serveur que serveur/serveur. Avec ce protocole, un utilisateur est appelé "acteur", il a deux "boîtes", une boite d'envoi et une boite de réception. Les URL de ces deux boites sont indiquées dans l'objet Person correspondant.

Le fonctionnement est assez trivial, pour recevoir les messages, les différentes instances qui veulent poster un message auprès de l'acteur envoient une requête HTTP POST contenant les nouveaux messages. Ledit acteur peut ensuite, via une requête HTTP GET récupérer le contenu de son Inbox. Ensuite, si l'acteur veut poster un message, il peut envoyer une requête POST à l'outbox et les autres acteurs pourront consulter cette outbox avec une simple requête GET.

Si Alice veut envoyer un message à Bob, elle poste simplement son message dans son outbox avec le destinataire, l'instance d'Alice s'occupera d'aller trouver l'inbox de Bob et d'acheminer le message vers cette inbox.

![Schéma détaillant les informations ci-dessus.](/static/img/fediverse/routing.webp)

Comme on a pu le voir, ActivityPub est un protocole plutôt simple dans son fonctionnement et qui permet d'interconnecter de nombreux services. Il s'appuie sur HTTPS, ce qui lui permet de bénéficier des dernières avancées de ce protocole comme la récente [version 3 de HTTP](https://ilearned.eu/http3.html).

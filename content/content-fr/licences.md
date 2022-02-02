Author: Rick
Date: 2022/01/25
Keywords: droit
Slug: comprendre-licences
Summary: La licence est une sorte de contrat qui permet d'expliquer les différentes utilisations que peuvent faire les utilisateurs du logiciel et du code source. Il en existe plusieurs types (libre, open source et propriétaire) avec certaines subtilités parfois (copyleft). 
Title: Comprendre les différentes licences

La licence est une sorte de contrat qui permet d'expliquer les différentes utilisations que peuvent faire les utilisateurs du logiciel et du code source. Il en existe plusieurs types (libre, open source et propriétaire) avec certaines subtilités parfois (copyleft). 

Je vais essayer ici d'expliquer clairement les différents concepts autour de ces licences ainsi que leurs différences. Et ce de la manière la plus claire possible, ce qui n'est pas chose aisée. Et j'essaierai de rester objectif.

# Le libre

Le libre est avant tout un mouvement politique et social (merci [Wikipedia](https://fr.wikipedia.org/wiki/Mouvement_du_logiciel_libre)) fondé en 1983 par Richard Matthew Stallman. Il promeut la liberté de l'utilisateur sur les logiciels, et cela se passe avec l'ouverture du code source. Un logiciel avec une licence libre doit pour ce faire respecter [4 libertés](https://www.gnu.org/philosophy/philosophy.fr.html):

 1. Exécuter le programme
 2. Étudier et modifier le programme (donc son code source)
 3. Redistribuer des copies du programme
 4. Redistribuer des versions modifiées

Si un logiciel respecte ces quatre libertés, il est donc libre. C'est le cas de LibreOffice, VLC, Linux, ou encore ce site ! [La FSF](https://fsf.org) est le principal organisme qui promeut le libre dans le monde. Elle se bat aussi en justice et aide les projets lorsque leurs licences libres ont été enfreintes. Elle fourni aussi un guide détaillant les nouvelles licences pour qu'elles puissent être utilisés dans des projets libres, en expliquant les libertés enfreintes ou non ainsi que les différentes compatibilités possibles. En France, il existe les associations [April](https://www.april.org/) et [Framasoft](https://framasoft.org/) (pour ne citer que les plus grosses) qui se chargent de promouvoir le libre.

Il existe nombreuses licences, voici une courte liste non exhaustive : GPL3, AGPL3, LGPL3, MIT, BSD, Apache 2.0, CC-BY... Chaque licence ayant certaines subtilités propres qu'on ne prendra pas le temps de traiter ici. Peut-être pour un prochain article ? ;)

Ce genre de licence peut s'appliquer aussi bien à du code qu'à des livres, des articles, de la documentation, des images, des vidéos...

# L'open source

L'open source a été créé à la fin des années 90 (1998). [L'OSI](https://opensource.org/) (pour Open Source Initiative) est l'organisme qui va approuver les licences comme Open Source. Une licence Open Source doit respecter [11 règles](https://opensource.org/osd). Elles se rapprochent du libre à une exception près. La règle 4 permet d'avoir des licences qui restreignent la redistribution du code source modifié et enfreint donc la 4e liberté.

> The license may restrict source-code from being distributed in modified form only if the license allows the distribution of "patch files" with the source code for the purpose of modifying the program at build time. [...]

Si le libre met en avant l'utilisateur et sa liberté, l'open source met en avant l'entreprise. Mettre son code en open source, c'est l'ouvrir dans un but productif, permettre à la communauté de l'améliorer pour le profit de l'entreprise.

# Le propriétaire

Les logiciels propriétaires sont tout simplement ceux qui ne rentrent dans aucune des deux précédentes catégories. Certaines licences sont tout à fait compréhensible moralement, mais qui ne sont pas libre au sens propre du terme. La licence de ce blog (CC-BY-NC-SA) interdit la redistribution payante des articles. Moralement compréhensible, mais pas libre pour autant, enfreignant ainsi la 3e liberté.
Certaines licences vont aussi interdire certains usages de leur logiciel (ne pas utiliser à but militaire, par de grosses entreprises...), en cassant donc la première liberté. Et les exemples sont encore nombreux !

Cependant, la plupart du temps, un logiciel propriétaire va tout juste redistribuer son **binaire** et non son code source. Ou va imposer de fortes contraintes sur son utilisation tout en faisant signer un contrat utilisateur, les fameuses cases "J'ai lu et j'accepte" surplombées par un long texte juridique. C'est le cas de Windows par exemple.

# Le copyleft

Le copyleft est quelque chose qui vient en plus de la licence. C'est pour ça qu'on nomme certaines licences "avec copyleft" et d'autres "sans copyleft". Le copyleft va forcer la réutilisation de la même licence sur des versions modifiées du code.

Par exemple, le code source pour Linux est en GPLv2. Si on modifie ce code, on doit appliquer la GPLv2 à cette nouvelle version. Le code source de Minix est sous licence BSD, qui n'a pas de copyleft. On peut donc reprendre ce code, le modifier et le rendre propriétaire.

# Conclusion

Si on peut résumer cet article :

 * Licence = contrat au sens juridique expliquant ce qu'on peut faire avec le programme et son code
 * Libre = 4 libertés
 * Open Source = 11 règles
 * Propriétaire = peut être bien moralement, mais surtout code fermé
 * Copyleft = type de licence "contaminante"

Il convient ensuite de choisir la bonne licence selon vos projets et vos convictions. 

Comme je l'ai indiqué plus haut, les licences (libres ou non) peuvent s'appliquer à des logiciels, des dessins, des vidéos ou encore du texte (comme des articles, de la documentation, un livre...). Cependant, certaines sont plus adaptées pour du code et d'autres pour du texte, de la musique, etc. Je ne suis pas rentré dans ces détails, car la philosophie derrière reste à peu près la même peu importe le support.

Voici quelques liens qui pourront vous êtres utiles :

 * [Liste non exhaustive des licences libres ou non d'après la FSF](https://www.gnu.org/licenses/license-list.html#SoftwareLicenses)
 * [Outil pour choisir une licence pour votre code facilement](https://ufal.github.io/public-license-selector/)
 * [Outil pour choisir facilement une licence pour vos œuvres de l'esprit n'étant pas du logiciel](https://creativecommons.org/choose/)

J'espère que j'ai été assez clair dans cet article en expliquant succinctement les différents types de licences. N'hésitez pas à me faire des retours (rick [at] gnous [dot] eu, ou en commentaires) pour que je puisse améliorer l'article / en faire un nouveau !

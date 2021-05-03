Title: Le soucis du DNS de son opérateur
Summary: Beaucoup de monde utilise le DNS par défaut de son opérateur, mais ce choix pose certains problème, c'est ce que l'on abordera aujourd'hui
Category: Today I Learned
slug: dns-fai
Date: 2021-05-03
author: Ramle
keywords: DNS, network, réseau, sécurité, fai

# Le soucis du DNS de son opérateur

Pour le moment, nous avons beaucoup abordé le DNS, avec différents moyens de sécuriser et les risques associés. Aujourd'hui, on va voir comment choisir correctement un résolveur, enfin pour être précis comment savoir le quel ne pas prendre.

Je suppose que vous avez résolu le NDD (nom de domaine) `blog.eban.bzh` grâce au DNS distribué par votre box, il y a fort à parier que vous ne l'ayez pas changé et donc que ce soit votre FAI qui répondent les requête, le problème étant que la plupart des gros FAI ne valide pas via DNSSEC. Souvent, ces DNS mentent sur base de demande faite par l'état, les listes sont d'ailleurs privées ce qui permettrai sans soucis de bloquer des sites totalement légitimes, c'est le cas de sci-hub par exemple, une plateforme qui partage des documents scientifiques.

Il y a aussi un autre problème, la confidentialité. En effet, le serveur distant peut voir toutes les requêtes faites par un client, dans le cas d'un FAI il peut théoriquement savoir précisément qui vous êtes. Ils sont (obligation légal) déjà en possession de votre identité liée à l'adresse IP. Il reste peut probable que les FAI le fassent vraiment, ça leur rajouterai un coup conséquent pour le stockage de logs, sans oublier les risques de sanction si il n'est pas stipulé dans les CGU (conditions générales d'utilisation) ce stockage des requêtes.

Il y aussi le problème de MITM, les DNS des opérateurs n'utilise pas de protocole comme DoH ou DoT, un pirate pourrait donc intercepter les requêtes.

Dans cet article, on s'est concentré sur les opérateurs, mais ces problèmes existent sur beaucoup de résolveur publique qui bien souvent, offrent peu de garantie quand à la confidentialité, ou l'authenticité des réponses.

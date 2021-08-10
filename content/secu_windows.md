Author: Lancelot
Date: 2021/07/01
Keywords: Windows, sécurité
Slug: secu_windows
Summary: "Accès refusé". S’il y a bien une erreur frustrante, c'est sûrement celle-ci. Sur Windows nous y sommes pourtant souvent confrontés, surtout dans une perspective attaquante. Dans cet article, je tâcherais de vous présenter, dans les grandes lignes, le modèle de sécurité qu’utilise Windows.
Title: Modèle de sécurité Windows

## Introduction

"Accès refusé". S’il y a bien une erreur frustrante, c’est sûrement celle-ci. Sur Windows nous y sommes pourtant souvent confrontés, surtout dans une perspective attaquante. En revanche, peu de gens comprennent pourquoi cette erreur (ou d’autres) vient s’immiscer dans sa confortable utilisation de son système d’exploitation.

Dans cet article, je tâcherais de vous présenter, dans les grandes lignes, le modèle de sécurité qu’utilise Windows, principalement les notions de privilège d’accès et de contrôle d’accès.

De manière générale, lorsque je parlerais d’objet Windows, je parlerais d’utilisateurs, de machines, de fichiers, ou encore de processus.

## Contexte de sécurité

Pour bien comprendre la suite, il est nécessaire de comprendre ce qu’est un contexte de sécurité chez notre ami Windows. Ce dernier désigne un ensemble d’attributs ou de règles de sécurité actuellement en vigueur pour reprendre la définition de Microsoft. Un contexte de sécurité se traduira par une structure de données particulières définis par la `SSPI` ("Security Support Provider Interface"), une `API` Windows écrite dans le but d’interagir avec le contexte de sécurité, elle est notamment utilisée, par exemple, pour l’authentification. Autrement dit, le contexte de sécurité définit les éléments de bases du système de sécurité de notre os favori (si c’est pas le cas faites comme si).

## SecurableObject

Un objet est dit "sécurisable" s’il a la capacité de posséder un descripteur de sécurité. De manières générales, énormément d’objet dans Windows sont des `SecurableObject`. Les processus, les clés de registre, les fichiers/répertoires, les objets ‘Active Directory’ et bien d’autres. Ils forment donc le cœur des interactions entre nous et le système d’exploitation. J’ai parlé des descripteurs de sécurité, ces derniers sont simplement des listes de plusieurs caractéristiques. Ils contiennent le `SID` ("Security Identifier", qui est un identifiant unique)  du propriétaire de l’objet, le `SID` du groupe propriétaire, et des `ACLs` pour "Access Control Lists". Les descripteurs de sécurité sont usuellement au format `SDDL` ("Security Descriptor Definition Langage") bien que peu reluisant, il est en réalité très pratique car simple d’utilisation (non pas de compréhension).

## Token d’accès

Lorsqu’un utilisateur Windows se connecte à son compte local (ou Active Directory) plusieurs informations seront alors stockés dans la mémoire. De manière assez évidente, il contiendra le condensat du mot de passe (sauf configurations très improbable ou un système relativement vieux et dans ces cas précis, ce sera le mot de passe en claire), son `SID`, le `SID` de son groupe, des privilèges d’accès (nous y reviendrons plus tard) et bien d’autres informations. On regroupe tout cela dans ce que l’on appelle un `token` d’accès. Ce dernier est alors gardé dans un processus un peu particulier appelé `LSASS.exe` pour "Local Security Autority SubSystem Service". Ce dernier est donc vital et très sensible.

![Une fois le mot de passe spécifié, un token est créé](/static/img/secu_windows/Auth LSASS.png)

Lorsqu'on interagit avec le système d’une quelconque manière, une copie de notre `token` d’accès est alors utilisée. Dans le cas d’un fichier, les informations que le `token` d’accès contient vont donc être comparées avec les informations contenues dans la `DACL` (qui est une liste contenant les accès, plus d’information  sur ce sujet un peu après) garantissant ou non un accès d’une certaine valeur. Il peut être destiné à de l’écriture, de la lecture ou bien même pour de l’exécution.

![Certaines informations du token sont comparées avec la DACL](/static/img/secu_windows/Principe d'accès.png)

Un cas plus intéressant est celui du démarrage d’un programme. En effet, ce dernier est lancé en tant qu’un utilisateur en particulier, il ne doit donc pas contourner ce fameux système d’accès. C’est pourquoi les processus sont considérés comme des `SecurableObject`, et dans cette situation, une copie de notre `token` d’accès est également donné et quand le programme interagira avec le système, il le fera bien selon les droits et l’identité de l’utilisateur connecté.

![Lorsque l'on créer un processus, on lui fournit notre token pour qu'il puisse l'utiliser](/static/img/secu_windows/Principe d'accès à un programme.png)

*La fonction [`CreateProcessA()`](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa) est une fonction de l'`API` Windows `kernel32.dll` qui permet de créer un nouveau processus.*

## Privilèges d’accès

Comme mentionné plus tôt, le `token` d’accès renferme en son sein un certain nombre de privilèges. Ces derniers sont attribués à chaque connexion, en fonction des règles de sécurité. Plus précisément, les privilèges d’accès sont donnés en fonction du groupe d’appartenance auquel on attribut des droits par défaut grâce aux `GPOs` locales (dans `gpedit.msc`, `Configuration Ordinateur \ Paramètres windows\ Paramètres de sécurité\ Stratégies local\ Attribution des droits utilisateur`). La liste de ces privilèges n’est pas présente sous forme d’énumération classique, en revanche voici une implémentation en PowerShell pour bien se rendre compte de l’ensemble de ces privilèges (issus de [PSReflect-Functions](https://github.com/jaredcatkinson/PSReflect-Functions)).
```powershell
$SecurityEntity = psenum $ENUM SecurityEntity UInt32 @{
	SeCreateTokenPrivilege =  1
	SeAssignPrimaryTokenPrivilege =  2
	SeLockMemoryPrivilege =  3
	SeIncreaseQuotaPrivilege =  4
	SeUnsolicitedInputPrivilege =  5
	SeMachineAccountPrivilege =  6
	SeTcbPrivilege =  7
	SeSecurityPrivilege =  8
	SeTakeOwnershipPrivilege =  9
	SeLoadDriverPrivilege =  10
	SeSystemProfilePrivilege =  11
	SeSystemtimePrivilege =  12
	SeProfileSingleProcessPrivilege =  13
	SeIncreaseBasePriorityPrivilege =  14
	SeCreatePagefilePrivilege =  15
	SeCreatePermanentPrivilege =  16
	SeBackupPrivilege =  17
	SeRestorePrivilege =  18
	SeShutdownPrivilege =  19
	SeDebugPrivilege =  20
	SeAuditPrivilege =  21
	SeSystemEnvironmentPrivilege =  22
	SeChangeNotifyPrivilege =  23
	SeRemoteShutdownPrivilege =  24
	SeUndockPrivilege =  25
	SeSyncAgentPrivilege =  26
	SeEnableDelegationPrivilege =  27
	SeManageVolumePrivilege =  28
	SeImpersonatePrivilege =  29
	SeCreateGlobalPrivilege =  30
	SeTrustedCredManAccessPrivilege =  31
	SeRelabelPrivilege =  32
	SeIncreaseWorkingSetPrivilege =  33
	SeTimeZonePrivilege =  34
	SeCreateSymbolicLinkPrivilege =  35
}
```
Et oui, 35 privilèges  ça fait beaucoup. Mais à quoi servent-ils ? Ils permettent d’effectuer certaines tâches systèmes. Il ne faut donc pas les confondre avec les `ACE` ("Access Control Entry", qui représente un droit attribuer dans une `DACL`), car ces dernières définissent l’accès à un `SecurableObject`. Par exemple, le droit `SeBackupPrivilege` est donné à tout membre du groupe `Backup Operators` et permet de lire le contenu d’un fichier peu importe ses `ACLs` (sauf si une interdiction explicite à votre encontre est présente).

![Si un privilège est présent comme SeBackupPrivilege, l'étape de comparaison avec la DACL n'est pas effectuée](/static/img/secu_windows/Principe d'accès à un programme-1.png)

Le droit `SeRestorePrivilege` permet identiquement d’écrire un fichier. Le droit `SeDebugPrivilege` (réservé aux Administrateurs), permet d’accéder et de manipuler la mémoire d’un autre programme, un programme que nous n’avons pas lancé. C’est typiquement ce droit que demande Mimikatz pour accéder aux fameux condensats de mots de passe gardé par `LSASS.exe`.

*Vous pouvez trouver une liste complète des droits donnés par quel privilège dans la [documentation officielle de Microsoft](https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants).*

Ces privilèges, sont donc naturellement très puissant et il ne faut surtout pas négliger leur sécurité, qui possède quoi. Bon, mais comment puis-je clairement savoir de quels privilèges je dispose ? La commande la plus simple pour cela est `whoami /all`. `whoami.exe` ouvre le `token` d’accès de son propre processus, or comme nous l’avons dit plus tôt, ce dernier contient toutes les informations dont le système à besoin pour achever ses tâches, notamment accéder aux `SecurableObject`. Ainsi, nous pouvons voir nos privilèges (`whoami /priv`), nos groupes (`whoami /groups`), notre `SID` (`whoami /user`) et bien d’autres. Un petit exemple, une fois connecté, je lance une invite de commande PowerShell et tape `whoami /priv`. Par malchance, le droit semble alors désactivé.

```text
Windows PowerShell
Copyright (C) Microsoft Corporation. Tous droits réservés.

Testez le nouveau système multiplateforme PowerShell https://aka.ms/pscore6

PS D:\> whoami /priv

Informations de privilèges
----------------------

Nom de privilège              Description                                  État
============================= ============================================ =========
SeShutdownPrivilege           Arrêter le système                           Désactivé
SeChangeNotifyPrivilege       Contourner la vérification de parcours       Activé
SeUndockPrivilege             Retirer l’ordinateur de la station d’accueil Désactivé
SeIncreaseWorkingSetPrivilege Augmenter une plage de travail de processus  Désactivé
SeTimeZonePrivilege           Changer le fuseau horaire                    Désactivé
PS D:\>
```
Pour éteindre mon ordinateur je dois donc activer ce droit. Grâce à une magie occulte je peux l’activer (en réalité j’use simplement d’un implémentation de la fonction `RtlAdjustPrivilege` de `NTDLL.dll`, qui permet d’ajuster les privilèges pour notre processus, en PowerShell) et on peut alors voir que maintenant je peux éteindre mon poste.
```text
PS D:\tools\PowerShellScript\PSReflect-Functions> RtlAdjustPrivilege -Privilege SeShutdownPrivilege -Verbose
COMMENTAIRES : [RtlAdjustPrivilege] Attempting to enable 'SeShutdownPrivilege' for the current process
COMMENTAIRES : [RtlAdjustPrivilege] enable for 'SeShutdownPrivilege' successful
PS D:\tools\PowerShellScript\PSReflect-Functions> whoami /priv

Informations de privilèges
----------------------

Nom de privilège              Description                                  État
============================= ============================================ =========
SeShutdownPrivilege           Arrêter le système                           Activé
SeChangeNotifyPrivilege       Contourner la vérification de parcours       Activé
SeUndockPrivilege             Retirer l’ordinateur de la station d’accueil Désactivé
SeIncreaseWorkingSetPrivilege Augmenter une plage de travail de processus  Désactivé
SeTimeZonePrivilege           Changer le fuseau horaire                    Désactivé
PS D:\tools\PowerShellScript\PSReflect-Functions>
```

Sauf qu’après une partie de "CS:GO" en compagnie d’une équipe russe le "ragequit" serait quelque peu ennuyant. C’est pour cela qu’il est possible d’activer ou de désactiver des privilèges. Attention, ces derniers doivent être contenu dans notre `token` d’accès initiale, sinon cela serait beaucoup trop facile. Lorsque nous utilisons un programme tel "shutdown.exe" il va utiliser certaines fonctions de la `WinAPI` ([`AdjustTokenPrivileges`](https://docs.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges) de `advapi32.dll` pour les curieux) pour changer ses privilèges, et de ce fait pouvoir dire adieu à notre partie gagnée d’avance.

![Pour activer un privilège tel SeShutdownPrivilege, un programme comme shutdown.exe utilise AdjustTokenPrivileges](/static/img/secu_windows/Principe d'accès à un programme-2.png)

## Les listes d’accès

Il en existe deux types. La première est la `SACL` pour "System Access Control List" qui est vraisemblablement la plus simple. En effet, elle permet d’établir un certain nombre de règles concernant l’audit d’accès à l’objet portant cette liste. On peut alors définir dans cette dernière quel événement, pour quel utilisateur, se doit d’être inscrit dans les journaux d’événements. L’autre type se nomme `DACL` pour "Discretionary Access Control List". La `DACL` contient un certains nombres d’`ACE` ("Access Control Entry") qui précise le type de droit accordé à un objet. Leur structure est assez élémentaire. En outre, une `ACE` contient un header déterminant son type c’est à dire accès autorisé ou refusé et d’autres informations. Le header, quant à lui, contient le droit garantit ou non. Ce droit est appelé masque d’accès. On énumère ce que l’on appelle les droits standards qui sont élémentaires:

 - `DELETE` est le droit de supprimer l’objet, je vous l’accorde il n’était pas très complexe celui-là.
 - `READ_CONTROL` est le droit de lire la `SACL/DACL`.
 - `WRITE_DAC` est le droit de modifier les entrés de la `DACL`, c’est à dire ajouter des `ACEs`.
 - `WRITE_OWNER` est le droit de modifier le propriétaire d’un objet, l’intérêt étant que ce dernier possède implicitement tous les droits souhaités.

Ces droits standards permettent alors de construire ce que l’on appelle les droits génériques:

 - `GENERIC_READ` permet, comme son nom l’indique, de lire les attributs et propriétés d’un objet. Si c’est un fichier par exemple, ce droit permet la lecture du contenu du fichier. Son équivalent sous linux est le flag "r".
 - `GENERIC_WRITE` permet la modification des propriétés et attributs de l’objet. Pour continuer dans le précédent exemple, ce droit permet la modification de son contenu. Son équivalent sous linux est le flag "w".
 - `GENERIC_EXECUTE` permet de lire les permissions d’un objet. Factuellement si c’est un programme, il permet de le lancer. Son équivalent sous linux serait le flag "x".
 - `GENERIC_ALL` est la combinaison de ces droits. Attention cependant, il est sensiblement plus fort, dans de très rare cas. Il peut s’avérer que la combinaison `GENERIC_READ/WRITE/EXECUTE` n’est pas équivalente à `GENERIC_ALL`, il n’a donc pas d’équivalent dans le système au pingouin.

Il en existe encore un grand nombre mais l’objectif n’est pas l’exhaustivité. Pour voir ces accès, il faut utiliser l’onglet sécurité des propriétés d’un objet. On peut également utiliser notre shell préférer aka PowerShell (là pour le coup, vous n’avez pas d’excuse car PowerShell c’est génial et opensource). Une commande particulière est destinée à cela: `Get-Acl`. Elle prend comme argument le chemin vers notre objet, `-Path` et ce sera globalement tout pour une utilisation simple. Le résultat retourné est alors une "table" ce qui est assez inconfortable. Pour s’affranchir de se problème d’affichage, on utilise un pipe `|` vers la commande `Format-List` (ou son alias `fl`). On peut alors apercevoir entre autre le propriétaire du fichier dans notre cas, les accès accordés ainsi que le descripteur de sécurité au format `SDDL`. 
```text
PS D:\tools\PowerShellScript\PSReflect-Functions> Get-Acl .\ | fl


Path   : Microsoft.PowerShell.Core\FileSystem::D:\tools\PowerShellScript\PSReflect-Functions
Owner  : DESKTOP-8Q2CUHH\Lancelot
Group  : DESKTOP-8Q2CUHH\Aucun
Access : BUILTIN\Administrateurs Allow  FullControl
         BUILTIN\Administrateurs Allow  268435456
         AUTORITE NT\Système Allow  FullControl
         AUTORITE NT\Système Allow  268435456
         AUTORITE NT\Utilisateurs authentifiés Allow  Modify, Synchronize
         AUTORITE NT\Utilisateurs authentifiés Allow  -536805376
         BUILTIN\Utilisateurs Allow  ReadAndExecute, Synchronize
         BUILTIN\Utilisateurs Allow  -1610612736
Audit  :
Sddl   : O:S-1-5-21-1739485902-3336647338-3362325240-1001G:S-1-5-21-1739485902-3336647338-3362325240-513D:(A;ID;FA;;;BA)(A;OICIIOID;GA;;;BA)(A;ID;FA;;;SY)(A;OICIIOID;GA;;;SY)(A;ID;0x1301bf;;;AU)(A;OICIIOID;SD
         GXGWGR;;;AU)(A;ID;0x1200a9;;;BU)(A;OICIIOID;GXGR;;;BU)



PS D:\tools\PowerShellScript\PSReflect-Functions>
```

Si vous souhaitez plus de précisions, je vous invite à lire [mon article sur le modèle de sécurité Windows](https://theredwindows.net/index.php/2021/08/05/modele-de-securite-windows/)

# Résumons

Lorsqu’un utilisateur se connecte à sa session, des informations seront gardées en mémoire dans un `token` d’accès. Lorsqu’il souhaite démarrer un programme, une copie de son `token` est donné. Si ce dernier interagit avec le système, il devra utiliser ses privilèges pour réaliser certaines opérations. S’il n’est pas tout le temps nécessaire de les utiliser, lorsque l’on souhaite accéder à un objet (fichier, processus …) notre `token` d’accès sert de carte d’identité qui sera comparer avec le contenu de la `DACL` du descripteur de sécurité de l’objet auquel le programme/utilisateur souhaite accéder. En fonction des différentes entrés dans la liste d’accès, il se verra refuser ou autoriser un certain accès.

![Description](https://ilearned.eu.org/static/img/secu_windows/schemasitemicrosoft.png)

J’espère que vous comprenez mieux à présent la manière dont l’os de Microsoft gère les permissions. Si cet article vous a plu, je vous invite à consulter mes articles sur les privilèges d’accès ainsi que sur l’abus des `ACLs` en Active Directory (et oui même si utile aux défenseurs, ils sont aussi utile aux attaquants).

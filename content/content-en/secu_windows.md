Author: Lancelot
Date: 2021/07/01
Keywords: Windows, Security
Slug: windows_security
Summary: "Access denied". If there is a frustrating error, it is surely this one. On Windows we are often confronted with it, especially from an attacker's perspective. In this article, I will try to present you, in broad outline, the security model used by Windows.
Title: Windows security model
Translator: MorpheusH3x

## Introduction

"Access denied". If there is a frustrating error, it is surely this one. On Windows we are often confronted with it, especially from an attacking perspective. However, few people understand why this error (or others) interferes with their comfortable use of their operating system.

In this article, I will try to give you an overview of the security model used by Windows, mainly the notions of access privilege and access control.

Generally speaking, when I talk about Windows objects, I am talking about users, machines, files, or even processes.

## Security environment

To understand what follows, it is necessary to understand what a security context is in our friend Windows. The latter designates a set of attributes or security rules currently in force, as defined by Microsoft. A security context will be translated by a particular data structure defined by the `SSPI` ("Security Support Provider Interface"), a Windows `API` written in order to interact with the security context, it is used, for example, for authentication. In other words, the security context defines the basic elements of the security system of our favorite OS (if it doesn't, pretend it does).

## SecurableObject

An object is said to be "securable" if it has the ability to have a security descriptor. In general, a lot of objects in Windows are `SecurableObjects`. Processes, registry keys, files/directories, Active Directory objects and many others. They form the core of the interactions between us and the operating system. I mentioned security descriptors, these are simply lists of several characteristics. They contain the `SID` ("Security Identifier", which is a unique identifier) of the owner of the object, the `SID` of the owner group, and `ACLs` for "Access Control Lists". Security descriptors are usually in the `SDDL` ("Security Descriptor Definition Language") format, which, although not very nice, is actually very practical because it is easy to use (not to understand).

## Access tokens

When a Windows user logs into his local account (or Active Directory) several pieces of information will be stored in the memory. Obviously, it will contain the password digest (except for very unlikely configurations or a relatively old system, in which case it will be the password in clear), his `SID`, the `SID` of his group, access privileges (we'll come back to this later) and many other information. All this is gathered in what is called an access token. This is then kept in a special process called `LSASS.exe` for "Local Security Autority SubSystem Service". It is therefore vital and very sensitive.

![Once the password is specified, a token is created](/static/img/secu_windows/Auth LSASS.webp)

When we interact with the system in any way, a copy of our access token is used. In the case of a file, the information that the access token contains will then be compared with the information in the `DACL` (which is a list containing the accesses, more on that later) guaranteeing or not an access of a certain value. It can be intended for writing, reading or even for execution.

![Some information of the token is compared with the DACL](/static/img/secu_windows/Access-principle.webp)

A more interesting case is that of starting a program. Indeed, the latter is launched as a particular user, so it must not bypass this famous access system. This is why processes are considered `SecurableObjects`, and in this situation, a copy of our `token` access is also given and when the program interacts with the system, it will do so according to the rights and identity of the connected user.

![When we create a process, we give it our token so that it can use it](/static/img/secu_windows/Principle of access to a program.webp)

*The function [`CreateProcessA()`](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa) is a function of the Windows `API` `kernel32.dll` which allows to create a new process.*

## Access privileges

As mentioned earlier, the access token contains a number of privileges within it. These are assigned to each connection, according to the security rules. More precisely, access privileges are given according to the group to which one belongs, to which one assigns default rights through local `GPOs` (in `gpedit.msc`, `Computer Configuration`, `Security Settings`, `Local Policies`, `User Rights Assignment`). The list of these privileges is not presented as a classical enumeration, but here is a PowerShell implementation to get a good idea of all these privileges (from [PSReflect-Functions](https://github.com/jaredcatkinson/PSReflect-Functions)).
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
And yes, 35 privileges is a lot. But what are they for? They allow to perform some system tasks. They should not be confused with `ACE` ("Access Control Entry", which is a right assigned in a `DACL`), because the latter defines access to a `SecurableObject`. For example, the `SeBackupPrivilege` right is given to any member of the `Backup Operators` group and allows you to read the contents of a file regardless of its `ACLs` (unless you are explicitly prohibited from doing so).

![If a privilege is present as SeBackupPrivilege, the comparison step with DACL is not performed](/static/img/secu_windows/Program access principle-1.webp)

The `SeRestorePrivilege` right allows identically to write a file. The `SeDebugPrivilege` right (reserved to Administrators), allows to access and manipulate the memory of another program, a program we have not launched. It is typically this right that Mimikatz asks for to access the famous password digests kept by `LSASS.exe`.

*You can find a complete list of the rights given by which privilege in the [official Microsoft documentation] (https://docs.microsoft.com/en-us/windows/win32/secauthz/privilege-constants).

These privileges are naturally very powerful and you should not neglect their security, who has what. Now, how can I clearly see which privileges I have? The simplest command for this is `whoami /all`. `whoami.exe` opens the `token` of its own process, and as we said earlier, it contains all the information the system needs to complete its tasks, including access to `SecurableObjects`. Thus, we can see our privileges (`whoami /priv`), our groups (`whoami /groups`), our `SID` (`whoami /user`) and many others. A small example, once logged in, I launch a PowerShell command prompt and type `whoami /priv`. By bad luck, the right seems to be disabled.

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
So to shut down my computer I have to activate this right. Thanks to some hidden magic I can activate it (in reality I'm just using an implementation of the `RtlAdjustPrivilege` function of `NTDLL.dll`, which allows to adjust the privileges for our process, in PowerShell) and we can see that now I can turn off my computer.
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

Except that after a game of "CS:GO" with a Russian team the "ragequit" would be somewhat boring. That's why it is possible to activate or deactivate privileges. Be careful, these must be contained in our initial access `token`, otherwise it would be much too easy. When we use a program like "shutdown.exe" it will use some functions of the `WinAPI` ([`AdjustTokenPrivileges`](https://docs.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges) of `advapi32.dll` for the curious) to change its privileges, and thus be able to say goodbye to our game won in advance.

![To activate a privilege such as SeShutdownPrivilege, a program like shutdown.exe uses AdjustTokenPrivileges](/static/img/secu_windows/Program access principle-2.webp)

## Access lists

There are two types. The first is the `SACL` for "System Access Control List" which is probably the simplest. Indeed, it allows to establish a certain number of rules concerning the access audit to the object carrying this list. You can then define in this list which event, for which user, should be recorded in the event logs. The other type is called `DACL` for "Discretionary Access Control List". The `DACL` contains a number of `ACE` ("Access Control Entry") which specify the type of right granted to an object. Their structure is quite elementary. In addition, an `ACE` contains a header determining its type, i.e. access allowed or denied, and other information. The header, in turn, contains the right guaranteed or not. This right is called an access mask. We list what we call the standard rights which are elementary:

 - `DELETE` is the right to delete the object, granted it wasn't a very complex one.
 - `READ_CONTROL` is the right to read the `SACL/DACL`.
 - `WRITE_DAC` is the right to modify the entries in the `DACL`, i.e. add `ACEs`.
 - `WRITE_OWNER` is the right to modify the owner of an object, the interest being that the owner implicitly has all the desired rights.

These standard rights are then used to build what are called generic rights:

 - `GENERIC_READ` allows, as its name indicates, to read the attributes and properties of an object. If it is a file for example, this right allows to read the content of the file. Its equivalent under linux is the "r" flag.
 - `GENERIC_WRITE` allows the modification of the object's properties and attributes. To continue in the previous example, this right allows the modification of its content. Its linux equivalent is the "w" flag.
 - `GENERIC_EXECUTE` allows to read the permissions of an object. In fact if it is a program, it allows to launch it. Its linux equivalent would be the "x" flag.
 - `GENERIC_ALL` is the combination of these rights. Be careful though, it is significantly stronger, in very rare cases. It may turn out that the combination `GENERIC_READ/WRITE/EXECUTE` is not equivalent to `GENERIC_ALL`, so it has no equivalent in the penguin system.

There are still a lot of them but the objective is not to be exhaustive. To see these accesses, you have to use the security tab of an object's properties. We can also use our favorite shell aka PowerShell (here you have no excuse because PowerShell is great and opensource). There is a special command for this: `Get-Acl`. It takes as argument the path to our object, `-Path` and that's about it for simple use. The result is a "table" which is quite uncomfortable. To get rid of this display problem, we use a `|` pipe to the `Format-List` command (or its alias `fl`). We can then see the owner of the file in our case, the accesses granted and the security descriptor in `SDDL` format. 
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

If you want more details, I invite you to read [my article about Windows security model](https://theredwindows.net/index.php/2021/08/05/modele-de-securite-windows/)

# Let's sum up

When a user logs in to his session, information will be kept in memory in an access `token`. When he wants to start a program, a copy of his token is given. If he interacts with the system, he will have to use his privileges to perform certain operations. If it is not necessary to use them all the time, when we want to access an object (file, process ...) our access token serves as an identity card which will be compared with the contents of the `DACL` of the security descriptor of the object the program/user wants to access. Depending on the different entries in the access list, it will be denied or allowed a certain access.

![Description](https://ilearned.eu.org/static/img/secu_windows/schemasitemicrosoft.webp)

I hope you now have a better understanding of how the Microsoft OS manages permissions. If you liked this article, I invite you to read my articles on access privileges and on the abuse of `ACLs` in Active Directory (and yes, even if useful for defenders, they are also useful for attackers).

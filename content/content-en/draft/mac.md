Author: Ramle 
Date: 2021/07/20
Keywords: sécurité
Slug: mac
Summary: A reproach often made to Linux is its management of the rights often too permissive, to remedy that were created the MAC
Title: Hardening your operating system with MACs
Translator: MorpheusH3x
Status: draft

A reproach often made to Linux is its management of rights often too permissive. There is of course a historical reason, at the birth of the different operating systems we know today, security was not the main concern. The basic goal was not to complicate the task of the users either (security is always done at the price of additional complexity). The problem with this starting philosophy is that you have to rethink security with too open a base.

In Linux everything is a file, physical devices have for example a file assigned in `/dev`. The access security for files is based on the permissions of each file. This mechanism quickly shows its limits. Permissions are very limited, under Linux these permissions are divided into 3, what the owner user can do, what the owner group can do and what everyone else is allowed to do. Each party can have 3 different rights:

- R (read): Reading
- W (write): Write
- X (Execute) : Execute (in the context of a folder this is the permission to list the contents)

We can view the permissions via the command `ls -l <folder>` :

```jsx
% ls -l
total 0
-rwxr-xr-x 1 ramle ramle 0 Jul 19 17:05 executable
-rw------- 1 root  root  0 Jul 19 17:05 root_only
```

`ls` divides the permissions into 3 parts, the user's, the group's and everyone's:

![Details of permissions displayed by LS](/static/img/mac/ls.png)

The concern of basing only on file permissions is the lack of control, the MAC security scheme allows to reinforce this by looking at many more factors. The concept is to look at all the actions done on the machine, and to look at the action and authorize it or not according to the access rules. The advantage of this model over the historical security of Linux (and UNIX for that matter) is that it is much more precise, for example allowing an application to access only certain ports and files (files that could be allowed depending on the file system).

Under Linux, there is no MAC framework base, but modules in the kernel are provided for a framework to be grafted onto it. There are two important ones, Apparmor and SELinux.

Both have similar features, but differ in one important point, Apparmor is based on the full path of a file, where SELinux is based only on the name, this difference is quite small in most cases, but depending on the framework used, bypass methods based on these specifics, for example using virtual links (symlink) or renaming a file, a good access policy avoids bypasses though.

Of course, Linux is not the only operating system that uses more advanced access controls than just basic permissions, Windows works on [this principle](https://ilearned.eu.org/secu_windows.html) as does MacOS and BSD with the integration of TrustedBSD.

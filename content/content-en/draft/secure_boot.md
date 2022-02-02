Author: Ramle 
Date: 2021/07/07
Keywords: sécurité
Slug: secure-boot
Summary: Checking the integrity of a system at boot time is crucial, if an attacker is able to modify files he can easily have full power to implement malware. To solve this, Secure Boot was developed.
Title: Checking the integrity of a system at boot time thanks to Secure Boot.
Translator: MorpheusH3x
Status: draft

The security of a system depends on many factors, one of the important factors is to be able to verify the integrity of the booted system, indeed without this verification an attacker could without much difficulty modify the boot files to add malware. This article will focus on desktop machines.

To fully understand how attacks can be carried out during the boot process it is important to understand how the BIOS boot mode works, and its replacement the UEFI.

## BIOS

The BIOS boot is based on a table of partitions in MBR (master boot record), to boot the bios will execute the code contained in the table of partitions, this code will pass the hand to the bootloader which will take care to launch the system. A rather obvious problem appears already, code can be directly inserted in this part, no verification is done by the BIOS. An attacker could also attack the bootloader which cannot be encrypted.

Under Linux (we will see how Windows works later) the most common bootloader is grub, it inserts in the MBR what to load its complete code which is contained in `/boot`, most bootloaders under Linux work on the same principle.

![An unencrypted system](/static/img/secure_boot/unencrypted_system.png)

To avoid a modification of the system we could encrypt the root partition (also called Userland) and make a separate /boot (the bootloader cannot be encrypted), a problem arises then, the initramfs and the kernel are always in clear.

![An encrypted system with only the userland encrypted](/static/img/secure_boot/encrypted_system_userland.png)

Grub (and it is to my knowledge the only one) allows to decrypt the boot partition, to keep the initramfs and the kernel encrypted. But grub itself is always modifiable, same thing for the code executed directly in the MBR.

![An encrypted system with userland and kernel encryption](/static/img/secure_boot/encrypted_system_userland_kernel.png)

Besides not being totally secure, with this method the passphrase has to be typed twice, once to read the initramfs and once to decrypt the root partition. (grub does not remember it).

A possible solution would be to sign the different elements of the boot, the problem is that in BIOS no mechanism for signature verification exists.

With a BIOS we have no possibility to secure a Linux system completely.

For Windows, the concept is very close, the BIOS will execute the code in the MBR, this code will trigger the Windows bootloader which, since Windows Vista, is bootmgr, encrypting the disk poses the same concern as under Linux, the bootloader will remain in clear.

## UEFI

With UEFI we do without MBR in favor of GPT which brings a number of advantages. The boot process is no longer done by an executable code in the MBR part, this code is contained in a FAT32 (or FAT16) partition, which allows not to be so limited in size, the part dedicated to the boot code in MBR is only 446 bytes. UEFI also brings a major evolution for security: Secure Boot, it is a way to verify the integrity via a signature of the EFI file. An EFI file is an executable launched by the UEFI, it could be compared to the ELF of Linux, or the exe of Windows.

When a pc with Secure Boot starts, it checks the EFI binary, to see if the signature corresponds to a "trusted" key and if the signature is not in the list of keys to refuse.

UEFI is based on variables for the keys, you can see them from Linux via the "efi-readvars" utility, which on my machine gives :

```jsx
Variable PK, length 823
PK: List 0, type X509
    Signature 0, size 795, owner 5b2a4205-8ee1-404d-a357-45629f968019
        Subject:
            CN=Ramle PK
        Issuer:
            CN=Ramle PK
Variable KEK, length 825
KEK: List 0, type X509
    Signature 0, size 797, owner 5b2a4205-8ee1-404d-a357-45629f968019
        Subject:
            CN=Ramle KEK
        Issuer:
            CN=Ramle KEK
Variable db, length 823
db: List 0, type X509
    Signature 0, size 795, owner 5b2a4205-8ee1-404d-a357-45629f968019
        Subject:
            CN=Ramle DB
        Issuer:
            CN=Ramle DB
Variable dbx has no entries
Variable MokList has no entries
```

Let's take a closer look at each variable:

- PK: This is the highest key in the chain of trust, it is there to sign the KEK key, only one key is possible in this variable. In general it is the constructor who puts his key, if you want to control totally the chain of trust you will have to change it.
- KEK : These keys are used to sign the keys that will go into DB or DBX, often there are 2 KEK, one for Microsoft and another for the Manufacturer.
- DB : These are the keys used for the verification of EFI binaries, often the computer comes with the keys of the manufacturer, Microsoft, Canonical (the company behind Ubuntu) and sometimes other companies.
- DBX: This is the list of untrusted keys.
- MOKList : It is used by a tool called Shim, this tool is there to load another bootloader which would not be signed with the keys present in DB, Shim will check the bootloader via the keys in the MOKList which is managed by the user, and not via the UEFI directly.

![The Secure Boot Chain of Trust](/static/img/secure_boot/secure_boot_chain_of_trust.png)

These variables are of course modifiable on most of the PCs, which allows to manage its own PKI (public key infrastructure).

If you want a real control you have to manage your own keys, under Linux it's possible without too much difficulty, FreeBSD and OpenBSD seem to support it too (I didn't have the opportunity to test it) and under Windows you can either use Microsoft keys or use your own keys which seems in theory possible.

I hope this article will have more for you, I think soon to make a small guide for the management of Secure Boot under Linux, so I let you watch the releases.

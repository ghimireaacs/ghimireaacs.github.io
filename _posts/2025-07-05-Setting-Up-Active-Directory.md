---
layout: post
title: "Setting Up Active Directory"
date: 2025-07-05 00:00:00 +0000
categories: Active Directory
tags: Active-Directory guide walkthrough TCM-SEC AD
description: "Setting Up Active Directory PNPT Method"
image:
 path: /assets/img/headers/activeDirectory.webp
---

At first Download ISOs
- [Windows Server Eval 2022](https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022)
- [Windows 10 Enterprise](https://www.microsoft.com/en-us/evalcenter/download-windows-10-enterprise)


## Setup Domain Controller

1. NEW VM
2. Typical
3. Server ISO
4. Split
5. Make sure its 60 GB
6. Finish
7. Edit
8. Add 8GB RAM
9. Remove Floppy Drive (Recommended)

### Install
1. Next > Install Now
2. Standard Evaluation Desktop Experience
3. Custom Install
4. New > Default > Apply > Ok
5. Next
6. Done
7. For This purpose set easy password `P@$$w0rd!`
8. Login
9. Install VMWare Tools
10. VM > Install VMWare tool 
11. Open This PC > Open ISO
12. Install

### SERVER CONFIGURATION (ADDS)
1. Change Hostname
	1. Start Menu > Name > Rename This PC
	2. HYDRA-DC
	3. Reboot.
2. Make this a Domain Controller
	1. Manage > Add Roles and Feature
		1. Role-based or Feature-based install > Next
		2. HYDRA-DC > Next
		3. Server Roles > ✅Active Directory Domain Services (ADDS) > Add Features > Next
		4. Next
		5. Next
		6. Restart Auto if required
		7. Install
	2. Promote This Server to Domain Controller
		1. Add a new forest
		2. Root Domain: `marvel.local` > Next
		3. Functional Level: 2016
		4. Same password for Admin Account > Next > Next
		5. Loads netbios Automatically > Next
		6. Next to last > Install
	3. Certificates Services
		1. Manage
		2. Add roles and Feature
		3. Role Based Feature
		4. Next to Features
		5. Role Based Features
		6. Active Directory Certificate Services (Used to verify ID in domain controller) (Allows us to use LDAP)
		7. Add Features > Next to AD CS Role Services
		8. ✅ Certificate Authority > Next
		9. ✅ Restart if Needed
		10. Install
	4. Configure Certificates Services
		1. Flag > Configure AD CS
		2. ✅ Certification AUthority > Next
		3. Private Key > Create New pvt key
		4. Default Next to Validity
		5. 99 years
		6. Default > Configure

## DC

ip: 192.168.135.131
administrator:`P@$$w0rd!`



## CLIENT SETUP

Setup 2 OS at same Time
- Download WIndows 10 Enterprise ISO

### VM Setup
1. Open VMWARE
2. Create new VM
3. select Downloaded ISO
4. Windows 10 Enterprise > Next > Yes (Without product key)
5. Name:  THE PUNISHER > Next 
6. SIZE 60 GB > Finish
7. Customize > Remove Floppy, Adjust RAM 8 GB Cpu 4 > OK
8. Power On and Hit any key and move to second VM do same, different name


### OS SETUP

(SIMALTANEOUSLY)
1. Power On Both Machines
2. Press key to continue
3. Install Now > Accept Terms > Custom > Next to install
4. RESTART
5. US > YES > US > YES > SKIP
6. Domain Join Instead
7. Punisher VM = `frankcastle` password= `Password1`
8. Spiderman VM = `peterparker` password = `Password1
9. All Questions Answered BOB
10. Disable all tracking > Not Now to Cortana
11. WAIT
12. INSTALL VMWARE TOOLS
13. Change Hostname > THEPUNISHER & SPIDERMAN


### SETTING UP USERS, GROUPS and POLICIES

#### SERVER

##### USER Setup
1. Server Manager
2. Tools > AD Users and Computers
3. Manage User Groups
	1. MARVEL.local ( Domain Controller) > *Right Click* >New > OU
		![](assets/img/posts/8374186a9e4ec287b84309cfc18497bb.webp)
	2. Move Everything Except `Admin` and `Guest` to New `Groups` > YES
		![](assets/img/posts/c6a3724ed01b57185a98dd924933dfee.webp)
		![](assets/img/posts/6d9f03394d84b36cc78c1f13001a55b0.webp)
4.  Create Another `Administrator`
	1. Copy current `Administrator`
		![](assets/img/posts/48cfc8b6b9784b5a80c08a1d7f80fbf7.webp)
		![](assets/img/posts/e9aeeb72e351d1d5bb9d8f87c58cc1d4.webp)
5. Create a *Service* account
	1. Name: SQL Service Password: MYpassword123# (Weak pw with complexity and character count for lab purpose)
		![](assets/img/posts/36bda5b872772704529408c93afc73c8.webp)
		![](assets/img/posts/bed32ca05225fd7f71d9893c7ef25376.webp)
6. Create Two New Users
	1. *Right Click* > New > User
		![](assets/img/posts/4074da60a0098b793bd9ff010fc771a0.webp)
		![](assets/img/posts/affb69b9b77b19b873aa9c92bef9ea79.webp)
		![](assets/img/posts/36cde6d2ca44f4ab89063f4f19bac706.webp)
	2. For Second User *copy* recently created user and change Names
		![](assets/img/posts/db44e1a5879b2613a61de42216c8713a.webp)

##### File Sharing To Exploit Later
1. Server Manager
2. File Share and Storage
3. Shares > Tasks > New Shares
4. SMB Share Quick > Next
5. C: is fine > Next
6. Name: `hackme`
7. ✅Allow Caching > Next
8. Permission > Next
9. Create

##### SETUP Service Account Fully
1. Open Command prompt as Admin
2. `setspn -a HYDRA-DC/SQLService.MARVEL.local:60111 MARVEL\SQLService`
3. Check with `setspn -T MARVEL.local -Q */*`

##### Setup Group Policy
1. Start Menu > Group Policy Management
2. Forest > Domains
3. *Right Click* MARVEL.local > Create a GPO in this domain and Link it here
4. Name: Disable Windows Defender > Ok
5. Edit *Newly created Policy* i.e `Disable Windows Defender`
	1. Computer Config > Policies > > Admin Templates > Windows Components > Microsoft Defender Antivirus
	2. *Double Click* Turn Off Microsoft Defender Antivirus
	3. Enabled > Apply
6. *Right Click* > Enforced

##### Setup Static IP Address
1. *Right Click* Network on Taskbar 
2. Open Network Internet Settings
3. Change Adapter options
4. Ethernet0
5. Properties > IPV4 > Use Following (acquired form `ipconfig` )
	1. IP: 192.168.135.137 (current ip from ipconfig)
	2. Subnet Mask: 255.255.255.0
	3. Gateway: 192.168.135.2
6. Ok 

# Join Machine To Domains

1. Login to Client Machines
2. Make IP Addresses Static
	1. Change Preferred DNS server to Domain Controller's IP i.e. 192.168.135.137

## Make Client devices Join the Domain

1. Start Menu
2. Access Work or School
	![](assets/img/posts/0f0554514a2d6d14c380eea35d3aefab.webp)
3. Connect
	![](assets/img/posts/557449303d8f76c26704e2563df0586b.webp)
4. Join this device to a local Active Directory Domain
	![](assets/img/posts/dc9bc20b351c66266191488ddcc564e4.webp)
5. Set it as `MARVEL.local`
6. Enter your Domain Controller Username and Password and ENTER
7. We can Add as Administrator
	![](assets/img/posts/0ad743d75d6aad97ca3a179b8195c07f.webp)
8. Restart Now
9. Verify If you Joined Domain
	1. Server Manager > Tools > AD Users and Computers
	2. Computers > You will see both your Devices
		![](assets/img/posts/cb5cbaefd24d15044d0e5d6d5034c564.webp)
		
10. Open CLient Login with MARVEL\administrator

### Modify Local Users for Client Machines

#### Enable Local Admin
1. Start > Users > Edit Local Users and Groups
2. Users > Administrator > Enable
	![](assets/img/posts/d9988e2da8a765e2b33376b90ce52dd3.webp)
3. Set Password (Password1!)
	![](assets/img/posts/0d4a2e1b9dd67792e98abe81483cdf88.webp)
4. Uncheck Account is Disabled > Apply > OK
	![](assets/img/posts/b62c2c1fb9902b30c1ed9de432abdea8.webp)


#### Add Other Administrators

1.  Start > Users > Edit Local Users and Groups
2. Groups > Administrators > Add > Search `fcastle` > Check Names > OK

	![](assets/img/posts/8cad1948d4c9dc5fdb2d34bf3652fbef.webp)
	
#### Logout and Check Local Account
1. Other Users
2.  .\peterparker | Password1
3. Map Network Drive > Z:
4. Folder > `\\HYDRA-DC\hackme` | Connect using Different Credentials
	![](assets/img/posts/e454745e8310d56c791b5d560a7f3caf.webp)
5. Use Credentials
	username: `administrator`
	password: `Pa$$w0rd!`

## SPIDERMAN

ip: 192.168.135.134
peterparker:Password1

local:
peterparker

## THEPUNISHER

ip: 192.168.134.135
frankcastle:Password1

local
frankcastle:Password123

Admins
tstark@MARVEL.local
pw: Password12345!

SQL Service
Password is MYpassword123#

Domain Controller
IP > 192.168.135.137


TO sign IN


![](assets/img/posts/071a957c87ed50e278296d12bb05a502.webp)
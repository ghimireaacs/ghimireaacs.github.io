---
layout: post
title: "Installing Proxmox and Post Installation"
date: 2025-07-24 00:32:00 +1100
category: Walkthrough
tags: [proxmox, homelab]
description: "Installing Proxmox and Post Installation using Community Script"
image: /assets/img/headers/proxmox.webp
---

Its 2025 most of us have a spare piece of Desktop or Laptop lying around, which seems like is not worth much. But using Proxmox that piece of old tech can make your life easier without a lot of trouble. You will not need a brand new unique system to run a server. Any PC should be fine after 2010, check specs for PCs that are older than 2010.

We will be Making a Bootable USB, Installing Proxmox and Setting up Post Installation process.
# Prerequisite

## Hardware
- USB Stick
- A Computer / Laptop to make USB Bootable
- Another Computer as Server
- WI-FI or A Lan Cable to connect Server to Router
## Software
- Balena Etcher
## Network
- IP Gateway (Router IP) Address and Subnet, Usually 192.168.x.x/24 
# Pre-Installation

Before Installing Proxmox we have to make a bootable USB drive. And our system ready to boot from USB.
## Prepare USB

1. Download Proxmox VE from [Official Proxmox Site](https://www.proxmox.com/en/downloads)
2. Download Balena Etcher from [Balena Etcher Official Site](https://etcher.balena.io/#download-etcher)
3. Flash Downloaded ISO file to USB
	![](assets/img/posts/32f9acc76a1be3de7e31a35a982a72ed.webp)![](assets/img/posts/495f48066f7746da167a1cc311ee3751.webp)![](assets/img/posts/7f265173d015846a32ed68043a6b3f45.webp)![](assets/img/posts/432cdecf0490211bfdc00f40b3197769.webp)
	
	> 	⚠️ Make sure you select right device

4. Select Yes on Windows Prompt.
5. Let it Flash.
6. Done

## BIOS Settings

1. Connect your USB
2. Start/Restart this machine.
3. During Boot, open BIOS/UEFI settings using `F8` or `DEL` key.
4. Now look for Boot Order. Look for Boot option on top.
5. Select your USB as boot device.
6. Now this will boot to Proxmox Installation.

> 💡 Boot Configuration GUI varies with motherboard manufacturer. Please look for your specific Motherboard Bios settings in the internet.


# Installation


During installation you will be prompted with the steps below. Here I have highlighted the selection with <mark style="background: #BBFABBA6;">Green</mark> and things to consider on <mark style="background: #D2B3FFA6;">Purple</mark>

1. Select Install Proxmox  VE (Graphical)
	![](assets/img/posts/4a47a0db6e60853dedfcfdf08a5ca249.webp)
2. Read The EULA and Agree (Mandatory for Installation)
	![](assets/img/posts/fb5c81ed3a220004b71069645f112867.webp)
3. Make sure you select the correct Disk here, one way to see correct disk is Size of the disk. But if you have only one disk you can go next as it will be default.
	![](assets/img/posts/10fb15c77258a991b0028080a64fb42d.webp)
4. Make sure you select your correct Location and Time Zone here.
	![](assets/img/posts/09dd8c2662b96ce14928333f055c5580.webp)
5. Write your desired password, Make sure you remember it and it complies with the policy highlighted in purple.
	![](assets/img/posts/8266e4bfeda1bd42d8f9794eb4ea0a13.webp)
6. ⚠️ Network is arguably most important section here because once its set up, we will be accessing Proxmox only through web.
	![](assets/img/posts/f19c9085129709ee14d013be869df69b.webp)
	1. IP Address (CIDR): This is where you allocate your static IP so it does not change in future and mess up with settings. Its borderline mandatory to have static IP. If you have Ethernet connected your Router will allocate an IP , change it. Personally i recommend changing last bits over 100 and leave subnet to 24. 
	2. Gateway : Router IP (Usually prefilled)
	3. DNS Server: Router IP. I recommend router IP so if i change my DNS in my router its global for all devices in LAN. You can also opt to `1.1.1.1` for Cloudflare or `8.8.8.8` for Google's DNS server.
	> 💡 All of the Network settings can be changed later too. These settings make sure we have Initial Network Access.
7. Summary: Final summary of all our configuration before we proceed with Installation.
	![](assets/img/posts/9eb9cd58b9ea5e04c890326b5c1f471f.webp)
8. After clicking Install it will take a couple of minutes to finish Installation and reboot Automatically.
	![](assets/img/posts/602e8f042f463dc47ebfdf6a94ed5a6d.webp)
9. After Reboot Select First option i.e. "Proxmox VE GNU/Linux" and Enter.
	![](assets/img/posts/7afbb1602613ec52b265d7a54ad27330.webp)
10. You will see Your IP and Port 8006 on the top. Yours will be different from mine. This is how we will access the web app and carry on from. Now you can remove monitor from proxmox server and move it to its designated area and will barely need to touch the hardware. Power and LAN is important and that's all we need.
	![](assets/img/posts/586e508f161f26ce94633729ac56c602.webp)

# First Access and Post Installation

1. Go to the given URL on your browser.
2. Since its self signed Certificate it will warn you. Accept the risk and continue.
3. Now for username `root` and `password` is what we set during installation.
4. Once we login we will be prompted A subscription message. Click OK. 

## Post Installation and Scripts

Here comes the magic of Proxmox Community. Proxmox is an open source software with a huge community behind it. The project "Proxmox VE Helper-Scripts" was started by a user who went by name "[Tteck](https://github.com/tteck/)" . He sadly passed away and the scripts are maintained by community in a [community github repo](https://github.com/community-scripts/ProxmoxVE)  and can be accessed at https://community-scripts.github.io/ProxmoxVE/ .

We will be using "[Proxmox VE Post Install](https://community-scripts.github.io/ProxmoxVE/scripts?id=post-pve-install)" Script. This script will updates our proxmox, disables bunch of features which are redundant in our use case and also modifies repos. Apart from that it also disables "Subscription Nag" , that ok option every time you have to hit when you open it up.

This is strongly recommended to run Immediately after Installation.

1.  Below Datacenter Click on pve.
	![](assets/img/posts/c51eb0ec190e11157de0e0ee756c9353.webp)
2. On top right you will see `shell`.
	![](assets/img/posts/ae0590af5df5d22044ceda3914c21023.webp)
3. Clicking `shell` will open a web shell where you can run the script.
	![](assets/img/posts/0a3854aabd6e78c94df808f5c890b0d8.webp)
4. Now either paste the script below or get it directly from "[Helper Script Website](https://community-scripts.github.io/ProxmoxVE/scripts?id=post-pve-install)"
	![](assets/img/posts/c8091a8d715fbb5703085555e24ea8e3.webp)
5. Now it is recommended to select Yes on all prompts.
	![](assets/img/posts/5ce32cbb4a3d03d02d573efe6ef7ab3f.webp)
6. It will reboot and your system is ready for VM.
	![](assets/img/posts/ee9e1c5d50672f7367550cb8378b61c0.webp)

Now for further we will be installing VMs.  I will add Link on this post for VM installation guide.

Welcome to HomeLab.


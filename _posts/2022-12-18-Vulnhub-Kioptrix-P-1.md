---
layout: post
title: "Vulnhub Kioptrix Walkthrough Part 1"
date: 2022-12-18 23:11:31 +1100
category: Walkthrough
tags: [vulnhub, kioptrix, guide, walkthrough, TCM-SEC, net-discover, arp-scan]
description: "Vulnhub Kioptrix Walkthrough Part 1"
image: /assets/img/headers/tcmsec.webp
---

![tcmsec](/assets/img/headers/tcmsec.webp)

```
Default username: John
Default Password: TwoCows2
```
*Tips: Save your all Scans in text/image for future use*

### Lets find our IP
- Start Virtual Machine
- `ip a` in your main OS terminal, this will give us ip of our target machine
 - Now go to your main machine _Kali_ run `sudo arp-scan -l`
![kioptrixIP](/assets/img/posts/kioptrixwt1_2.webp)

This will give us *IP address, Mac Address and Vendor*
We are looking for our matching IP. or *Azureware/VMware*

***
> Optional

Now go to terminal
	- `sudo netdiscover -r your IP/subnet mask`
		- `sudo netdiscover -r 192.168.0.0/24`
*_This did not work in my case_*
***
### Look for OPEN PORTS
	nmap
- `sudo nmap -sS 192.168.0.26` *-sS stands for stealth mode*
  ![kioptrixIP](/assets/img/posts/kioptrixwt1_3.webp)

### For Full scan with *nmap*:
	Gives extensive information
- `sudo nmap -T4 -p- -A ip_of_target`

	*_Note: Here -T4 is for speed, -p- all Ports and  -A for all info, OS, Fingerprinting, applications and their version of applications, etc._*
![kioptrixIP nmap ip](/assets/img/posts/kioptrixwt1_4.webp)

### NMAP
	Common Nmap commands and Uses

- Host Discovery
	- As long as there is `nmap . . .  ip`  it is going to discover hosts
	- attribute order does not matter start with `nmap` or `sudo nmap` and end with `ip`
	- To scan only UDP
		- `nmap -sU -T4 192.168.0.26`
			- Note: removing -A makes it faster because it only scan few Info
![kioptrix NMAP udp scan](/assets/img/posts/kioptrixwt1_5.webp)

---

### Here we found
- Target IP, Mac Address
- OPEN TCP Ports
- OS, application uses, and Versions
- Some more useful info.

---
layout: post
title: "Vulnhub Kioptrix Walkthrough Part 1"
date: 2022-12-18 23:11:31 +1100
category: Walkthrough
tags: [vulnhub, kioptrix, guide, walkthrough, TCM-SEC, net-discover, arp-scan]
description: "Step-by-step walkthrough of Vulnhub Kioptrix Level 1. Covers network discovery with net-discover and arp-scan, service enumeration, and exploitation. TCM Security training series."
image: /assets/img/headers/tcmsec.webp
---

This is part of the TCM Security Practical Ethical Hacking course. Kioptrix is a classic beginner-friendly vulnerable machine available on Vulnhub. The idea is to compromise the machine and understand what you are doing at each step, not just copy paste commands. This was one of my first full walkthroughs.

The setup is simple. Download the Kioptrix VM from Vulnhub, run it in VMware or VirtualBox on a host-only or NAT network with your Kali machine. Your job is to find it on the network and get in.

```
Default username: John
Default Password: TwoCows2
```

> Save your scan results as text files or screenshots as you go. You will want to refer back to them later.
{: .prompt-tip }

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
- Target IP and Mac Address
- Open TCP ports
- OS, running applications, and their versions
- Enough information to start looking for exploits

## What This Tells Us

After enumeration you should have a list of services and their versions. The next step is looking up those versions for known vulnerabilities. Tools like Searchsploit, or just a Google search with the service name and version, will give you a list of exploits to try.

Kioptrix Level 1 is vulnerable to a well-known mod_ssl exploit. If you have got this far you have everything you need to find it.

Continue to [Kioptrix Walkthrough Part 2](/posts/Vulnhub-Kioptrix-P-2/) for web application enumeration with Nikto, Dirbuster, and Burpsuite.

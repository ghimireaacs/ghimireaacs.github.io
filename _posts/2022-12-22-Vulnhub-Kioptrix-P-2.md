---
layout: post
title: "Vulnhub Kioptrix Walkthrough Part 2"
date: 2022-12-22 23:11:31 +1100
category: Walkthrough
tags: [vulnhub, kioptrix, guide, walkthrough, TCM-SEC, nikto, dirbuster, burpsuite]
description: "Vulnhub Kioptrix Walkthrough Part 2"
image: /assets/img/headers/tcmsec.webp
---
![tcmsec](/assets/img/headers/tcmsec.webp)

```bash
Default username: John
Default Password: TwoCows2
```

### NIKTO

> Web Vulneribility Scanner

`nikto -host url`

`nikto -h target ip`

![niktoScan](/assets/img/posts/kioptrixwt2_1.webp)
- *Findings*
	1. Outdated Applications - Google common exploits for given Version
		1) Apache
		2) mod_ssl
		3) openssl
	2) mod_ssl
		1) vulnerable to a remote buffer overflow
	3) Little bit of Directory Busting

### DIRBUSTER
> Directory Busting / Finding Folders

> ALternatives: gobuster, dirb, ferox boster

- `dirbuster&`
- insert target url on Target URL section
- Check 'Go Faster'
- Check List based brute force
- Click browse, navigate to `/usr/share/wordlists/dirbuster/`
- Select a list
- File extension: php,txt,zip _choose the extension you want to look for_
_*Note: more extension more time*_
- START
![niktoScan](/assets/img/posts/kioptrixwt2_2.webp)

*Tip: Dir Scan takes a while. It is always a good idea to start the scan as soon as possible so we can do other task while the scan is running in Background.*

![Burpsuite Config](/assets/img/posts/kioptrixwt2_3.webp)

### BURPSUITE

> Security Testing Web Applications

- start Burpsuite
- Setup your browser for burpsuite
- Next, Use Burp default
- Start Burp
- Choose _Proxy_ from Top Menu
- Click on *Intercept is off* to tun it on and Open Browser
![Burpsuite Config](/assets/img/posts/kioptrixwt2_4.webp)

- Open _target url_ on the browser
- on the text area _right click_ > _send to repeater_
- go to New option _repeater_ on top menu
- try changing command and send
- This can modify website
![Burpsuite Config](/assets/img/posts/kioptrixwt2_5.webp)

- Screenshot or save result for info Disclosure
- Go to _Target > Sitemap > Response_
- Screenshot for Info Disclosure
- Turn _Intercept_ Off
![Burpsuite Config](/assets/img/posts/kioptrixwt2_6.webp)


### Dirbuster (again)
> Results are back

- Lets check folders
- _Usage_ seems interesting
- Lets check files in browser
- At the bottom there is *Webalizer 2.01*
- Lets note that

> [!NOTE]
> Check through files and sources for possible Passwords and Leaks


### METASPLOIT

> Exploitation Framework

- `msfconsole`
- msf6 > `search smb`
- You will see many results, lets find _SMB version_
- there's a path _auxiliary/scanner/smb/smb_version_ (Long way to do it)
- `use auxiliary/scanner/smb/smb_version`
- `info`
- We found _RHOSTS_ so far, which stands for _Remote Hosts_
- `set RHOSTS _Target IP_`
- `run`
- We found
	-  Samba 2.2.1a

### SMB Client
> Connect to file share

- `smbclient -L \\\\target ip\\ `
	- _-L_ lists the files
	- use the slashes(\)
- Just Press Enter without Password
![Samba Result](/assets/img/posts/kioptrixwt2_7.webp)

>
NOTE:
Question: My enum4linux and/or smbclient are not working. I am receiving "Protocol negotiation failed: NT_STATUS_IO_TIMEOUT". 
How do I resolve?

> Resolution:
On Kali, edit /etc/samba/smb.conf
Add the following under global:
``` conf
client min protocol = CORE
client max protocol = SMB3
```

- Here we find IPC and $admin , $admin is useful to us lets try it
- Let's try again
- `smbclient \\\\target ip\\ADMIN$`
	- Wrong Password
- `smbclient -L \\\\target ip\\IPC$`
	- We are inside *SMB*
	- `ls` : To list files
	- _ACCESS DENIED_


### SSH
> Remote Login

- From our `nmap scan` we have _OpenSSH version 2.9p2_
- `ssh target_ip`
	- _Their offer: diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1_
- `ssh target_ip -oKexAlgorithms=+diffie-hellman-group1-sha1`
	- It is going to ask for Cypher
- If you get _Their offer: ssh-rsa,ssh-dss_
	- Navigate to ~/.ssh/config
	- add
		HOST _targetip_
			HostKeyAlgorithms +ssh-dss

- Now it asks for _cypher_
- `ssh target_ip -oKexAlgorithms=+diffie-hellman-group1-sha1 -c aes128-cbc`
- Its asks for confirmation _Type: yes_
- It prompts for password
- Lets exit
	- We are not going to exploit yet.

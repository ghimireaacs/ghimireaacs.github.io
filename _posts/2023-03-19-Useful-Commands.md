---
layout: post
title: "Useful Linux Commands for Hacking"
date: 2023-03-19 22:34:31 +1100
category: Hacking
tags: [commands, Hacking, Privilege-Escalation]
description: "A quick-reference sheet of common Linux commands used in penetration testing and CTFs — enumeration, privilege escalation, file transfers, and more."
image: /assets/img/headers/linuxCommands.webp
---


When you land on a Linux machine during a CTF or a pentest, the first thing you do is figure out where you are and what you have. These are the commands I reach for during the enumeration phase. The goal is to understand the system, find the users, map the network, and look for anything that can be leveraged.

I keep this as a reference for myself. You will use different commands depending on the box and the situation, but these cover most of the basics.

## System Enumeration

Command | Description | Example
---------|----------|---------
 hostname | Displays the hostname of the machine | `hostname`
 uname -a | Displays Sys information, may help to find kernel vulneribilities| `uname -a`
 /proc/version | Information about processess, helps to find kernel and compiler info | `/proc/version`
 /etc/issue | Gives info about OS, but can be changed, makes it easy to understand system | /etc/issue
 ps | Displays running processes in a linux system, Displays the following: <ul> <li>PID : The Process ID</li> <li>TTY: Terminal type used by user</li> <li>Time: Amount of CPU  used by the process </li> <li>CMD: The Comman or Executable running.</li></ul> | <ul> <li>`ps -A` : View all running processes</li><li> `ps axjf`: view processes tree</li> <li>`ps aux`: Displays processes for all users.</li></ul>
 env | Displays environmental variables, like PATH which may contain info about compiler or scripting language (eg. PYTHON) which could be leveraged for Privilege escalation | `env`
 sudo -l | Used to display all commands that can be used by current users as sudo | sudo -l
 ls | Lists all the files and folders | <ul><li>`ls`</li><li>`ls -la` : Displays items including Hidden Files and Folders</li></ul>
 id | General overview of user's privilege level and group memberships | `id`
 /etc/passwd | Can be an easy way to discover users on the system | `cat /etc/passwd` or `cat /etc/passwd \| cut -d ":" -f 1`
 history | Displays all the commands used before | `history`
 ifconfig | Info about the network interfaces of the system | `ifconfig`
 ip route | Verifies ifconfig info | `ip route`
 netstat | Gather info on existing connections | <ul><li>`netstat -a` : Shows all listening ports and established connections</li><li>`netstat -at` or `netstat -au`: lists TCP/UDP protocols respectively</li><li>`netstat -l` : Lists ports on Listening mode. These ports are open and ready to accept incoming connections.</li><li>`netstat -lt` : Same as netstat -l but displays TCP connections only</li><li>`netstat -s` : list network usage statistics by protocol This can also be used with the -t or -u options to limit the output to a specific protocol. </li> <li>`netstat -tp` : Lists connections with service name and PID info.</li><li> `netstat -ltp` : to list listening ports</li> <li>`netstat -i` : shows interface stats</li><li>`netstat -ano` : <ol><li>`-a`: Display all sockets</li><li>`-n` : Do not resolve names</li> <li>`-o` : Display Timers</li></ol></li></ul>

---

## Find Command

`find` is one of the most useful commands for privilege escalation. You use it to hunt for files with specific permissions, SUID bits set, or files owned by root. Those are often your path to escalating privileges on a box.

Command | Description
--------|------------
`find . -name notes` | Finds the file named "Notes"
`find /home -name notes` | Finds the filename in home directory.
`find / -type d -name config` | Find the directory named config under "/"
`find / -type f -perm 0777` | Find files with the 777 permission (Read, Write and Execute)
`find / -perm a=x` | Find all executable files
`find / -perm -u=s -type f` | Find files with SUID bit set. These run as the file owner, not the caller. If root owns a SUID binary you can often abuse it.
`find / -writable -type d` | Find world-writable directories. Useful for dropping files.

## What To Do With This

Enumeration is about building a picture. You are not looking for one thing. You run these commands and look at the output together. What users exist? What services are running? What ports are open? Is there anything misconfigured?

The more you do it the faster you get at spotting what does not belong.

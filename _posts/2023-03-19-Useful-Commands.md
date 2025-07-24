---
layout: post
title: "Useful Linux Commands for Hacking"
date: 2023-03-19 22:34:31 +1100
category: Hacking
tags: [commands, Hacking, Privilege-Escalation]
description: "Common Linux Commands for Hacking."
image: /assets/img/headers/linuxCommands.webp
---


Common Linux Commands for Hacking.


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


# Find Command


Command | Description
--------|------------
`find . -name notes` | Finds the file named "Notes"
`find /home -name notes` | Finds the filename in home directory.
`find / -type d -name config` | Find the directory named config under "/"
`find / -type f -perm 0777` | Find files with the 777 permission (Read, Write and Execute)
`find / -perm a=x` | ''''

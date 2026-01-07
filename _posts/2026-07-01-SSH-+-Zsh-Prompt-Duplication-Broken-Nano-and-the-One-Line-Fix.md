---
layout: post
title: "SSH + Zsh Prompt Duplication, Broken Nano, and the One-Line Fix"
date: 2026-01-07 09:02:00 +1100
category: Linux
tags: [ssh, zsh, homelab]
description: "While migrating to a Linux workstation with a modern terminal (Ghostty), Zsh, Oh My Zsh, and Powerlevel10k, I encountered a severe and confusing issue."
image: /assets/img/headers/p10kbug.webp
---
## Background
So with latest windows Updates its so hard to stay now, almost like they want you out. So i decided to use Linux as main gig again. Now i use Linux on my Laptops and Servers, it's even as secondary boot in my main workstation. But i play invasive games like Valorant, FIFA and GTA Online (Now Borked in Linux) with my friends, i have to run Windows. 
Now this story will continue somewhere else.
So recently i have decided to build a real, usable, stable Linux system for my main workstation.

## Configuration

Here is what i have decided to go with, for my system.

### Main Rig

| MAIN RIG     |            |
| ------------ | ---------- |
| Distro       | Arch Linux |
| Desktop Env. | KDE Plasma |
| Shell        | ZSH        |
| Terminal     | Ghostty    |

Even though i have pretty beefy rig i wanted it to be less bloat, so i chose `ghostty` from get go and removed `konsole`. Also set one application per purpose. I mean i even cut down terminal, who could go cheaper than that? I also have a `bootstrapped` dotfiles, which was repurposed from Workstation to Server dotfiles at `https://github.com/ghimireaacs/serverdotfiles`. So all my servers are configured using this. Hence all of them have:

### Servers

| SERVERS      |                  |
| ------------ | ---------------- |
| Distro       | Ubuntu           |
| Desktop Env. | NONE             |
| Shell        | ZSH              |
| Terminal     | SSH client-owned |

### DOTFILES

| DOTFILES Components |     |
| ------------------- | --- |
| Oh My Zsh           |     |
| Powerelvel10k       |     |
| Custom Aliases      |     |
| Custom Exports      |     |
| Custom .zshrc       |     |

---

I also recently updated them so i could have same aliases and system running everywhere so its seamless, however i also wanted my servers and workstation to look and behave slightly different, because each have their own need. So i updated the files again, and bootstrapped with my workstation.
Now it does auto finds distro and installs needed packages accordingly, also has multiple identifiers for workstation and server so it behaves a certain way. I thought this will be the problem but they were fine.
I installed in my main rig, Voila, worked like a charm. I reconfigured this, adjusted with necessary changes, modified prompts and `git push`.


![](assets/img/posts/20260107182116.webp)



## Problem

> **Question:** So what broke?
{: .prompt-tip }


At first i got this multiple prompts which looked weird on its own, which i thought was a minor bug. Then i tried to clear screen with `ctrl + l` and it failed. Then i started to type something, well i got double of same things, and it was broken.


![](assets/img/posts/20260107182648.webp)




### Troubleshooting

Now after this i tried a bunch of different things i don't remember in order but most obvious were: 

1. Changing shell from `zsh` to `bash`
  So I was already on remote, i switched to bash, it fixed some problem like the prompts weren't weird  anymore, however `ctrl + l` didn't behave like it should. It did't clear console but did got to new line, which turns out to be terminal capability issue. I did find a 🗝️ clue here, but i treated it as another sort of problem. I also tried changing local `zsh` to `bash`and then ssh to remote, problem persisted. 
2. Changing Terminal from `ghostty` to `kitty`
 Even after switching to a completely different terminal `kitty`, well you guessed it, same problem.
3. Changing OS
 Now NO! I did not nuke my system again, i booted back to my Windows, ssh from there, guess what? No error! This made me sure there was something wrong with my `ZSH` or `ghostty` config or my Entire `dotfiles`, well mostly `.zshrc`.
4. Cleared `ZSH CACHE` before launching ssh.
5. Tried `zsh -f`, `zsh -T` none of them worked.
6. Tried changing SERVER Config
 So remember when i said i got a clue? I tried `nano ~/.zshrc` to make changes on server side, there now i had that again.
 `Error opening terminal: xterm-ghostty.`
 There, there's the solution.

> **BUG:** Error opening terminal: xterm-ghostty.
{: .prompt-warning}

## Root Cause

Turns out when we SSH, the client exports the `TERM` environment variable to the server.
Since we have `TERM=xterm-ghostty` in our local machine, it sent exactly that. Now my server received this and used this, since the server did not have a matching `terminfo` entry for `xterm-ghostty`, this caused terminal capability misinterpretation.


## Solution

Now i use `config` file for my ssh, this helps me simplify my hostnames, have different private keys tied to different machines and its portable, so far. Until i needed to add this one more configuration:

```ssh

Host *
    SetEnv TERM=xterm-256color

```

This configuration helps me have a consistent TERM across all my hosts.

---

There that's the solution.

## TL;DR

- I wanted a pretty, functional prompt across my workspace and servers.
- I used ZSH, OMZ and  `ghostty` terminal to achieve this.
- This introduced a `TERM` mismatch across SSH sessions.
- Setting a consistent `TERM` in `config` file solved it.

> **Tip:** Set `TERM` in your SSH config to avoid terminal capability issues.
{: .prompt-tip }



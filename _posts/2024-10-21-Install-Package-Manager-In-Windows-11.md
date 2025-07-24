---
layout: post
title: "Update All Apps with One Line Of Code in Windows"
date: 2024-10-21 05:19:38 +1100
category: Windows
tags: [Windows, Winget, Software, Install]
description: "Winget is CLI tool that Installs, Updates and List All softwares on your windows machine, similar to apt-get, brew, pacman, nix, etc"
image: /assets/img/headers/winget.webp
---

Its a headache to update each softwares on Windows. Its tough to update something manually.
We do not use Microsoft Store, Microsoft. Please Leave us alone. With said that, Microsoft
store do have a very important application there though and we can use that to update any
and everything, well most of it.
[Winget](https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1)

## Winget

Winget is an Open Source Windows Package Manager designed to run from Command Line Interface (Terminal). From one simple command you can Install your favorite package, uninstall non-necessary ones and Update, those needed to be updated. Also it lists all the package you have installed in your system, and export it. You can format your pc and install all those packages by importing them, or give it to your non tech savvy friends so they can install those cool softwares.

## Let's Dive into it

Winget comes pre installed in Windows 11(21H2 and later).
To verify this
Go to Terminal and execute following command:
    
    `winget –version`

If it shows the version Skip the installation part, otherwise follow the installation.

## Install Winget:

Go To [Winget](https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1).

It will open Microsoft Store. Click on Get.
Once Installed, restart your pc.

## Running Winget

Head straight to terminal and execute following command:

- Winget Help

        winget --help


- Find Winget Packages

        winget find vscode

This will look for vscode in the Packages.
'Id' is very useful here, you may want to copy it.(just select and right click)

Lets install VScode.

    winget install Microsoft.VisualStudioCode` (right click for paste)

So installation is done.

Lets see the list,

    winget export -o C:\Path\to\exported.json

Similary to import

    winget import -i C:\Path\to\exported.json

## Upgrade

To upgrade all available packages:

    winget upgrade --all

Follow the Prompts and....
Done!

## Wrap Up

- Install winget
- Install, Update and Uninstall from CLI
- Upgrade Everything available with one line
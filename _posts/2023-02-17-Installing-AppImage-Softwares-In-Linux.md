---
layout: post
title: "Install AppImage Softwares in Linux"
date: 2023-02-17 03:10:16 +1100
category: Linux
tags: [Linux, AppImage, Software, Install]
description: "How to Install AppIMages Software in Linux"
image: /assets/img/headers/appimg.webp
---

AppImage is a software Distribution format for Linux. It is getting popular these days for the following reasons.

---

## Why to use AppImage?

1. <mark>Portable</mark> : They can run on Multiple Linux Distribution without modification and without compatibility issue.
2. <mark>Versatile</mark> : It can be used to distributed as Graphical or Command Line applications.
3. <mark>Convenient</mark> : Can be downloaded and run with single click without any administrative privileges or installation.
4. <mark>Easy To Use</mark> : AppImages are self Contained software. There is no need to install any dependencies or libraries. This makes installation process easier and faster.

---

## How To Integrate on System

1. Download the appImage file
2. Download icon for your app
3. Copy Both files it on folder /home/user/folder/
4. Right click on the appImage file,
5. click Permission
6. Check ‘Allow executing file as program’
    or 
    
    `chmod +x ~/folder/minecraft.AppImage`
7. Create a text File



   ```
    [Desktop Entry]
    Type=Application
    Name=Minecraft
    Comment=Minecraft
    Icon=/home/user/folder/Minecraft/icon.png
    Exec=/home/user/folder/Minecraft/minecraft
    Terminal=false
    Categories=Minecraft;game
    ```

> 💡 **Tip:** Here, Icon is place of your icon and Exec is location of your application. We are using Minecraft as example here. Replace these with your folder and file names.

8. Save file in `.local/share/applications/appName.desktop`
9. Save as .desktop format.
10. Log Out or Restart System.

---

And now you can run your appImage as usual application without problem.

## Uninstall

Simply Delete those 2 files. Voila.

---

Despite Being One of the User Friendly Format, Flatpaks are considered better due to its security and Can be updated later.
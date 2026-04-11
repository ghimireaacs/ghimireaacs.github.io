---
layout: post
title: "Install AppImage Softwares in Linux"
date: 2023-02-17 03:10:16 +1100
category: Linux
tags: [Linux, AppImage, Software, Install]
description: "AppImage is a portable software format for Linux. Learn how to download, make executable, and run AppImage applications on any Linux distro without a package manager."
image: /assets/img/headers/appimg.webp
---

I had a piece of software that was only available as an AppImage. No snap package, no apt repo, just the AppImage file. I had no idea what to do with it at first. Turns out it is straightforward once you know the process.

AppImage is a software distribution format for Linux. It is getting popular these days for the following reasons.

---

## Why to use AppImage?

1. <mark>Portable</mark> : They can run on Multiple Linux Distribution without modification and without compatibility issue.
2. <mark>Versatile</mark> : It can be used to distributed as Graphical or Command Line applications.
3. <mark>Convenient</mark> : Can be downloaded and run with single click without any administrative privileges or installation.
4. <mark>Easy To Use</mark> : AppImages are self Contained software. There is no need to install any dependencies or libraries. This makes installation process easier and faster.

---

## How To Integrate on System

By default you can just double click an AppImage and it runs. But that means it does not show up in your application launcher, there is no icon in the taskbar, and it does not feel like a real installed application. The desktop entry file fixes that.

1. Download the AppImage file
2. Download an icon for your app (PNG works fine)
3. Copy both files to a folder like `/home/user/Apps/AppName/`
4. Make the AppImage executable. Right click the file, go to Properties, Permissions, check "Allow executing file as program". Or just run:

    `chmod +x ~/Apps/AppName/appname.AppImage`

5. Create a `.desktop` file. This is what tells your system how to show the app in the launcher.

   ```
    [Desktop Entry]
    Type=Application
    Name=Minecraft
    Comment=Minecraft
    Icon=/home/user/Apps/Minecraft/icon.png
    Exec=/home/user/Apps/Minecraft/minecraft.AppImage
    Terminal=false
    Categories=Game;
    ```

> `Icon` is the full path to your icon file. `Exec` is the full path to your AppImage. Replace the Minecraft references with your actual app name and paths.
{: .prompt-tip }

6. Save the file to `.local/share/applications/appname.desktop`
7. Log out or restart your session.

---

Now the app shows up in your application launcher like any other installed software. You can pin it, search for it, done.

## Uninstall

Delete the AppImage file and the `.desktop` file. That's it. Nothing else was installed on your system.

## AppImage vs Flatpak

AppImage is portable and simple but it does not sandbox the application. Flatpak is considered more secure because it runs apps in a sandbox and handles updates through a proper store. If both options exist for an app I would go with Flatpak. But if AppImage is the only option, now you know how to use it properly.
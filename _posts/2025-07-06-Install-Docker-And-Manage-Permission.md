---
layout: post
title: "Installing Docker and Setting Permission"
date: 2025-07-06 01:11:31 +1100
category: Homelab
tags: [docker, linux, ubuntu, containers, homelab, permissions]
description: "How to install Docker on Linux using the official apt repository and configure user group permissions so you can run containers without sudo."
image: /assets/img/headers/dockerInstall.webp
---


Every server I set up eventually needs Docker. There are a few ways to install it. Snap is one option but I avoid it because it adds a lot of overhead and snap packages have caused me issues before. There is also the convenience script that pipes a shell script directly into bash from the internet, which I am not comfortable running on production machines.

The right way is the official apt repository method from Docker's own documentation. It takes a couple of extra steps but you get the latest stable version from a verified source and full control over updates.

The permissions step at the end is important and most guides skip explaining why. By default Docker runs as root. Every `docker` command requires `sudo`. That gets tedious and causes permission errors when containers try to write files to bind mounts. Adding your user to the `docker` group means you run everything without sudo. Just make sure you trust who else is in that group since docker group access is effectively root access on the host.

## Installing Docker

1. Setup docker's apt repo

    ```bash
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

2. Install Latest Docker and its dependencies

    `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

3. Create Docker group (Most likely already created)

    `sudo groupadd docker`


4. Add user to the group

    `sudo usermod -aG docker $USER`


5. Logout and Log Back in or restart or ..
	
    `newgrp docker`



> This will ensure you will not need to run "sudo" everytime you run docker and also fixes most Permission error.
{: .prompt-warning }

If you run into DNS issues inside containers after this setup, see [Broken Docker DNS Due to Pi-hole](/posts/Broken-Docker-DNS-Due-to-PiHole/) — a common gotcha on systems that have previously run Pi-hole.

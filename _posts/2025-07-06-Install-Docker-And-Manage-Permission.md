---
layout: post
title: "Installing Docker and Setting Permission"
date: 2025-07-06 01:11:31 +1100
category: Walkthrough
tags: [docker, homelab]
description: "Installing Docker and Setting Permission"
image: /assets/img/headers/dockerInstall.webp
---


# Installing Docker

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



> [!WARNING]
> This will ensure you will not need to run "sudo" everytime you run docker and also fixes most Permission error.

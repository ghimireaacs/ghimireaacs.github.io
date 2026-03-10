---
layout: post
title: "Broken Docker DNS Due to Pi-hole"
date: 2026-03-11 00:00:00 +1100
category: Homelab
tags: [docker, dns, pihole, networking, debugging]
description: "Docker containers couldn't resolve DNS despite correct daemon.json config. The real culprit was Pi-hole's leftover nftables rules redirecting all DNS traffic to a closed port."
image: /assets/img/headers/dockerBrokenDNS.webp
---

New container, can't resolve DNS. Classic. Except this time I'd already set the DNS in `daemon.json`, restarted Docker, checked iptables — everything looked right. Ping worked. DNS didn't. Spent way too long on this one.

Here's what actually happened.

## Symptoms

- New Docker containers can't resolve DNS
- `nslookup google.com` inside container returns `connection refused` or `no servers could be reached`
- `ping 1.1.1.1` from inside the same container works fine
- Existing containers on manually created networks work
- `docker run --rm --network host busybox nslookup google.com` resolves fine

## Everything I Checked That Wasn't The Problem

- `daemon.json` — DNS correctly set, config validated with `dockerd --validate`
- systemd override — bare `dockerd` was running and reading `daemon.json` correctly
- iptables FORWARD chain — DOCKER-FORWARD had all the right ACCEPT rules
- MASQUERADE rules — all bridge subnets were covered in POSTROUTING
- Bogon blocking on OPNsense — not enabled
- Removed TCP port 2375 exposure — good cleanup but didn't fix DNS
- `/run/docker.sock` was a **directory** instead of a socket file — fixed it, DNS still broken

## The Actual Root Cause

Pi-hole's nftables rules were redirecting all DNS traffic to port 55, even though Pi-hole hadn't been running for a while.

When Pi-hole runs as a Docker container it injects rules into the nftables `ip nat PREROUTING` chain to intercept DNS:

```
udp dport 53 redirect to :55
tcp dport 53 redirect to :55
```

These rules **do not get cleaned up** when you stop or remove the container. So with nothing listening on port 55 anymore, every DNS query from every container was getting an ICMP port unreachable back — which shows up as "connection refused" in nslookup.

The reason ping worked but DNS didn't is straightforward: ICMP doesn't touch port 53, so MASQUERADE and routing worked fine. DNS specifically hits the redirect rule and dies there.

You can spot it instantly:

```bash
sudo nft list ruleset | grep -E "53|redirect"
```

## Fix

Find the rule handles and delete them:

```bash
# See the handles
sudo nft -a list chain ip nat PREROUTING | grep "redirect to"

# Delete by handle number
sudo nft delete rule ip nat PREROUTING handle <handle_number>
```

Or do it in one shot:

```bash
sudo nft delete rule ip nat PREROUTING handle $(sudo nft -a list chain ip nat PREROUTING | grep "redirect to :55" | grep udp | awk '{print $NF}')
sudo nft delete rule ip nat PREROUTING handle $(sudo nft -a list chain ip nat PREROUTING | grep "redirect to :55" | grep tcp | awk '{print $NF}')
```

Verify:

```bash
docker run --rm busybox nslookup google.com
```

## Bonus: The Docker Socket Was a Directory

While debugging I also found `/run/docker.sock` was a directory instead of a socket file, which is why `docker` commands weren't connecting. Likely caused by a failed Docker startup writing to the path before the socket was created.

```bash
sudo systemctl stop docker docker.socket
sudo rm -rf /run/docker.sock
sudo systemctl start docker.socket
sudo systemctl start docker
```

## Takeaways

- If Docker DNS fails but ping works, check nftables before anything else
- Pi-hole does not clean up its nftables rules on removal — you have to do it manually
- `docker run --rm --network host busybox nslookup google.com` is a fast way to confirm whether the issue is bridge networking or something deeper

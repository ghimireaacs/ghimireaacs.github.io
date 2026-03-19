---
layout: post
title: "Syncthing Three-Way Sync Across VLANs"
date: 2026-03-20 00:00:00 +1100
category: Homelab
tags: [syncthing, vlan, networking, opnsense, docker, selfhosted]
description: "Set up Syncthing across three devices on different VLANs. Local discovery breaks, direct connections fail silently. Here's what actually fixed it."
image: /assets/img/headers/syncthingVlan.webp
---

Wanted Syncthing running across three devices: a server on the utility VM, my Windows PC, and my Pixel. Files sync everywhere, no cloud, no Dropbox. Simple enough in theory.

My network runs five VLANs on OPNsense. Servers on VLAN 10, PC on VLAN 50, phones on VLAN 20. This caused every problem.

## The Setup

Syncthing server running in Docker on the utility VM (`10.10.10.114`) on VLAN 10. Windows PC on VLAN 50. Pixel on VLAN 20. Global discovery and relay turned off so sync traffic stays on the LAN.

The goal was hub-and-spoke plus direct: everything syncs to the server, but phone and PC also sync directly when both are on the LAN.

![](assets/img/posts/syncthingTwoDevices.webp)


## Problem 1: Nothing Connects

With global discovery and relay disabled, Syncthing needs to know exactly where to reach each device. Local discovery uses UDP multicast on port 21027 which does not cross VLAN boundaries. So every device just sat there with "Last seen: never."

The fix is to stop relying on discovery and pin addresses manually. The rule is simple: stationary hosts get pinned, mobile devices get `dynamic`.

| Device entry | Address |
|---|---|
| Server (as seen from any client) | `tcp://10.10.10.114:22000` |
| Windows (as seen from Pixel) | `tcp://10.10.50.100:22000` |
| Phone (as seen from anyone) | `dynamic` |

The phone's IP changes across networks so you can't pin it. Let the phone always dial out.

One thing that tripped me up: Syncthing has a "device defaults" setting under Actions > Settings. Changing the address there only applies to new devices you add going forward, it does **not** update existing devices. You have to go into each existing device and change the address individually.

![](assets/img/posts/pixelSyncthing.webp)



## Problem 2: Phone and PC Would Not Talk

VLAN 20 (Personal) had no path to VLAN 50 (PC) in my firewall rules. Adding the OPNsense rule was straightforward but it had to go **above** the existing block rule for that VLAN pair. First match wins in OPNsense. My Syncthing pass rule was sitting below a block rule and never getting evaluated.

Correct order on the PERSONAL interface:

```
Pass   PERSONAL net   SERVERS net     any
Pass   PERSONAL net   TENANTS net     any
Pass   PERSONAL net   IOT net         any
Pass   PERSONAL net   PC net          TCP/UDP  22000   <- Syncthing exception
Block  PERSONAL net   PC net          any              <- everything else blocked
Pass   PERSONAL net   *               any              <- internet catch-all
```

![](assets/img/posts/firewallRule.webp)



## Pairing Devices

Do not manually type device IDs. When an unknown device tries to connect the UI shows a banner notification: "Device X wants to connect, Add?" Click that, both sides approve each other and you are done. Typing IDs manually is error prone and slower.

## End State

Three-way sync working. Server and Windows, server and Pixel are the main sync paths. Pixel and Windows direct also works when both are on the LAN. All connections show direct LAN IPs, no relay.

![](assets/img/posts/diagramSyncthing.webp)



![](assets/img/posts/syncthingDevices.webp)



## Takeaways

- Local discovery (UDP multicast) does not cross VLANs, pin addresses instead
- "Device defaults" in Syncthing does not update existing devices, change each one manually
- Firewall rule order matters, pass rule must sit above any block rule for the same destination

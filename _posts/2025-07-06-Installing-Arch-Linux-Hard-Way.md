---
layout: post
title: "Installing Arch Linux Hard Way"
date: 2025-07-06T01:11:31+11:00
categories: Walkthrough
tags: arch archinstall install Linux
description: "Installing Arch Linux Hard Way"
image:
 path: /assets/img/headers/ArchInstall.webp
---


## Before Installation

- Backup your data
- Download [Balena Etcher](https://etcher.balena.io/) & [ISO of ARCH Linux](https://archlinux.org/download/)
- Burn ISO to a USB
- Restart

## Boot

- Press DEL and load to BIOS mode
- Change Boot Priorities to USB
- Reboot

## ARCH

- Load 'Arch Linux Install Medium'

- Connect Your Arch to internet
	
	`iwctl --passphrase "$WIFIPASSWORD" station wlan0 connect $WIFINAME`

- ping 8.8.8.8
	
	- If you get bytes back you are connected

- Check if you are on UEFI mode
	
	`efivar -l`

- List your disks (Remember your diskname you want to install Arch to)
	
	`lsblk`
	
	> for me its *sdc*

- Split up Partition and Prepare your Drive

	`gdisk /dev/sdc`
	
	> CHOOSE YOUR DRIVE CAREFULLY

	`x` for 'expert'
	`z` for 'Zap'
	"Y" to WIPE DISK
	"Y" again to Confirm

- Verify partitions
	`lsblk` - notice there is no partition on your disk

- Partitioning
	
	`cgdisk /dev/sdc`
- Press any key to continue
> We are using cgdisk because its easier, relatively.

- Separate ROOT and HOME Partition
	> Root Partition: Where all OS Files will be stored
	> Home Partition: Where all General Files will be Stored

- Use your keyboard and highlight "NEW" press "ENTER"
- First Sector: (Default):  (leave Blank and press "ENTER")
- Size in Sectors: 1024MiB
	- 1 GB for Boot Drive 
- Hex Code for GUID: 'EF00'
- Name your Drive: 'boot'

- SWAP MEMORY
	> When you run out of RAM this memory is used.
	> Make this regardless of your RAM Size
	
	- Highlight  and go to BIG size 'free space' (probably 3rd option)
	- "NEW" again
	- First Sector: (Default):  (leave Blank and press "ENTER")
	- Size in Sectors: 16GiB
		- 16 GB for SWAP Drive 
	- Hex Code for GUID: '8200'
	- Name your Drive: 'swap'

- BOOT Partition
	- Highlight  and go to BIG size 'free space' (probably last option)
	- "NEW" again
	- First Sector: (Default):  (leave Blank and press "ENTER")
	- Size in Sectors: 40GiB
		- 40 GB for Root Drive 
	- Hex Code for GUID: '8300'
	- Name your Drive: 'root'

- Home Partition
	- Highlight  and go to BIG size 'free space' (probably last option)
	- "NEW" again
	- First Sector: (Default):  (leave Blank and press "ENTER")
	- Size in Sectors: (Default):  (leave Blank and press "ENTER")
	- Hex Code for GUID: '8300'
	- Name your Drive: 'home'
- Use your arrows key to select "Write"
- Confirm with "yes"
- And arrows key to "Quit"
- `clear`

- Formatting Drives
	- `lsblk` to confirm drives again
	- `mkfs.fat -F32 /dev/sdc1`
		> File Allocation Table
	- `mkswap /dev/sdc2`
		> To make swap format
	- `swapon /dev/sdc2`
		 Enable Swap
	- `mkfs.ext4 /dev/sdc3`
		'y' to confirm if it asks
	- `mkfs.ext4 /dev/sdc4`
		> Hint: press up arrow and change sdc3 to sdc4

- Mounting the drives
	`mount /dev/sdc3 /mnt`
	`mkdir /mnt/boot`
	`mkdir /mnt/home`
	`mount /dev/sdc1 /mnt/boot`
	`mount /dev/sdc4 /mnt/home`
	> Basically we are making folder and structuring it with proper drives and partitions we made earlier.

- Update Mirrorlist
	`cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup`
	> We are just Backing up incase we mess something up.
	`rankmirrors`
		> This is to find Fastest mirror suitable to YOU.
		> If you find error install rankmirrors
		`sudo pacman -Sy pacman-contrib`
		Press Enter to confirm
	`rankmirrors -n 6 /etc/pacman.d/mirrorlist.backup > /etc/pacman.d/mirrorlist`
		> This will be working so system isn't hang, Wait till it shows root@Archiso.
		> What it did was found best mirrors and copied it to your mirrorlist
	 `cat /etc/pacman.d/mirrorlist`
	 > shows what we did earlier, so yeah ranked mirrorlist
	 
- INSTALLING NOW
	`pacstrap -K /mnt base linux linux-firmware base-devel`
		> We are installing Base Linux.

	`genfstab -U -p /mnt >> /mnt/etc/fstab`
		> setup all the drives and structure so hard drive is recognized while booting

- Booting into Installation
	`arch-chroot /mnt`
- Install  'nano' and 'bash-completion'
	`sudo pacman -S nano bash-completion`
		Enter to confirm
		
- Enable Locales
	`nano /etc/locale.gen`
		- Find your locale (for me its en_AU.UTF-8 UTF-8)
		- remove # from its front
		- hit 'ctrl o' and press enter to save 
		- hit 'ctrl x' to close
	
	`locale-gen`
	`echo LANG=en_AU.UTF-8 > /etc/locale.conf`
	`export LANG=en_AU.UTF-8`

- TimeZone
	`ls /usr/share/zoneinfo/`
		> From here select your country and press tab
		> It will list your Timezone
		> write few characters of your TZ and press Tab
	Move to first part of your script and change, mine is Australia Sydney so i will be doing this:
	`ln -s /usr/share/zoneinfo/Australia/Sydney > /etc/localtime`

	`hwclock --systohc --utc`
	> We are syncing time with BIOS time so Your PC has right time every time you open it. 

- Hostname
	
	`echo archish > /etc/hostname`
	
	> instead of 'archish' use whatever name you want

- IF YOU HAVE SSD
	`systemctl enable fstrim.timer`

- Enable 32 bits packages
	`nano /etc/pacman.conf`
		Go all the way down to \[multilib] and remove # from both line
	`sudo pacman -Sy`

- SET USER AND PASSWORDS
	- set root password
		`passwd`
		> Type password enter, it wont show it but its writing
	- add user
		`useradd -m -g users -G wheel,storage,power -s /bin/bash ghost`
			> instead of ghost write your own username
	- give that user password
		`passwd ghost`
		Type password and enter.
- Modify sudo file
	`EDITOR=nano visudo`
		Opens sudo file
	Search for %wheel
		use 'ctrl w'
	find '%wheel ALL=(ALL:ALL)ALL'
	Uncomment it (remove # from front)

- BootLoader
	`mount -t efivarfs efivarfs /sys/firmware/efi/efivars/`
- Install bootloader
	`bootctl install`
- Write entries for boot loader
	`nano /boot/loader/entries/arch.conf`
	Write the 3 lines
	```
	title ARCH
	linux /vmlinuz-linux
	initrd /initramfs-linux.img
``
> save and exit (ctrl o and ctrl x)

- Point to your harddrive
	`echo "options root=PARTUUID=$(blkid -s PARTUUID -o value /dev/sdc3) rw" >> /boot/loader/entries/arch.conf`
	> This hardcode your UID of partition to your bootloader

	`ip link`
	 Know your network

- enable 'dhcpcd'
	`sudo pacman -S dhcpcd`
	`sudo sydtemctl enable dhcpcd@wlan0.service`

- install NetworkManager
	`sudo pacman -S networkmanager`
	`sudo systemctl enable NetworkManager.service`
- install linux headers
	`sudo pacman -S linux-headers`
## IF YOU HAVE GPU

### NVIDIA

`sudo pacman -S nvidia-dkms libglvnd nvidia-utils opencl-nvidia lib32-libglvnd lib32-nvidia-utils lib32-opencl-nvidia nvidia-settings`

`sudo nano /etc/mkinitcpio.conf`
- Inside MODULE=() add these in exact order, it should look like this
	`MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)`
- make sure they are loaded during boot time
	`sudo nano /boot/loader/entries/arch.conf`
- right after options line, after rw, in same line
	`nvidia-drm.modeset=1`
- Hook for pacman to update nvidia driver
	`sudo mkdir /etc/pacman.d/hooks`
	`sudo nano /etc/pacman.d/hooks/nvidia.hook`
	Add
	```
	[Trigger]
	Operation=Install
	Operation=Upgrade
	Operation=Remove
	Type=Package
	Target=nvidia

	[Action]
	Depends=mkinitcpio
	When=PostTransaction
	Exec=/usr/bin/mkinitcpio -P
``

## Everyone Again

`exit`
`umount -R /mnt`
`reboot`

> You can plug out the USB

When the system boots up, use your credentials to login.

If you cannot connect to internet
`nmtui`
- Activate a Connection
- and Connect

- Now lets install x11 for KDE
	`sudo pacman -S xorg-server xorg-apps xorg-xinit xorg-tvm xorg-xclock xterm`
- to test
	`startx`
	if clocks shows up its installed, click any terminal u see and
	`exit`

## Install Plasma or Any Desktop Environment you want

`sudo pacman -S plasma sddm`
- enter password
- just keep entering Enter

- Enable SDDM
 `sudo systemctl sddm.service`

REBOOT



> 💡 This is straight method to install arch linux "hard way". If you get any error or prefer different way, consult [Arch Wiki Installation Guide](https://wiki.archlinux.org/title/Installation_guide).
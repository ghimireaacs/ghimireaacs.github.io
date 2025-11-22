---
layout: post
title: "How I Utilize Github to Store and Download My Public SSH Keys"
date: 2025-08-09 03:32:00 +1100
category: Homelab
tags: [ssh, homelab]
description: "Store your SSH Public keys on Github, Import them and Run them without a lot of configuration at the start."
image: /assets/img/headers/githubssh.webp
---

The first thing I do after I install a fresh new VM is SSH into that machine and use it locally. Now i will not rant about SSH and its uses and why you need it or why it's better than web console. So, let's get to the point.

## Logging In

There are two ways we can login to server:

1. Key Pair Method
2. Username/Password

Although SSH is very secure protocol in on itself, it is not totally immune to Bruteforce attack and other Human Errors that could lead to some error. By allowing users to login with <mark style="background: #FF5582A6;">Username and Password</mark>, we leave the machine vulnerable to such attacks. And that's here <mark style="background: #BBFABBA6;">KeyPair Method</mark> comes.

<mark style="background: #BBFABBA6;">KeyPair Method</mark>: In this method we will have a Public Key and Private Key. Each of the keys are a long random complex characters As their name suggest one can be Public and another should be kept very securely.

For our intense and purpose, Public Keys are stored in Remote Server and Private Keys are stored in Our Private Machine.

![](assets/img/posts/8898976de2367d86c92f90b095b64c16.webp)

## Generating Key Pair

Now before we move on to server setup, let's create a key pair.

1. Open your CLI
2. `ssh-keygen -t ed25519 -C "username@email.com"`
   ![](assets/img/posts/0bbec1ea9a1d9bef9e78ecf8166e8980.webp)
3. Set a Passphrase. (This is not SSH password it's extra layer of security to use you private key.)
   ![](assets/img/posts/5b5ef986d2597846f46e73e547763d8a.webp)
   > 💡 I choose default name so i do not have to provide '-i keyfile' during login. But if you have multiple private key for different purpose you can name them accordingly.

Now you will have 2 files. Private key: `id_ed25519` and Public key with `.pub` extension: `id_ed25519.pub`, in your ~/.ssh directory.

### Permissions

Make sure you have correct permission set for your keys when you download or paste it in a file. You do not need to worry about permission on the files created by the command however if you choose to backup or copy it in another file you should set the following permission.

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_25519
chmod 644 ~/.ssh/id_25519.pub
```

## Storing The Keys

### Private Keys

This should always be on your local machine and nowhere else but you can use Password manager like Bitwarden for backup.

### Public Keys

Now this is the best part, you can store this anywhere but i would recommend it to store in Github or Launchpad. For me, I use Github a lot so i choose Github.

1. Go to Github Settings
   ![](assets/img/posts/ebde93544f57e002c486e5b57e611c2c.webp)
2. On Access Tab choose `SSH and GPG Keys`
   ![](assets/img/posts/9c6fe9e312380988b65b7521a0a2aff3.webp)
3. Click on New SSH Key
   ![](assets/img/posts/62e39e14921f61e435decc112e9c2a96.webp)
4. Set a Title, Key Type: `Authentication Key`
5. Key: Now paste contents of `id_25519.pub` ‼️ Check its `.pub`.
6. Add SSH Key
   ![](assets/img/posts/069032f2bce598e18d1e8885fd000002.webp)
7. Fill up your 2FA and Submit.

Now you will see List of public Keys in your account.
We will leave this for now and retrieve them from our CLI/shell.
![](assets/img/posts/4b7ea49059630d1ed0c79f2c148753d0.webp)

## Accessing The Public Key

Now just like almost everything in life there are multiple ways we can do this.

1. Manual Method
2. Automatic Method

### Manual Method

This is the method where we simply copy and paste our public key into a file.

1. Copy the content of `id_25519.pub`
2. Paste it in `~/.ssh/authorized_keys` and save it.
3. Check Permission of the `authorized_keys` or just change it from command
   `chmod 644 ~/.ssh/id_25519.pub`.
4. Done.

Now this method is not much of a task on itself if you want to do once or not store public key in some Publicly accessible repo itself. But there is better way we can do it and integrates perfectly and seamlessly with any workflow.

### Automatic Method

Given you have to go through setup process but just like any automation once you set it. All you need is One command line. And it will retrieve your Public SSH key and make your machine accessible by you.

`ssh-import-id-gh github-username`

That's it that's all you need.
Copy this command, change it to the `github-username` you saved your public key to and done.

Now you can access your Machine.

> 💡 Pro Tip: If your private key is compromised in anyway remove this newly added line from `authorized_keys`.

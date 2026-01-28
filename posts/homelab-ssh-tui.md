---
title: "Homelab SSH Dashboard"
slug: "homelab-ssh-tui"
date: "2026-01-27"
tags: ["tui", "python", "homelab"]
---

This is a terminal UI I built to quickly view and manage my home lab. It allows me to easily see if my servers or VMs are up and easily SSH into them. And yes, I used Arch, BTW.

### What it does
- Shows host status and quick actions
- SSH shortcuts
- Displays key info in one place

## Screenshots
![Main screen](/static/img/homelab-ssh-tui/main.png)


![Active connection](/static/img/homelab-ssh-tui/active_connection.png)

## Notes / Lessons learned
My initial plan was to open the SSH connection within the TUI. When I was experimenting with this I discovered I would have to basically create my own terminal within Python. I eventually decided to open the SSH connection in a separate terminal. This allowed my custom themes and any terminal functions to work with minimal effort. All in all, I am very happy with how this project turned out and will keep looking for improvements to make.

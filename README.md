# Project Dylan

**Project Dylan** is a consolidated master recon and utility toolkit written in Python. It features async subdomain enumeration, live Minecraft server status pinging, CIDR-supported port sweeping, and Mojang player profile lookups.

---

## Features

1. **Advanced Minecraft & Subdomain Scanner**
   * Async DNS resolution supporting `A`, `AAAA`, and `SRV` records.
   * Multiple wordlist tiers, ranging from quick base lists to high-density permutation matrices.
   * **Live SLP Pinger**: Automatically pings discovered servers on port 25565 to check online status, player counts, and server versions.

2. **Port & Subnet Sweeper**
   * Multithreaded TCP socket port checks.
   * Full **CIDR subnet range support** (allowing you to scan entire local or remote network ranges like `192.168.1.0/24`).

3. **Mojang Player, UUID & Skin Tracker**
   * Resolves Minecraft usernames to unique Mojang UUIDs.
   * Decodes session server metadata to pull direct skin texture URLs.

---

## Requirements

* Python 3.x
* Optional: `dnspython` for enhanced asynchronous DNS lookup speeds. Install it via pip:
  ```bash
  pip install dnspython

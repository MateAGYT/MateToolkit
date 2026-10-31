<div align="center">

# Mate-Toolkit
# [Download Releases](https://github.com/MateAGYT/MateToolkit/releases)

**A 90-tool Windows toolkit wrapping essential CLIs inside a fast, dark, and animated PyQt6 graphical interface — media, networking, recon, web utilities, and data tools in a single window.**

![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)
![GUI](https://img.shields.io/badge/gui-PyQt6-41CD52?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Tools](https://img.shields.io/badge/tools-90-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)

> **`MateAGYT/MateToolkit` is the exclusive official repository.** Avoid downloading builds from unverified sources.

</div>

---

# 📑 Table of contents

- [1. About](#-about)
- [2. Disclaimer & License](#-disclaimer--license)
- [3. Features](#️-features)
  - [Media](#-media)
  - [Network](#-network)
  - [Recon](#-recon)
  - [Web](#-web)
  - [Data](#-data)
  - [Utilities](#-utilities)
- [4. Why Mate-Toolkit?](#-why-mate-toolkit)
- [5. Comparison](#-comparison)
- [6. Requirements](#-requirements)
- [7. Installation](#️-installation)
- [8. Troubleshooting & FAQ](#-troubleshooting--faq)
- [9. Roadmap](#-roadmap)
- [10. Credits](#-credits)
- [11. Contributing](#-contributing)

---

# 🧭 About

**Mate-Toolkit** consolidates 90 command-line utilities into a unified desktop application. Instead of managing complex flag combinations across dozens of separate binaries, you interact with clean forms featuring labeled inputs, dropdown selectors, file pickers, and inline `?` help guides that explain each option clearly before execution.

Every tool occupies a dedicated page within the left navigation panel, featuring a **GUIDE** tab, an environment check verifying binary availability, and a one-click **INSTALL** button that downloads and extracts portable builds into local `bin_<tool>` directories without modifying your system `PATH`.

Background tasks execute asynchronously on worker threads to keep the UI responsive, and pressing `Escape` terminates running processes immediately. Built-in pure-Python capabilities cover hashing, encoding, ciphers, regex, JWT inspection, diffing, data parsing, unit conversion, subnet math, and port probing. External binaries like nmap, ffmpeg, ffuf, nuclei, and 7-Zip are wrapped seamlessly.

---

# ❗ Disclaimer & License

**a) Disclaimer.** The software operates as a graphical frontend executing user-selected commands against designated targets. Ensure compliance with authorization protocols and legal regulations before scanning or testing networks.

**b) License.** MIT License. See [`LICENSE`](LICENSE) for details.

---

# ⚙️ Features

> 90 tools divided across six core functional categories.

## 🎥 Media

| Tool | Function |
|---|---|
| **yt-dlp** | Download media streams with preset formats and automatic ffmpeg integration. |
| **ffmpeg** | Transcode media, extract audio tracks, and generate GIFs. |
| **gallery-dl** | Bulk download image galleries from web links. |
| **ImageMagick** | Resize, convert, and strip metadata from images. |
| **MediaInfo** | Inspect container properties, codecs, and bitrates. |
| **ExifTool** | View or wipe file metadata and GPS coordinates. |
| **SoX** | Normalize and process audio files. |
| **MKVToolNix** | Remux containers and manage subtitle streams. |
| **7-Zip** | Handle archives and compressed formats. |
| **ASCII Art** | Render images as text graphics. |

## 🌐 Network

| Tool | Function |
|---|---|
| **nmap** | Execute scan profiles ranging from rapid checks to full TCP/UDP sweeps. |
| **DNS Lookup** | Query multiple record types via secure DNS-over-HTTPS providers. |
| **Zone Transfer** | Check name servers for AXFR configurations. |
| **Port Probe** | Conduct concurrent TCP connection sweeps. |
| **Subnet Calculator** | Compute network ranges, masks, and broadcast addresses. |
| **Ping / Traceroute** | Measure network latency and trace packet paths. |
| **Whois** | Retrieve domain registration details. |
| **Netcat** | Establish raw TCP connections and read service banners. |
| **Packet Capture** | Record network traffic using BPF filters. |
| **iperf3** | Benchmark network throughput speeds. |

## 🔍 Recon

| Tool | Function |
|---|---|
| **Subdomains** | Enumerate subdomains using certificate transparency logs. |
| **Site DNA** | Inspect technology stacks, headers, and page metrics. |
| **TLS Inspector** | Analyze certificate details and handshake validity. |
| **RDAP** | Perform modern registration and IP allocation lookups. |
| **IP Info** | Retrieve geolocation, ASN, and hosting data. |
| **Robots & Sitemap** | Parse crawl rules and published endpoint lists. |
| **WAF Detect** | Identify web application firewall signatures. |
| **WhatWeb** | Fingerprint web technologies at varying aggression levels. |
| **Nuclei** | Execute vulnerability scans using custom templates. |

## 🕸️ Web

| Tool | Function |
|---|---|
| **HTTP Headers** | Inspect response headers and security hardening posture. |
| **CORS Checker** | Test for insecure cross-origin resource sharing configurations. |
| **sqlmap** | Automate database injection testing. |
| **ffuf** | Perform high-speed directory and parameter fuzzing. |
| **URL Inspector** | Parse components, parameters, and redirect chains. |
| **Cookie Parser** | Decode values and check security attribute flags. |
| **Gobuster / Feroxbuster** | Discover hidden endpoints and virtual hosts. |
| **Nikto** | Scan web servers for known misconfigurations. |

## 📊 Data

| Tool | Function |
|---|---|
| **Hash Checker** | Verify file integrity against published cryptographic hashes. |
| **Hash ID** | Identify hash algorithms using structural heuristics. |
| **Encoder / Decoder** | Convert text across Base64, hex, URL, and binary formats. |
| **Ciphers** | Encrypt and decrypt text using classical ciphers. |
| **Base Converter** | Translate numbers across binary, octal, decimal, and hex bases. |
| **Text Tools** | Modify case, sort lines, strip duplicates, and analyze entropy. |
| **Diff Checker** | Compare text differences with whitespace tolerance. |
| **Regex Tester** | Evaluate regular expressions and inspect capture groups. |
| **JWT Decoder** | Inspect tokens, check expiration, and verify signatures. |

## 🧰 Utilities

| Tool | Function |
|---|---|
| **Passwords** | Generate secure credentials with customizable entropy metrics. |
| **Identifiers** | Produce UUIDs and secure random tokens. |
| **Timestamps** | Convert between Epoch time and ISO 8601 formats. |
| **Shredder** | Securely overwrite files using multi-pass deletion. |
| **Status Codes** | Reference HTTP response codes and practical descriptions. |
| **File Split** | Divide large files or merge split archive chunks. |
| **Batch Rename** | Modify filenames sequentially with preview support. |

---

# 🏆 Why Mate-Toolkit?

- **Unified Interface:** Access 90 tools from a single streamlined window.
- **Guided Inputs:** Inline help explanations eliminate the need to memorize complex CLI flags.
- **Portable Architecture:** Local tool folders keep your system clean without global environment clutter.
- **Reliable State Check:** Environment validations verify binary readiness prior to execution.
- **Robust Console Output:** Color-coded severity logging, asynchronous worker execution, and clean cancellation controls.

---

# 📊 Comparison

| Feature | Mate-Toolkit | DevToys | CyberChef | Raw CLI |
|---|---|---|---|---|
| Offline Support | **✅** | ✅ | ✅ | ✅ |
| Network & Recon Tools | **✅** | ❌ | 🟡 | ✅ |
| Media Processing | **✅** | 🟡 | ❌ | ✅ |
| In-App Options Guide | **✅** | 🟡 | ❌ | ❌ |
| One-Click Tool Setup | **✅** | ❌ | ❌ | ❌ |
| Cancellable Console | **✅** | ❌ | ❌ | ✅ |

---

# 📋 Requirements

- **Operating System:** Windows 10/11 (x64)
- **Runtime:** Python 3.10+ (with Python added to system PATH)
- **Disk Space:** ~400 MB minimum (additional space required for optional external tool downloads)

---

# 🛠️ Installation

1. Verify Python 3.10+ is installed with the PATH option enabled.
2. Clone or download the repository source files.
3. Install required Python packages:
   ```cmd
   py -m pip install PyQt6 requests

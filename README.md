<p align="center">
  <img src="https://raw.githubusercontent.com/ChatSamuel/SPS-SECURITY/main/assets/banner.png">
</p>

# SPS Security

**Multi-Engine Antivirus System — Open Source CLI**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen?style=for-the-badge)](https://github.com/ChatSamuel/SPS-SECURITY/releases)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Android%20%7C%20macOS-lightgrey?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

*A professional, modular, multi-engine malware detection tool built in Python.*  
*Comparable to VirusTotal + MetaDefender — but open source and terminal-native.*

[Features](#-features) •
[Architecture](#-architecture) •
[Installation](#-installation) •
[Usage](#-usage) •
[Engines](#-detection-engines) •
[Risk Levels](#-risk-levels) •
[Roadmap](#-roadmap) •
[Contributing](#-contributing)

</div>

---

## 📖 Overview

**SPS Security** is an open-source, terminal-native antivirus system designed for developers, security researchers, and power users who need real malware detection without commercial bloat.

It combines **local heuristic analysis**, **signature-based detection**, and **cloud-powered multi-engine scanning** (VirusTotal, MalwareBazaar, ThreatFox) into a single, unified CLI experience — with an interactive shell, real-time file monitoring, automatic quarantine, and intelligent weighted scoring.

Built to run anywhere Python runs: Linux, macOS, Android (Termux), and WSL.

> **"The goal is not to replace enterprise AV — it's to give every developer a real security tool they can understand, extend, and trust."**

---

## ✨ Features

### Core Detection
| Feature | Description |
|---|---|
| 🔍 **Heuristic Engine** | Detects suspicious patterns: `eval()`, `exec()`, `base64`, `subprocess`, PowerShell, bash reverse shells |
| 🗄️ **Signature Database** | Local SQLite-backed signature store — updated independently, works offline |
| ☁️ **Cloud Scan** | Parallel queries to VirusTotal, MalwareBazaar, and ThreatFox with weighted scoring |
| 🧵 **Multi-thread Scanner** | `ThreadPoolExecutor`-powered parallel scanning for directories |
| 👁️ **Real-time Monitor** | `watchdog`-powered file system observer — detects new/modified files instantly |

### Threat Management
| Feature | Description |
|---|---|
| 🔒 **Automatic Quarantine** | Suspicious files moved atomically to `quarantine/timestamp_filename` |
| 🧹 **Quarantine Cleanup** | Secure deletion of quarantined files on demand |
| 📋 **Logging System** | Structured log file at `logs/sps.log` with timestamp, risk, engine, and file path |
| 📊 **Intelligent Scoring** | Weighted aggregation of local + cloud results into a single confidence score |

### User Experience
| Feature | Description |
|---|---|
| 🖥️ **Interactive Shell** | Persistent `sps ›` prompt — banner shown once, commands loop until exit |
| 🎨 **Rich UI** | Color-coded panels, weight bars, engine tables, and progress spinners via `Rich` |
| 📱 **Android Support** | Fully functional in Termux on Android |
| 🚀 **Direct Mode** | Non-interactive: `sps cloud file.exe` for scripting and automation |

---

## 🏗️ Architecture

SPS Security is organized into four clean layers. Each layer has a single responsibility and communicates only through well-defined interfaces.

```
┌─────────────────────────────────────────────────┐
│                   CLI LAYER                     │
│          cli.py  ·  Interactive Shell           │
│    Direct commands  ·  Menu  ·  Banner          │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│                 ACTIONS LAYER                   │
│  cloud_action  ·  monitor_action                │
│  cleanup_action  ·  thread_scan_action          │
└──────┬───────────────────────────────┬──────────┘
       │                               │
┌──────▼──────────┐         ┌──────────▼──────────┐
│   LOCAL ENGINES │         │   CLOUD ENGINES     │
│  heuristic.py   │         │  virustotal.py      │
│  database.py    │         │  malwarebazaar.py   │
│  score.py       │         │  threatfox.py       │
│  threaded_scan  │         │  manager.py         │
└──────┬──────────┘         └──────────┬──────────┘
       │                               │
┌──────▼───────────────────────────────▼──────────┐
│                SUPPORT LAYER                    │
│  quarantine.py  ·  logger.py                   │
│  cache.py  ·  hasher.py  ·  config.py          │
└─────────────────────────────────────────────────┘
```

### Directory Structure

```
SPS-SECURITY/
│
├── sps_security/                  # Main package
│   │
│   ├── actions/                   # High-level command handlers
│   │   ├── __init__.py
│   │   ├── cloud_action.py        # Cloud scan orchestration
│   │   ├── monitor_action.py      # Real-time monitoring
│   │   ├── cleanup_action.py      # Quarantine cleanup
│   │   └── thread_scan_action.py  # Multi-thread directory scan
│   │
│   ├── cloud/                     # Cloud API integrations
│   │   ├── __init__.py
│   │   └── cloud_scanner.py       # Unified cloud scan entry point
│   │
│   ├── api/                       # API engine layer
│   │   ├── __init__.py
│   │   ├── base_api.py            # Abstract engine contract
│   │   ├── virustotal.py          # VirusTotal v3 engine (weight: 0.95)
│   │   ├── malwarebazaar.py       # MalwareBazaar engine (weight: 0.75)
│   │   ├── threatfox.py           # ThreatFox IOC engine (weight: 0.60)
│   │   └── manager.py             # Parallel orchestrator + score aggregator
│   │
│   ├── security/                  # Local security engines
│   │   ├── heuristic.py           # Pattern-based threat detection
│   │   ├── database.py            # Local signature database
│   │   ├── score.py               # Intelligent scoring system
│   │   ├── quarantine.py          # File quarantine system
│   │   ├── logger.py              # Structured logging
│   │   └── threaded_scan.py       # Multi-threaded scanner
│   │
│   ├── core/                      # Core utilities
│   │   ├── hasher.py              # File fingerprinting (SHA256/MD5/SHA1)
│   │   └── cache.py               # TTL-based result cache
│   │
│   ├── ui/                        # Terminal interface
│   │   ├── banner.py              # ASCII banner (shown once)
│   │   ├── shell.py               # Interactive shell loop + dispatcher
│   │   └── display.py             # Rich panels, tables, colors
│   │
│   ├── db/                        # Signature database files
│   │   └── signatures.txt         # Known threat signatures
│   │
│   ├── cli.py                     # Entry point + Click commands
│   └── config.py                  # Central configuration
│
├── quarantine/                    # Quarantined files (auto-created)
├── logs/                          # Log files (auto-created)
│   └── sps.log
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

---

## 🔧 Detection Engines

### Local Engines

#### Heuristic Engine
Scans file content for known-dangerous patterns without any network connection.

**Detected patterns:**
```
eval(              # Dynamic code execution
exec(              # Dynamic code execution
base64             # Encoded payload delivery
subprocess         # System process spawning
os.system(         # Shell command execution
powershell         # PowerShell invocation
cmd.exe            # Windows shell invocation
bash -i            # Bash reverse shell
/bin/sh            # Unix shell invocation
wget http          # Remote download
curl http          # Remote download
nc -e              # Netcat reverse shell
```

#### Signature Database Engine
Matches file content against a local database of known malware signatures.

**Database location:** `sps_security/db/signatures.txt`

**Built-in signatures:**
```
trojan
malware
backdoor
keylogger
ransomware
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
```

### Cloud Engines

| Engine | Weight | Type | API Key Required |
|---|---|---|---|
| **VirusTotal** | `0.95` (highest) | 70+ sub-engine aggregator | ✅ Yes (free tier available) |
| **MalwareBazaar** | `0.75` (medium) | Confirmed malware sample DB | ❌ No |
| **ThreatFox** | `0.60` (lower) | Community IOC database | ❌ No |

**How weights work:**

Each engine contributes to the final score according to:
```
engine_contribution = weight × detection_ratio × confidence
final_score = sum(contributions) / sum(weights)
```

This means VirusTotal (with 70+ internal scanners and weight 0.95) has far more influence on the verdict than a single community IOC report from ThreatFox.

---

## 🚦 Risk Levels

| Level | Color | Score Range | Meaning |
|---|---|---|---|
| 🟢 **SAFE** | Green | 0.0 – 5% | No threats detected |
| 🟡 **LOW** | Yellow | 5% – 25% | Suspicious — possible false positive |
| 🟠 **MEDIUM** | Orange | 25% – 50% | Likely threat — review recommended |
| 🔴 **HIGH** | Red | 50% – 75% | High confidence threat |
| 💀 **CRITICAL** | Bold Red | 75% – 100% | Confirmed threat — quarantine immediately |

### Anti-False-Positive System
If only **one low-weight engine** detects a threat (and the score is below 25%), the system applies a **40% dampening factor** to prevent false alarms. Escalation to HIGH or CRITICAL requires **at least 2 engines to agree**.

---

## 🔒 Quarantine System

When a file is classified as HIGH or above, SPS Security automatically:

1. Moves the file to the `quarantine/` directory
2. Renames it with a timestamp prefix: `20260321_143022_filename.exe`
3. Logs the quarantine event with full metadata
4. Reports the quarantine path in the UI

**To review quarantined files:**
```bash
ls quarantine/
```

**To clean up quarantine (secure deletion):**
```bash
sps
# then: cleanup
# or directly:
sps cache --clear
```

> ⚠️ Files in quarantine are **not deleted automatically**. Manual cleanup is required.

---

## 📋 Logging

All scan events are logged to `logs/sps.log`.

**Log format:**
```
2026-03-21 09:06:44 | CRITICAL | VirusTotal    | /sdcard/Downloads/trojan.txt
2026-03-21 09:06:44 | CRITICAL | MalwareBazaar | /sdcard/Downloads/trojan.txt
2026-03-21 09:06:44 | QUARANTINE | auto        | quarantine/20260321_090644_trojan.txt
```

**To view live logs:**
```bash
tail -f logs/sps.log
```

---

## 📦 Installation

### Requirements

- Python 3.8 or higher
- pip
- Internet connection (for cloud scan features)
- VirusTotal API key (free at [virustotal.com](https://www.virustotal.com))

### Install from source

```bash
# 1. Clone the repository
git clone https://github.com/ChatSamuel/SPS-SECURITY.git
cd SPS-SECURITY

# 2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Linux / macOS / Termux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package
pip install -e .

# 5. Set your VirusTotal API key
export VT_API_KEY="your_api_key_here"

# 6. Run SPS Security
sps
```

### Install on Android (Termux)

```bash
# Install Python and git in Termux
pkg update && pkg install python git -y

# Clone and install
git clone https://github.com/ChatSamuel/SPS-SECURITY.git
cd SPS-SECURITY
pip install -e .

# Set API key
export VT_API_KEY="your_api_key_here"

# Run
sps
```

### Quick test (no API key needed)

```bash
# Test with EICAR standard test file
echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.txt
sps cloud eicar.txt
```

---

## 🚀 Usage

### Interactive Mode (recommended)

```bash
sps
```

The banner appears once. The shell opens and waits for commands:

```
sps › cloud malware.exe
sps › scan /sdcard/Downloads
sps › monitor /sdcard
sps › cleanup
sps › help
sps › exit
```

### Direct Mode (for scripting)

```bash
# Cloud scan a file
sps cloud suspicious.exe

# Cloud scan bypassing cache
sps cloud suspicious.exe --no-cache

# Local scan (file or directory)
sps scan /path/to/directory

# Deep scan
sps scan /path/to/file --deep

# Real-time monitoring
sps monitor /sdcard/Downloads

# APK analysis
sps apk app.apk

# Cache management
sps cache --stats
sps cache --clear
```

### Full Command Reference

```
sps [OPTIONS] COMMAND [ARGS]

Options:
  --version   Show version and exit.
  -h, --help  Show help message and exit.

Commands:
  cloud    Run a multi-engine cloud scan on a file
  scan     Run a local multi-engine scan on a file or directory
  apk      Analyze an Android APK file for threats
  monitor  Start real-time file system monitoring
  cache    Manage the local scan result cache
```

### Example Output — Cloud Scan

```
╔══════════════════════════════════════════════════════╗
║              SCAN RESULT  eicar.txt                  ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  💀  CRITICAL                                        ║
║                                                      ║
║  Score         81.3%  |  Confidence    87%           ║
║  Detections    2/3 engines                           ║
║  Family        EICAR-Test-File                       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

Engine Breakdown
┌──────────────────┬────────────┬─────────────┬────────────┬───────────┬──────────────────┐
│ Engine           │ Weight     │ Result      │ Detections │ Confidence│ Family           │
├──────────────────┼────────────┼─────────────┼────────────┼───────────┼──────────────────┤
│ VirusTotal       │ ████████ 95%│ ✗ DETECTED  │ 63/77      │ 90%       │ EICAR-Test-File  │
│ MalwareBazaar    │ ██████░░ 75%│ ✗ DETECTED  │ 1/1        │ 90%       │ EICAR            │
│ ThreatFox        │ █████░░░ 60%│ ✓ CLEAN     │ 0/0        │ 40%       │ —                │
└──────────────────┴────────────┴─────────────┴────────────┴───────────┴──────────────────┘

  Completed in 1842 ms
```

---

## ⚙️ Configuration

All settings are controlled via environment variables or `sps_security/config.py`.

| Variable | Default | Description |
|---|---|---|
| `VT_API_KEY` | *(required)* | VirusTotal API key |
| `MB_API_KEY` | *(optional)* | MalwareBazaar key (free without) |
| `TF_API_KEY` | *(optional)* | ThreatFox key (free without) |
| `SPS_CACHE_PATH` | `.sps_cache.json` | Cache file path |
| `SPS_CACHE_TTL_HOURS` | `24` | How long cache entries stay valid |
| `SPS_API_TIMEOUT` | `15` | API request timeout in seconds |
| `SPS_MAX_WORKERS` | `6` | Parallel thread pool size |
| `SPS_WEIGHT_VT` | `0.95` | VirusTotal engine weight |
| `SPS_WEIGHT_MB` | `0.75` | MalwareBazaar engine weight |
| `SPS_WEIGHT_TF` | `0.60` | ThreatFox engine weight |

---

## 🗺️ Roadmap

### v2.0 (Current — March 2026)
- [x] Multi-engine cloud scanning (VirusTotal + MalwareBazaar + ThreatFox)
- [x] Weighted scoring system with anti-false-positive logic
- [x] Real-time file monitoring (watchdog)
- [x] Interactive terminal shell (banner shown once)
- [x] Automatic quarantine system
- [x] Structured logging
- [x] Multi-threaded directory scanning
- [x] TTL-based result cache
- [x] APK analysis (Phase 1: hash-based cloud scan)
- [x] Android/Termux support

### v2.1 (Planned — Q2 2026)
- [ ] YARA rule support for local scanning
- [ ] APK static analysis (Phase 2: manifest + permissions)
- [ ] PDF malicious content detection
- [ ] Office document macro scanner
- [ ] Configurable YAML-based rule system
- [ ] Automatic signature database updates

### v3.0 (Planned — Q3 2026)
- [ ] FastAPI REST server (`sps serve`)
- [ ] Web dashboard (React)
- [ ] Multi-file drag-and-drop upload
- [ ] API key management UI
- [ ] Docker image (`docker run sps-security`)
- [ ] Plugin system for custom engines

### Future / SaaS
- [ ] Cloud-hosted scanning service
- [ ] Team API with rate limiting
- [ ] Enterprise webhook integration
- [ ] Billing and subscription management

---

## 🤝 Contributing

Contributions are welcome and appreciated. SPS Security is built with extensibility in mind — adding a new engine takes less than 50 lines of code.

### How to add a new cloud engine

1. Create `sps_security/api/myengine.py`
2. Inherit from `BaseAPI`
3. Implement `analyze(file_hash, file_path) -> EngineResult`
4. Register it in `actions/cloud_action.py`

```python
# sps_security/api/myengine.py
from .base_api import BaseAPI, EngineResult

class MyEngine(BaseAPI):
    NAME         = "myengine"
    DISPLAY_NAME = "My Engine"
    WEIGHT       = 0.70

    def analyze(self, file_hash: str, file_path=None) -> EngineResult:
        # ... query your API ...
        return EngineResult(
            engine_name=self.DISPLAY_NAME,
            weight=self.WEIGHT,
            detected=True,
            confidence=0.85,
            raw_detections=1,
            total_scanners=1,
        )
```

### Development setup

```bash
git clone https://github.com/ChatSamuel/SPS-SECURITY.git
cd SPS-SECURITY
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Pull Request guidelines

- Fork the repository
- Create a feature branch: `git checkout -b feature/my-new-engine`
- Write clear commit messages in English
- Add a test file if adding a new engine
- Open a PR with a description of what you changed and why

### Code style

- Python 3.8+ compatible
- PEP 8 formatting
- Type hints on all public functions
- English-only comments and docstrings

---

## 🔐 Security

### Reporting vulnerabilities

If you discover a security vulnerability in SPS Security, **please do not open a public issue**.

Instead, report it privately by emailing the author or opening a [GitHub Security Advisory](https://github.com/ChatSamuel/SPS-SECURITY/security/advisories/new).

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### API key safety

- **Never commit API keys** to the repository
- Always use environment variables: `export VT_API_KEY=...`
- The `.gitignore` in this repo excludes `.env` files automatically

### Disclaimer

> SPS Security is provided for **educational and research purposes only**.  
> The authors are not responsible for misuse of this tool.  
> Always scan files you have legal permission to analyze.  
> Using this tool against systems you do not own may be illegal.

---

## 📊 Performance

| Operation | Typical Time |
|---|---|
| Local heuristic scan (1 file) | < 50 ms |
| Cloud scan — cache hit | < 10 ms |
| Cloud scan — 3 engines parallel | 1,500 – 4,000 ms |
| Directory scan (100 files, 6 threads) | ~ 5 seconds |
| Real-time monitor startup | < 200 ms |

---

## 🧪 Testing

```bash
# Create EICAR test file (safe test — not real malware)
echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.txt

# Test local heuristic
echo 'import subprocess; subprocess.call(["bash", "-i"])' > heuristic_test.py

# Test cloud scan
sps cloud eicar.txt

# Test real-time monitor (open a second terminal and create a file)
sps monitor .
# In another terminal: echo "trojan" > test_threat.txt
```

---

## 📝 Changelog

### v2.0.0 — March 2026
- **NEW** Interactive terminal shell (`sps` with no args)
- **NEW** Banner shown once at startup — not on every command
- **NEW** MalwareBazaar engine (free, no API key)
- **NEW** ThreatFox IOC engine (free, no API key)
- **NEW** Weighted multi-engine scoring
- **NEW** Anti-false-positive dampening system
- **NEW** Global confidence metric
- **NEW** TTL-based result cache with versioning
- **NEW** Single-pass file hashing (SHA256 + MD5 + SHA1)
- **NEW** APK scan support (Phase 1)
- **IMPROVED** Engine breakdown table with weight bars
- **IMPROVED** CLI organized into actions layer
- **IMPROVED** All UI labels standardized to English
- **FIXED** Banner no longer appears on every command call

### v1.0.0 — Initial Release
- Basic CLI with VirusTotal integration
- Local heuristic engine
- Signature database
- Quarantine system
- Real-time monitor
- Multi-thread scanner

---

## 👤 Author

**Samuel Pontes**

- GitHub: [@ChatSamuel](https://github.com/ChatSamuel)
- Project: [SPS-SECURITY](https://github.com/ChatSamuel/SPS-SECURITY)

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.

```
MIT License — Copyright (c) 2026 Samuel Pontes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

## ⚠️ Disclaimer

SPS Security is an **open-source educational tool** for malware research and system security.

- Do **not** use this tool to scan systems you do not own or have explicit permission to test
- The detection results are **informational only** — do not rely solely on SPS Security for production security decisions
- Cloud scan results depend on third-party APIs (VirusTotal, MalwareBazaar, ThreatFox) — their accuracy and availability are outside the control of this project
- The authors assume **no liability** for damages caused by the use or misuse of this software

---

<div align="center">

Made with ❤️ by [Samuel Pontes](https://github.com/ChatSamuel)

⭐ Star this project if it helped you — it motivates continued development!

</div>


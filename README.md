# Simple-SSH-Login-Scanner 🛡️ ![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
Simple SSH Login Scanner is a Python script that monitors failed SSH login attempts from system logs (auth.log or journalctl), displaying details like username, IP address, and timestamp to help detect unauthorized access attempts or brute-force attacks.

## Features ✨
- 🔍 Scans **auth.log** or **journalctl** logs for failed SSH login attempts.
- 👤 Displays the **username**, **IP address** *(with IPv4/IPv6 identification)*, and **timestamp** for **each failed attempt**.
- ⏱️ Option to **read only** the **last 100 log entries** *(or specify a **custom number**)*.
- 🌐 Can scan the **entire** *journalctl* log with a **simple flag** *(`--all`)*.
- 🎨 Easy-to-read terminal output with **colored status messages** for **better visibility**.

## Installation ⚙️
1. Clone the repository or download the `ssh-login-scanner.py` file:
2. Ensure you have **Python 3** installed.
3. Make sure to have **root privileges** for reading log files *(auth.log / journalctl)*.

## Usage 🚀
Run the script using the following command:
```
python3 simple_ssh_login_scanner.py
```
*(This will read the **last 500 entries** in your log file and print the **last 100 failed logins**.)*
### Optional flags 🚩
`--limit <number>`: Show the last ***'number'*** of failed login attempts (default: 100).

`--all`: Read the **entire** *journalctl* log. *This might take some time depending on your log file size.*
### Example Output 💻
```
[*] Attempting to read auth.log...
**************************************************
[!] Failed login detected in auth.log file:
-> Username: root
-> IP Address: 192.168.1.1 (IPv4)
-> Timestamp: Apr 18 13:45:22
--------------------------------------------------
[*] Script finished in 0.12 seconds.
--------------------------------------------------
```
# Script Flow 🔄
1. **Log Check:** The script first attempts to read ***auth.log***. If it’s unavailable *(e.g., permissions)*, it falls back to ***journalctl***.
2. **Pattern Matching:** It uses **regex** to extract **usernames** and **IP addresses** from **failed login attempts**.
3. **IP Type Identification:** It distinguishes between **IPv4**, **IPv6**, and **invalid IP addresses**.
4. **Timestamp:** Displays the **exact time** of **each failed attempt** for auditing purposes.

# Example Usage 📄
In this scenario, the script would **read the last *500* entries** in the log file and **output the last *50* failed login attempts**:
```
python3 simple_ssh_login_scanner.py --limit 50
```
In this scenario the script would **read *every* entry** in the log file and **output the last *500* failed login attempts**.
```
python3 simple_ssh_login_scanner.py --limit 500 --all
```
# Requirements ⚡
- Python 3
- Root privileges for reading system log files *(auth.log / journalctl)*.

# License 📜
This project is licensed under the MIT License - see the LICENSE file for details.

# Contributing 🤝
Feel free to **fork** the repo, create an **issue**, or submit a **pull request** for any **improvements** or **bug fixes**!

# Python Port Scanner 

A lightweight TCP port scanner built from scratch in Python to practice network security fundamentals and socket programming.

## What It Does

This tool scans a target IP address or hostname across a specified port range and reports which ports are open, along with the commonly associated service (e.g. SSH, HTTP, FTP).

## Why I Built This

As part of my cybersecurity journey, I wanted to understand how tools like Nmap work under the hood rather than just using them as a black box. Building this scanner taught me:

- How TCP connections work at the socket level
- The three-way handshake and connection states
- How to map open ports to likely running services
- Practical Python scripting for security tooling

## How to Use

```bash
# Basic scan (default range 1-1024)
python3 port_scanner.py 192.168.1.1

# Scan a specific port range
python3 port_scanner.py 192.168.1.1 -p 1-500

# Scan with a custom timeout
python3 port_scanner.py scanme.nmap.org -p 1-100 -t 0.5
```

## Important: Legal & Ethical Use

Only scan systems you own or have explicit permission to test. This tool was built strictly for educational purposes within my own home lab.

## Tech Used

- Python 3
- `socket` library (standard library, no external dependencies)
- `argparse` for command-line interface

## What I'd Add Next

- Multithreading to speed up large port range scans
- Banner grabbing to identify service versions
- Output saved to a file (JSON/CSV)

## About Me

Cybersecurity student at Birmingham City University.
GitHub: [prosper-anele](https://github.com/prosper-anele)
LinkedIn: [Prosper Anele](https://linkedin.com/in/prosper-anele)

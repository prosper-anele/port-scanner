#!/usr/bin/env python3
"""
Simple TCP Port Scanner
Author: Prosper Anele
Description: A lightweight port scanner built to practice networking
             fundamentals and socket programming in Python.
"""

import socket
import sys
import argparse
from datetime import datetime

# Common ports and their typical services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy",
}


def scan_port(target: str, port: int, timeout: float = 1.0) -> bool:
    """Attempt to connect to a single TCP port. Returns True if open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            return result == 0
    except socket.error:
        return False


def scan_range(target: str, start_port: int, end_port: int, timeout: float = 1.0):
    """Scan a range of ports on the target and report open ones."""
    print(f"\nScanning target: {target}")
    print(f"Port range: {start_port}-{end_port}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("-" * 50)

    open_ports = []

    try:
        for port in range(start_port, end_port + 1):
            if scan_port(target, port, timeout):
                service = COMMON_PORTS.get(port, "Unknown")
                print(f"Port {port:<6} OPEN    ({service})")
                open_ports.append(port)
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)

    print("-" * 50)
    print(f"\nScan complete. {len(open_ports)} open port(s) found.")
    if open_ports:
        print(f"Open ports: {open_ports}")
    return open_ports


def resolve_target(target: str) -> str:
    """Resolve a hostname to an IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: Could not resolve hostname '{target}'")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="A simple TCP port scanner for learning network security fundamentals."
    )
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument(
        "-p", "--ports", default="1-1024",
        help="Port range to scan, e.g. 1-1024 (default: 1-1024)"
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=1.0,
        help="Timeout in seconds per port (default: 1.0)"
    )

    args = parser.parse_args()

    try:
        start_port, end_port = map(int, args.ports.split("-"))
    except ValueError:
        print("Error: Port range must be in the format start-end, e.g. 1-1024")
        sys.exit(1)

    ip = resolve_target(args.target)
    scan_range(ip, start_port, end_port, args.timeout)


if __name__ == "__main__":
    main()

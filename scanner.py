import socket
import sys
from datetime import datetime


def grab_banner(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        sock.connect((target, port))

        request = f"HEAD / HTTP/1.0\r\nHost: {target}\r\n\r\n"
        sock.send(request.encode())

        banner = sock.recv(1024).decode(errors="ignore")

        sock.close()

        return banner.strip()

    except (socket.timeout, ConnectionRefusedError, OSError):
        return None


def get_service(port):
    try:
        service = socket.getservbyport(port, "tcp")
        return service.upper()

    except OSError:
        return "UNKNOWN"


def assess_risk(port, service):
    if port in [21, 23, 3389]:
        return "HIGH"

    if port in [22, 25, 53, 80, 443, 8080, 8443]:
        return "MEDIUM"

    return "LOW"


def scan_ports(target, start_port, end_port):

    print()
    print("=" * 45)
    print("        PYTHON PORT SCANNER")
    print("=" * 45)
    print(f"Target: {target}")
    print(f"Ports:  {start_port}-{end_port}")
    print("=" * 45)
    print()

    open_ports = []
    report_lines = []

    report_lines.append("PORT SCAN REPORT")
    report_lines.append("================")
    report_lines.append(f"Target: {target}")
    report_lines.append(f"Port range: {start_port}-{end_port}")
    report_lines.append(
        f"Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    report_lines.append("")

    for port in range(start_port, end_port + 1):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:

            service = get_service(port)
            risk = assess_risk(port, service)

            print(f"[+] Port {port} is OPEN")
            print(f"    Service: {service}")

            banner = grab_banner(target, port)

            protocol = "Unknown"
            technology = "Unknown"

            if banner:

                first_line = banner.splitlines()[0]

                print(f"    Banner: {first_line}")

                if first_line.startswith("HTTP/"):
                    protocol = "HTTP"
                    print("    Protocol: HTTP")

                if "X-Powered-By: Next.js" in banner:
                    technology = "Next.js"
                    print("    Technology: Next.js")

            print(f"    Risk: {risk}")
            print()

            report_lines.append(f"Port: {port}")
            report_lines.append("Status: OPEN")
            report_lines.append(f"Service: {service}")
            report_lines.append(f"Protocol: {protocol}")
            report_lines.append(f"Technology: {technology}")
            report_lines.append(f"Risk: {risk}")

            if banner:
                report_lines.append(
                    f"Banner: {banner.splitlines()[0]}"
                )

            report_lines.append("")
            report_lines.append("----------------")
            report_lines.append("")

            open_ports.append(port)

        else:
            print(f"[-] Port {port} is closed")

        sock.close()

    print()
    print("Scan complete.")

    if open_ports:
        print(f"Open ports found: {len(open_ports)}")
    else:
        print("No open ports found.")

    report_lines.append("SCAN SUMMARY")
    report_lines.append("============")
    report_lines.append(
        f"Open ports found: {len(open_ports)}"
    )

    if open_ports:
        report_lines.append(
            f"Open ports: {', '.join(map(str, open_ports))}"
        )
    else:
        report_lines.append("Open ports: None")

    with open("scan_report.txt", "w") as report_file:
        report_file.write("\n".join(report_lines))

    print("Report saved to: scan_report.txt")


def show_usage():
    print()
    print("Python Port Scanner")
    print()
    print("Usage:")
    print(
        "python3 scanner.py "
        "--target <IP> --start <PORT> --end <PORT>"
    )
    print()
    print("Example:")
    print(
        "python3 scanner.py "
        "--target 127.0.0.1 --start 2998 --end 3002"
    )
    print()


def get_argument(name):
    if name in sys.argv:
        index = sys.argv.index(name)

        if index + 1 < len(sys.argv):
            return sys.argv[index + 1]

    return None


# Check arguments

if "--help" in sys.argv or "-h" in sys.argv:
    show_usage()
    sys.exit(0)


target = get_argument("--target")
start_value = get_argument("--start")
end_value = get_argument("--end")


if target is None or start_value is None or end_value is None:
    print("Error: Missing required arguments.")
    show_usage()
    sys.exit(1)


# Convert ports to integers

try:
    start_port = int(start_value)
    end_port = int(end_value)

except ValueError:
    print("Error: Ports must be numbers.")
    sys.exit(1)


# Validate ports

if not 1 <= start_port <= 65535:
    print("Error: Start port must be between 1 and 65535.")
    sys.exit(1)


if not 1 <= end_port <= 65535:
    print("Error: End port must be between 1 and 65535.")
    sys.exit(1)


if start_port > end_port:
    print("Error: Start port cannot be greater than end port.")
    sys.exit(1)


# Start scanner

scan_ports(target, start_port, end_port)
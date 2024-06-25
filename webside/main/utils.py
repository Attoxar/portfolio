import socket
import concurrent.futures
import requests
from urllib.parse import urljoin
import time
from scapy.all import *
import nmap

SQL_INJECTION_PAYLOADS = ("'", "' OR 1=1 --", '" OR 1=1 --', "' OR 'a'='a'")
CROSS_SITE_SCRIPT = ("<script>alert(1)</script>", "<img src=x onerror=alert(1)>")
LOCAL_FILE_INJECTION = ("../../../../etc/passwd", "../../../../windows/win.ini")
SENSITIVE_FILES = (".git", ".env", "config.php", "backup.zip", "backup.sql")


def port_scanning(target):
    print(f"Scanning ports on {target}...")
    open_ports = []
    ports = range(1, 8444)  # Adjusted the port range

    def scan_port(target, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target, port))
                if result == 0:
                    return port
        except Exception as e:
            print(f"Error scanning port {port}: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {
            executor.submit(scan_port, target, port): port for port in ports
        }
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                if result:
                    open_ports.append(result)
            except Exception as e:
                print(f"Error retrieving result for port {port}: {e}")

    return open_ports


def website_vulnerabilities(target):
    print(f"Performing web vulnerability scan on {target}...")
    vulnerabilities = []
    try:
        response = requests.get(target)
        if response.status_code == 200:
            print("Target website is accessible")
            headers = response.headers

            security_headers = {
                "Content-Security-Policy": "Content Security Policy (CSP)",
                "X-Content-Type-Options": "X-Content-Type-Options",
                "X-Frame-Options": "X-Frame-Options",
                "X-XSS-Protection": "X-XSS-Protection",
                "Strict-Transport-Security": "Strict Transport Security (HSTS)",
                "Referrer-Policy": "Referrer Policy",
                "Permissions-Policy": "Permissions Policy",
            }

            for header, description in security_headers.items():
                if header in headers:
                    vulnerabilities.append(
                        f"[+] {description} is set: {headers[header]}"
                    )
                else:
                    vulnerabilities.append(f"[-] {description} is missing")

            for payload in SQL_INJECTION_PAYLOADS:
                test_url = f"{target}?id={payload}"
                test_response = requests.get(test_url)
                if (
                    "syntax error" in test_response.text.lower()
                    or "mysql" in test_response.text.lower()
                ):
                    vulnerabilities.append(
                        f"[!] Possible SQL Injection vulnerability detected with payload: {payload}"
                    )

            for payload in CROSS_SITE_SCRIPT:
                test_url = f"{target}?q={payload}"
                test_response = requests.get(test_url)
                if payload in test_response.text:
                    vulnerabilities.append(
                        f"[!] Possible XSS vulnerability detected with payload: {payload}"
                    )

            for payload in LOCAL_FILE_INJECTION:
                test_url = f"{target}?file={payload}"
                test_response = requests.get(test_url)
                if (
                    "root:x:" in test_response.text
                    or "windows" in test_response.text.lower()
                ):
                    vulnerabilities.append(
                        f"[!] Possible Directory Traversal vulnerability detected with payload: {payload}"
                    )

            for sensitive_file in SENSITIVE_FILES:
                test_url = urljoin(target, sensitive_file)
                test_response = requests.get(test_url)
                if test_response.status_code == 200:
                    vulnerabilities.append(
                        f"[!] Sensitive file found: {sensitive_file}"
                    )

            test_url = f"{target}?next=http://example.com"
            test_response = requests.get(test_url, allow_redirects=False)
            if test_response.status_code in [
                301,
                302,
            ] and "example.com" in test_response.headers.get("Location", ""):
                vulnerabilities.append(
                    f"[!] Possible open redirect vulnerability detected"
                )

            if "X-Powered-By" in headers:
                vulnerabilities.append(
                    f"[!] X-Powered-By header is present: {headers['X-Powered-By']} (may disclose server technology)"
                )

            if "Server" in headers:
                vulnerabilities.append(
                    f"[!] Server header is present: {headers['Server']} (may disclose server version)"
                )

        else:
            vulnerabilities.append("Failed to access target website")
    except requests.exceptions.RequestException as e:
        vulnerabilities.append(f"Error: {e}")

    return vulnerabilities


def looking_up_dns(target):
    print(f"Performing DNS lookup for {target}...")
    try:
        ip_address = socket.gethostbyname(target)
        return ip_address
    except socket.gaierror:
        return "Hostname could not be resolved"


def traceroute_view(target):
    print(f"Tracerouting to {target}...")
    hops = []
    try:
        max_hops = 30
        target_ip = socket.gethostbyname(target)

        for ttl in range(1, max_hops + 1):
            packet = IP(dst=target_ip, ttl=ttl) / ICMP()
            start_time = time.time()
            reply = sr1(packet, verbose=False, timeout=1)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000

            if reply is None:
                hops.append(f"{ttl}: * Timeout")
            else:
                hop_ip = reply.src
                try:
                    response = requests.get(f"http://ipinfo.io/{hop_ip}/json")
                    data = response.json()
                    loc = data.get("loc", None)
                    if loc:
                        latitude, longitude = loc.split(",")
                        hops.append(
                            f"{ttl}: {hop_ip} ({rtt:.2f} ms) - Latitude: {latitude}, Longitude: {longitude}"
                        )
                    else:
                        hops.append(
                            f"{ttl}: {hop_ip} ({rtt:.2f} ms) - GPS Coordinates: Not available"
                        )
                except requests.RequestException as e:
                    hops.append(
                        f"{ttl}: {hop_ip} ({rtt:.2f} ms) - Error retrieving geolocation data: {e}"
                    )

                if reply.type == 0:
                    break

        return hops
    except socket.gaierror:
        return [
            f"Failed to resolve hostname '{target}'. Please provide a valid target."
        ]
    except Exception as e:
        return [f"Error performing traceroute: {e}"]


def os_detection(target):
    print(f"Detecting operating system of {target}...")
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments="-O")
        os_guess = nm[target]["osmatch"][0]["name"]
        return os_guess
    except Exception as e:
        return f"Error: {e}"

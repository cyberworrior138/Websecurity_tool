#!/usr/bin/env python3
# ==================================================
# MR.VIRUS TOOLKIT
# Web Information & Security Learning Tool
# Author: Mr.Virus (TZ)
# Purpose: Educational & Ethical Use Only
# ==================================================

import socket
import ssl
import requests
import sys
import time
import threading

# ===================== COLORS =====================
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ===================== LOADING ANIMATION =====================
loading = False

def spinner(text="Scanning"):
    symbols = ["|", "/", "-", "\\"]
    i = 0
    while loading:
        print(f"\r{CYAN}{text} {symbols[i % len(symbols)]}{RESET}", end="")
        time.sleep(0.1)
        i += 1
    print("\r", end="")

def start_loading(text):
    global loading
    loading = True
    t = threading.Thread(target=spinner, args=(text,))
    t.start()
    return t

def stop_loading():
    global loading
    loading = False
    time.sleep(0.2)

# ===================== BANNER =====================
def show_banner():
    print(GREEN + """
███████╗██╗   ██╗██╗██████╗ ██╗   ██╗███████╗
██╔════╝██║   ██║██║██╔══██╗██║   ██║██╔════╝
█████╗  ██║   ██║██║██████╔╝██║   ██║███████╗
██╔══╝  ██║   ██║██║██╔══██╗██║   ██║╚════██║
██║     ╚██████╔╝██║██║  ██║╚██████╔╝███████║
╚═╝      ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

        MR.VIRUS HACKER - TZ
        Web Information Tool
--------------------------------------------------
Educational tool only. Use responsibly.
Instagram: @uknown_virus404x
--------------------------------------------------
""" + RESET)

# ===================== FUNCTIONS =====================
def get_ip(domain):
    try:
        return GREEN + socket.gethostbyname(domain) + RESET
    except:
        return RED + "IP not found" + RESET

def http_headers(url):
    try:
        r = requests.get(url, timeout=5, allow_redirects=False)
        return r.status_code, r.headers
    except:
        return None, None

def ssl_info(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                return ssock.getpeercert()
    except:
        return None

# ===================== AUTO PORT SCAN =====================
def scan_ports(domain):
    common_ports = {
        21: "FTP",
        22: "SSH",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        8080: "HTTP-ALT"
    }

    open_ports = []

    for port, service in common_ports.items():
        try:
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((domain, port))
            if result == 0:
                open_ports.append((port, service))
            sock.close()
        except:
            pass

    return open_ports

# ===================== MENU =====================
def menu():
    print(CYAN + """
[1] Get IP Address
[2] HTTP Headers (Port 80)
[3] HTTPS Headers (Port 443)
[4] SSL Certificate Info
[5] Auto Detect Open Ports
[6] Full Scan (All)
[0] Exit
""" + RESET)

# ===================== MAIN =====================
def main():
    show_banner()
    site = input(YELLOW + "Enter website (example: google.com): " + RESET).strip()
    domain = site.replace("https://", "").replace("http://", "").split("/")[0]

    while True:
        menu()
        choice = input(BLUE + "Select option: " + RESET).strip()

        if choice == "1":
            print(GREEN + "\n[+] IP Address:" + RESET, get_ip(domain))

        elif choice == "2":
            print(YELLOW + "\n[+] HTTP Headers (Port 80)" + RESET)
            status, headers = http_headers(f"http://{domain}")
            if status:
                print(GREEN + "Status:" + RESET, status)
                for h in headers:
                    print(CYAN + f"{h}:" + RESET, headers[h])
            else:
                print(RED + "HTTP not responding" + RESET)

        elif choice == "3":
            print(YELLOW + "\n[+] HTTPS Headers (Port 443)" + RESET)
            status, headers = http_headers(f"https://{domain}")
            if status:
                print(GREEN + "Status:" + RESET, status)
                for h in headers:
                    print(CYAN + f"{h}:" + RESET, headers[h])
            else:
                print(RED + "HTTPS not responding" + RESET)

        elif choice == "4":
            print(YELLOW + "\n[+] SSL Certificate Info" + RESET)
            cert = ssl_info(domain)
            if cert:
                print(GREEN + "Issuer:" + RESET, cert.get("issuer"))
                print(GREEN + "Valid Until:" + RESET, cert.get("notAfter"))
            else:
                print(RED + "SSL info not available" + RESET)

        elif choice == "5":
            start_loading("Scanning open ports")
            ports = scan_ports(domain)
            stop_loading()

            print(GREEN + "\n[+] Open Ports Found:" + RESET)
            if ports:
                for p, s in ports:
                    print(GREEN + f"Port {p} OPEN" + RESET, f"({s})")
            else:
                print(RED + "No open common ports detected" + RESET)

        elif choice == "6":
            start_loading("Running full scan")
            ip = get_ip(domain)
            ports = scan_ports(domain)
            stop_loading()

            print(GREEN + "\n[+] IP Address:" + RESET, ip)
            print(GREEN + "\n[+] Open Ports:" + RESET)
            for p, s in ports:
                print(GREEN + f"Port {p} OPEN" + RESET, f"({s})")

        elif choice == "0":
            print(RED + "Exiting... Stay safe 😎" + RESET)
            sys.exit()

        else:
            print(RED + "Invalid option!" + RESET)

if __name__ == "__main__":
    main()

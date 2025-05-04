#!/usr/bin/env python3
from scapy.all import IP, TCP, sr1
import argparse
import sys
import socket

## colors ##
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
reset = "\033[0m"
bold = "\033[1m"
## colors ##

## banner ##
script_banner = r"""
  )\.--.     )\.-.     /`-.  .'(     /`-.  .-,.-.,-.         /`-.  )\    /(
 (   ._.'  ,' ,-,_)  ,' _  \ \  )  ,' _  \ ) ,, ,. (       ,' _  \ \ (_.' /
  `-.`.   (  .   _  (  '-' ( ) (  (  '-' ( \( |(  )/      (  '-' (  )  _.'
 ,_ (  \   ) '..' )  ) ,_ .' \  )  ) ,._.'    ) \     ,_   ) ,._.'  / /
(  '.)  ) (  ,   (  (  ' ) \  ) \ (  '        \ (    (  \ (  '     (  \
 '._,_.'   )/'._.'   )/   )/   )/  )/          )/     ).'  )/       ).'
"""
## banner ##

verbose = False
very_verbose = False

def parse_args():
    # argparse code. I need to learn how to use argparse.
    # planning on adding -i for interface, -D for decoy (using like src from scapy)
    # ping (regular ping), -v (verbose)
    parser = argparse.ArgumentParser(description=f"scaper.py going nuclear")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument(
            "-p", "--port",
            help="Ports to scan (e.g., 22,80,443 or 20-100)",
            required=False,
            default="0-1000"
        )
    parser.add_argument(
            "--banner",
            help="Display port version banner",
            action="store_true"
    )
    parser.add_argument(
            "-D", "--decoy",
            help=f"Decoy ip addresses separated by commas (e.g., 10.10.10.10,10.10.10.11,etc.)",
            required=False,
            default=None
        )
    parser.add_argument(
            "-v", "--verbose",
            help="Enable verbose output",
            action="store_true"
        )
    parser.add_argument(
            "-vv", "--very-verbose",
            help="Enable very verbose output",
            action="store_true"
        )
    parser.add_argument(
            "-vlvl", "--vlvl",
            help="Set verbosity level (0-3)",
            type=int,
            choices=[0, 1, 2, 3],
            default=0
        )
    args = parser.parse_args()
    return args
open_ports = []
def scanner(ip, port, decoys=None):
    global vlvl
    global verbose
    global very_verbose
    packet = IP(dst=ip)/TCP(dport=port, flags="S")

    if decoys:
        for decoy in decoys:
            try:
                decoy_packet = IP(src=decoy, dst=ip)/TCP(dport=port, flags="S")
                sr1(decoy_packet, timeout=1, verbose=vlvl)
                if very_verbose:
                    print(f"{bold}{yellow}[*]{reset} Sending decoy packet from {decoy} to {ip}:{port}")

            except Exception as e:
                print(f"{bold}{red}[ERROR]{reset}{e}")
                sys.exit(1)

    response = sr1(packet, timeout=1, verbose=vlvl)
    if response is None:
        print(f"{bold}{yellow}[-]{reset} No response {ip}:{port}")
    elif response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:
            print(f"{bold}{green}[+]{reset} {ip}:{port} is OPEN")
            open_ports.append(port)
        elif response.getlayer(TCP).flags == 0x14:
            if verbose or very_verbose:
                print(f"{bold}{red}[-]{reset} {ip}:{port} is CLOSED")
    else:
        if verbose or very_verbose:
            print(f"{bold}{yellow}[*]{reset} Unexpected response")

def scan_ports(ip, ports, decoys=None):
    for port in ports:
        scanner(ip, port, decoys)

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024)
        print(f"{bold}{green}[+]{reset} {ip}:{port} - {banner.decode().strip()}")
        s.close()
    except socket.timeout:
        print(f"{bold}{red}[ERROR]{reset} Timeout while grabbing banner from {ip}:{port}")
    except socket.error as e:
        print(f"{bold}{red}[ERROR]{reset} Socket error: {e}")
    except Exception as e:
        print(f"{bold}{red}[ERROR]{reset} {e}")
    finally:
        try:
            s.close()
        except:
            pass

def main():
    global verbose
    global very_verbose
    global vlvl
    args = parse_args()
    scope = args.target
    verbose = args.verbose
    ports_in = args.port
    banner_grab = args.banner
    decoys_in = args.decoy
    very_verbose = args.very_verbose
    vlvl = args.vlvl

    ports = []
    if "-" in ports_in:
        start, end = map(int, ports_in.split("-"))
        ports = range(start, end + 1)
    else:
        ports = list(map(int, ports_in.split(",")))
    decoys = decoys_in.split(",") if decoys_in else None
    
    scan_ports(scope, ports, decoys)
    if banner_grab:
        for port in open_ports:
            grab_banner(scope, port)

if __name__ == "__main__":
    print(f"{bold}{green}{script_banner}{reset}")
    try:
        main()
    except (KeyboardInterrupt, PermissionError) as e:
        print(f"{bold}{red}[ERROR]{reset} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{bold}{red}[ERROR]{reset} {e}")
        sys.exit(1)
    finally:
        if very_verbose:
            print(f"{bold}{yellow}[*]{reset} Script finished")
            sys.exit(0)
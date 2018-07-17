"""
Blacklist checker.

Usage:
    blacklist-checker [options] --file=<file> [--smtp=<server> --from=<from> --to=<to>] ip <ip>...
    blacklist-checker [options] --file=<file> [--smtp=<server> --from=<from> --to=<to>] domain <domain>...
    blacklist-checker -h | --help

Options:
  -h  --help     Show this screen.
  -t <timeout>   Sets dns query timeout [default: 1]
  -l <lifetime>  Sets dns query lifetime [default: 1]
"""

# Works with domain names and IPs

import dns.resolver
import dns.reversename
import smtplib
from email.message import EmailMessage
import datetime
import sys
from docopt import docopt

domain_list = []
domain_ips = []

ip_rip = {}

blacklists = []
bl_listed = []


def read_conf():
    if arguments["<domain>"]:
        for domain in arguments["<domain>"]:
            domain_list.append(domain)
    elif arguments["<ip>"]:
        for ip in arguments["<ip>"]:
            domain_ips.append(ip)


def read_blacklists():
    try:
        with open(arguments["--file"]) as file:
            for line in file:
                blacklists.append(line.strip())
    except (FileNotFoundError, PermissionError):
        print("WRONG FILE OR NO FILE WITH BLACKLISTS")
        sys.exit(1)


def get_ip_from_domain():
    print()
    for domain in domain_list:
        try:
            ip = dns.resolver.query(domain, "A")
            domain_ips.append(ip.rrset.items[0].address)
            print(f"{domain} : {ip.rrset.items[0].address}")
            print()
        except dns.resolver.NXDOMAIN:
            print(f"Domain {domain} does not exist")
    return


def reverse_ip():
    # METHOD 1
    # for ip in domain_ips:
    #     reversed_ip = dns.reversename.from_address(ip)
    #     ip_rip[ip] = str(reversed_ip)[:-14]

    # METHOD 2
    for ip in domain_ips:
        try:
            new_ip = ip.split(".")
            reversed_ip = new_ip[3] + "." + new_ip[2] + "." + new_ip[1] + "." + new_ip[0]
            ip_rip[ip] = reversed_ip
        except IndexError:
            print(f"{ip} Invalid IP address")
    return


def check_blacklists():
    resolver = dns.resolver.Resolver()
    try:
        resolver.timeout = int(arguments["-t"])
        resolver.lifetime = int(arguments["-l"])
    except ValueError:
        print("timeout and lifetime must be integers")
        sys.exit(1)

    for normal_ip, reversed_ip in ip_rip.items():
        print()
        print("Checking: " + normal_ip)
        for blist in blacklists:
            try:
                result = resolver.query(reversed_ip + "." + blist)
                if result.rrset:
                    print(f"{blist}: \033[91mLISTED\033[0;0m".rjust(50))
                    bl_listed.append(f"{blist}: LISTED")
            except dns.resolver.NXDOMAIN:
                print(f"{blist}: \033[90mNOT LISTED\033[0;0m".rjust(50))
            except (dns.resolver.NoAnswer, dns.exception.Timeout):
                print(f"{blist}: \033[93mFAILED\033[0;0m".rjust(50))
    return


def send_email():
    if arguments["--smtp"] and arguments["--from"] and arguments["--to"]:
        msg = EmailMessage()

        try:
            s = smtplib.SMTP(arguments["--smtp"])
        except:
            print("Could not connect to SMTP server")
            sys.exit(1)

        msg["Subject"] = f"BLACKLIST CHECK {now:%Y-%m-%d}"
        msg["From"] = arguments["--from"]
        msg["To"] = arguments["--to"]

        if not bl_listed:
            msg.set_content("NOT LISTED")
        else:
            msg.set_content("\n".join(bl_listed))

        try:
            s.send_message(msg)
            s.quit()
        except smtplib.SMTPRecipientsRefused:
            print("Invalid recipent address")
            sys.exit(1)
        except smtplib.SMTPSenderRefused:
            print("Invalid sender address")
            sys.exit(1)
    else:
        pass
    return


if __name__ == '__main__':
    now = datetime.datetime.now()

    arguments = docopt(__doc__)

    print()
    print(f"BLACKLIST CHECK {now:%Y-%m-%d}")
    print()

    read_conf()
    read_blacklists()
    get_ip_from_domain()
    reverse_ip()
    check_blacklists()
    send_email()

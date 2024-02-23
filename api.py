#!/usr/bin/env python3

from bottle import route, run, template 
import os
import re
import subprocess
from urllib.parse import urlparse

# helper functions
def add(data, fp):
    with open(fp, "a") as f:
        f.write(data)
        f.write("\n")
    return "Success"

def rm(data, fp):
    with open(fp,"r") as f:
        lines = f.readlines()
    with open(fp, "w") as f:
        for line in lines:
            if not data in line.strip("\n"):
                f.write(line)
    return "Done"

def show(fp):
    d = ""
    with open(fp, "r") as f:
        d = f.read()
    return d

def do_config(oper):
    sanitize = re.sub(r"\W+", "", oper)
    if sanitize in ["start", "stop", "restart", "reload"]:
        subprocess.call(["systemctl", "{}".format(sanitize), "squid.service"])
        return "Success"
    else:
        return "Invalid Command"


# api routes
@route("/service/<oper>")
def handle_service_manage(oper):
    r = do_config(oper)
    return r

@route("/domain/<stat>/<domain>")
def handle_domain(stat, domain):
    if stat == "show":
        return show("/etc/squid/ban_domains.txt")
    elif stat == "add":
        r = add("." + domain, "/etc/squid/ban_domains.txt")
        return "Status: {}".format(r)
    elif stat == "remove":
        r = rm(domain, "/etc/squid/ban_domains.txt")
        return "Domain removed"
    else:
        return "Unknown Domain stat!"

@route("/arp/<stat>/<arp>")
def hanndle_arp(stat, arp):
    if stat == "show":
        return show("/etc/squid/allowed_mac.txt")
    elif stat== "add":
        r = add(arp, "/etc/squid/allowed_mac.txt")
        return "Status: {}".format(r)
    elif stat == "remove":
        r = rm(arp, "/etc/squid/allowed_mac.txt")
        return "ARP removed"
    else:
        return "Unknown ARP stat!"

@route("/port/<stat>/<port>")
def handle_port(stat, port):
    if stat == "show":
        return show("/etc/squid/allowed_ports.txt")
    elif stat == "add":
        r = add(port, "/etc/squid/allowed_ports.txt")
        return "Status: {}".format(r)
    elif stat == "remove":
        r = rm(port, "/etc/squid/allowed_ports.txt")
        return "Port removed"
    else:
        return "Unknown stat!"

run(host="0.0.0.0", port=7505, debug=True)

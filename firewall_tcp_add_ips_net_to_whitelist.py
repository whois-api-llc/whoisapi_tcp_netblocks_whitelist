#!/usr/bin/env python3
"""
Python script to add netblocks to an iptables filter for ssh or other tcp.
Usable example code. 
Details in the README file
(c) WhoisXML API, Inc. 2022.
Licensed under GPL.
"""
import sys
import os
from time import sleep
import netaddr
import ipnetblocks

#Configuration.
#Customize here.
#API key for the IP Netblocks API, subscribe here:
#https://ip-netblocks.whoisxmlapi.com/api
APIKEY = "YOUR_API_KEY"
#This is the file containing allowed CIDRs and IPs:
ALLOWEDFILE = "/etc/ssh/allowed_networks"

#We need an IP address as a positional argument
try:
    ip = sys.argv[1]
except:
    sys.stderr.write("Error: an IP address has to be specified")


#We get the netblocks our IP belongs to
#using the Netblocks API:
try:
    client = ipnetblocks.Client(APIKEY)
    ipwhois_data = client.get(ip)
    #Description of the ranges
    descriptions = []
    #The ranges in from IP - to IP format
    inetnums = []
    for network in ipwhois_data.inetnums:
        descriptions.append(
            network.inetnum + ' ' + \
            network.netname + '-' + \
            str(network.description))
        inetnums.append(network.inetnum)
except Exception as e:
    print("Netblocks API error: %s"%str(e))
    sys.exit(1)

#Offer the user the list of netblocks
#to select the one to be added.
#Print a numbered list
k = 1
for network in descriptions:
    print(k, network)
    k += 1

#Now we keep on asking the user
#until we get a valid result
choice = -1
while not 1 <= choice <= len(descriptions):
    choice = input("Which one you choose? (Default: 1) ")
    #The default
    if choice == '':
        choice = 1
    else:
        try:
            #valid number
            choice = int(choice)
        except:
            #invalid answer
            choice = -1

#Python starts numbering with 0:
choice -= 1

#Confirm the choice again
yn = input("Add %s (y/n)? "%descriptions[choice])
if yn != 'y':
    print("Aborted")
    sys.exit(1)

#Extract CIDRs from the obtained netrange
[ip_low, ip_high] = [s.strip() for s in inetnums[choice].split('-')]
cidrs = set(
    [str(network) for network in netaddr.iprange_to_cidrs(ip_low, ip_high)])

#Read the already added CIDRS from the file
with open(ALLOWEDFILE, 'rt') as whitelist_file:
    current_list = set([s.strip() for s in whitelist_file.readlines()])
    whitelist_file.close()

#Create the union of the set of old and new CIDRs
new_whitelist = sorted(list(current_list.union(cidrs)))

#Write it back to the file
with open(ALLOWEDFILE, 'wt') as whitelist_file:
    for target in new_whitelist:
        whitelist_file.write("%s\n"%target)
    whitelist_file.close()

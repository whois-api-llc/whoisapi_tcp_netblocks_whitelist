#!/bin/bash
"""
BASH script to add additional firewall rules for inbound tcp,
based on a file with allowed IPs and CIDRs.
Usable example code. 
Details in the README file
(c) WhoisXML API, Inc. 2022.
Licensed under GPL.
"""

#Customize here
#SSH port.
#We'll filter inbound tcp connections from this:
SSHPORT=22
#The whitelist file wit an IP or CIDR each line
WHITELISTFILE=/etc/ssh/allowed_networks

#We want the whitelist file to exist already.
#If it does not, the user may get locked out.
if [ ! -f $WHITELISTFILE ];then
   echo "Error: $WHITELISTFILE does not exist."
   echo "Create one with a default whitelisted IP or range"
   exit 1

#Echo the configuration
echo "ssh port: $SSHPORT"
echo "whitelist: $WHITELISTFILE"

#comm needs a sorted file, so we sort the whitelist.
#We keep it in a temporary file
SORTEDWL=$(tempfile)
sort -u < $WHITELISTFILE > $SORTEDWL

#Get a sorted list of already existing ACCEPT
#rules for the given port,
#find new IPs and ranges from the whitelist
#and add ACCEPTs for them
#to the beginning of the INPUT chain
iptables -L -n | grep ACCEPT | \
    grep "dpt:$SSHPORT" | \
    awk '{print $4}' | \
    sort -u | \
    comm -13 - $SORTEDWL | \
    while read target
    do
	echo "Adding $target to the beginnning of INPUT chain"
	iptables -I INPUT -p tcp -s "$target" --dport $SSHPORT -j ACCEPT
    done
#Remove the temporary file
rm $SORTEDWL

#If there is no generic DROP rule for the port,
#append it to the end of the INPUT chain
if ! (iptables -L -n | grep DROP | grep -q "dpt:$SSHPORT")
then
    echo "Adding missing drop rule to the end of INPUT chain."
    iptables -A INPUT -p tcp -s 0.0.0.0/0 --dport $SSHPORT -j DROP
fi
#Report that we are done.
echo "Done."

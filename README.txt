	   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
	    SET IPATABLES TCP INBOUND WHITELIST RULES FOR A
			PORT BASED ON NETBLOCKS

			   WhoisXML API, Inc.
	   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Table of Contents
─────────────────

1 Files
2 Setup and use
.. 2.1 Get your API key
.. 2.2 Install the required python packages, e.g.
.. 2.3 Set up an initial whitelist file, e.g.
.. 2.4 Configure the scripts
.. 2.5 Activate the whitelist
.. 2.6 Add new IPs or netblocks to the whitelist.
3 License


Scripts to maintain iptables firewall rules to allow ssh (or other tcp)
inbound connections only from specific network ranges. It is intended to
use on Linux and similar systems. It helps to set up network ranges
based on a single member IP, e.g. to whitelist a cellphone operator's
dynamic IP network based on a simple IPv4 address.

The ranges are stored in a whitelist file in CIDR format. The file can
also contain IP addresses.

This is a tutorial demonstration that can be used in practice. Feel free
to modify, customize, etc.


1 Files
═══════

  README.org
        this README in emacs org format
  README.md
        this README in markdown
  README.txt
        this README as plain text
  LICENSE.txt
        license, GPL v3.0
  requirements.txt
        requirements for the python script
  firewall_tcp_add_ips_net_to_whitelist.py
        script that
  firewall_tcp_update_iptables.sh
        script to update iptables settings


2 Setup and use
═══════════════

  Do everything on your local machine as `root'.


2.1 Get your API key
────────────────────

  Subscribe to the IP netblocks API at its web site,
  [https://ip-netblocks.whoisxmlapi.com/api]. A free access is available
  and it is likely to be sufficient if you manage a small system. You
  will get an API key.


2.2 Install the required python packages, e.g.
──────────────────────────────────────────────

  ┌────
  │ pip3 install -r requirements.txt
  └────


2.3 Set up an initial whitelist file, e.g.
──────────────────────────────────────────

  ┌────
  │ echo '192.168.0.0/16' >> /etc/ssh/allowed_networks
  └────
  If you are using ssh for your session, it is important that your
  current IP or its range should be on the whitelist.


2.4 Configure the scripts
─────────────────────────

  Customize lines 11 to 17 of `firewall_tcp_update_iptables.sh' and
  lines 15 to 21 of `firewall_tcp_add_ips_net_to_whitelist.py'. There
  are three settings: the file holding the whitelisted IPs and networks,
  `/etc/ssh/allowed_networks' by default, the port of the ssh service,
  22 by default, and your API key obtained in the first step.


2.5 Activate the whitelist
──────────────────────────

  To update the rules of the INPUT chain, run
  `firewall_tcp_update_iptables.sh'. It will ensure that the given port
  rejects everything by default and add the newly added IPs and ranges
  to the whitelist. The script can be run anytime. By default, iptables
  will forget settings after reboot, so you may want to run it upon
  bootup.


2.6 Add new IPs or netblocks to the whitelist.
──────────────────────────────────────────────

  To add single IPs, e.g. `10.0.0.2' just do
  ┌────
  │ echo '10.0.0.2' >> /etc/ssh/allowed_networks
  └────
  Then run `firewall_tcp_update_iptables.sh'.  You can do the same to
  manually add ranges in CIDR notation, e.g. `192.168.0.0/16'

  To add a network a given IP belongs to, assuming e.g. you want to add
  a netblock which `8.8.8.8' belongs to, run
  `firewall_tcp_add_ips_net_to_whitelist.py' like this:
  ┌────
  │ ./firewall_tcp_add_ips_net_to_whitelist.py 8.8.8.8
  └────
  Your session will look like this:
  ┌────
  │ 1 8.8.8.0 - 8.8.8.255 LVLT-GOGL-8-8-8-[]
  │ 2 8.0.0.0 - 8.15.255.255 LVLT-ORG-8-8-[]
  │ 3 8.0.0.0 - 8.127.255.255 LVLT-ORG-8-8-[]
  │ 4 8.0.0.0 - 8.255.255.255 NET8-[]
  │ 5 6.0.0.0 - 13.115.255.255 NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK-['IPv4 address block not managed by the RIPE NCC']
  │ 6 0.0.0.0 - 255.255.255.255 IANA-IPV4-MAPPED-ADDRESS-[]
  │ 7 :: - ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff IANA-BLK-['The whole IPv6 address space']
  │ Which one you choose? (Default: 1) 1
  │ Add 8.8.8.0 - 8.8.8.255 LVLT-GOGL-8-8-8-[] (y/n)?
  └────
  The whitelist file will now contain `8.8.8.0/24'.  Then run
  `firewall_tcp_update_iptables.sh' to activate your new settings.

  Instead on `8.8.8.8' you will probably want to add e.g. a range
  belonging to your cellphone network provider where your phone gets
  your IPs from.


3 License
═════════

  (c) WhoisXML API, Inc. 2022.

  The code is licensed under General Public License v 3.0. A copy of the
  license is included in the file LICENSE.txt.

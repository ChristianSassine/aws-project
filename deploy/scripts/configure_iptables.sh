#!/bin/bash

echo "configuring iptables for trusted host"
echo "Gatekeeper ip: $1"
echo "Proxy ip: $2"

# Clear existing rules
sudo iptables -F
# Allow INPUT from gatekeeper
sudo iptables -A INPUT -p tcp --dport 80 -s $1 -j ACCEPT
# Allow OUTPUT to proxy
sudo iptables -A OUTPUT -p tcp --dport 80 -s $2 -j ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Allow Established and related connections
sudo iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Show the rules
sudo iptables -L -v -n
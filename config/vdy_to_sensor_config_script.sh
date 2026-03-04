#!/bin/bash

echo "Richte alle Konfigurationen fuer die Ethernet Schnittstelle ein"
sudo ip addr add 192.168.16.5/24 dev eth0
sudo ip link add link eth0 name eth0.34 type vlan id 34
sudo ip link set eth0.34 up
sudo ip addr add 192.168.16.5/24 dev eth0.34

echo "Richte alle Konfigurationen fuer das CAN Interface ein"
sudo ip link set can0 type can bitrate 250000
sudo ip link set up can0 

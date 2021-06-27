#!/bin/bash

echo '[+] net guy here!'

# add multicast ip route!!
sudo ip route add 224.0.0.0/4 dev eth1

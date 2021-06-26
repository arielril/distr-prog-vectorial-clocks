#!/bin/bash

echo 'Here is the boot guy!'

# Install necessary packages
sudo apt-get install -y \
  python3

# link python to python3
sudo ln -sf $(which python3) /bin/python

# add multicast ip route!!
sudo ip route add 224.0.0.0/4 dev eth1

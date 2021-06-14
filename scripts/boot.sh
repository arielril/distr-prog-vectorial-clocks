#!/bin/bash

echo 'Here is the boot guy!'

# Install necessary packages
sudo apt-get install -y \
    python3

# link python to python3
sudo ln -sf $(which python3) /bin/python

pip install -r requirements.txt

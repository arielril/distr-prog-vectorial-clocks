#!/bin/bash

echo 'Here is the alias guy!'

# Add aliases
echo 'alias la="ls -lah"' >/root/.bashrc 2>/dev/null
echo 'alias la="ls -lah"' >/home/vagrant/.bashrc 2>/dev/null

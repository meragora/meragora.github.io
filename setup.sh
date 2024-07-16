#!/bin/bash
# Update package list
apt-get update
# Install build-essential and other necessary packages
apt-get install -y build-essential libssl-dev libffi-dev python3-dev

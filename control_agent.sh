#! /bin/bash
sudo apt-get update
sudo apt-get -y install git
sudo apt-get -y install wget
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
cd /root/
sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install flask
sudo pip install paramiko
sudo git clone https://github.com/oceanshy/Swarm-Agent.git

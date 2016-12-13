#! /bin/bash

sudo docker pull registry
sudo docker run -d -p 5000:5000 --name registry registry


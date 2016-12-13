#! /bin/bash

# cd /root/switch_25_10_2016
# sh /root/switch_25_10_2016/build_and_deploy.sh
# sudo docker tag mogswitch/inputdistributor localhost:5000/inputdistributor
# sudo docker push localhost:5000/inputdistributor
# sudo docker tag mogswitch/proxytranscoder localhost:5000/proxytranscoder
# sudo docker push localhost:5000/proxytranscoder
# sudo docker tag mogswitch/videoswitcher localhost:5000/videoswitcher
# sudo docker push localhost:5000/videoswitcher
# sudo docker tag mogswitch/outputtranscoder localhost:5000/outputtranscoder
# sudo docker push localhost:5000/outputtranscoder

sudo docker pull ubuntu
sudo docker tag ubuntu localhost:5000/ubuntu
sudo docker push localhost:5000/ubuntu


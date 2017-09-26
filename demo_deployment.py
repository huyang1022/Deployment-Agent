#! /usr/bin/env python

# Copyright 2017 --Yang Hu--
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'Yang Hu'

import paramiko, time
from img_info import ImgInfo
import threading


def pull_img(img, in_img, fl_img, in_ip, now_img, start_time):
    try:
        print "%s, %s: ======= Start Deploying =======" % (img.name, img.image)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(img.ip, username=img.user, key_filename=img.key)
        stdin, stdout, stderr = ssh.exec_command("sudo docker pull %s" % (img.image))
        stdout.read()
        print "%s, %s: ======= Finish Deploying =======" % (img.name, img.image)
    except Exception as e:
            print '%s: %s' % (img.ip, e)
    ssh.close()
    finish_time = time.time() - start_time
    in_img.append(now_img)
    in_ip.remove(img.ip)
    if finish_time >  img.deadline:
        fl_img.append(now_img)
    print "VM: %s, Image: %s, Deadline: %f(s), Finish Time: %f(s)" % (img.name, img.image, img.deadline, finish_time)



def run(in_file):
    img_list = []
    in_file.readline()
    while True:
        line = in_file.readline()
        file_list = line.split()
        if not file_list: break
        if file_list[0] == "node0":
            img = ImgInfo("129.7.98.10", "root", "/Users/Oceans/.ssh/id_rsa", file_list[0], file_list[1], int(file_list[2]))
        if file_list[0] == "node1":
            img = ImgInfo("129.7.98.11", "root", "/Users/Oceans/.ssh/id_rsa", file_list[0], file_list[1], int(file_list[2]))
        if file_list[0] == "node2":
            img = ImgInfo("129.7.98.13", "root", "/Users/Oceans/.ssh/id_rsa", file_list[0], file_list[1], int(file_list[2]))
        if file_list[0] == "node3":
            img = ImgInfo("129.7.98.12", "root", "/Users/Oceans/.ssh/id_rsa", file_list[0], file_list[1], int(file_list[2]))
        img_list.append(img)

    img_cnt = len(img_list)

    threads = []


    # =============== Bandwidth-aware EDF ============================
    img_list.sort(key=lambda x:  x.deadline)
    in_ip = []
    in_img = []
    fl_img = []


    start_time = time.time()

    while len(in_img) < img_cnt:
        now_img = 0

        for i in img_list:
            now_img += 1
            if (now_img not in in_img)  and (i.ip not in in_ip):
                in_ip.append(i.ip)
                threads.append(threading.Thread(target=pull_img, args=(i, in_img, fl_img, in_ip, now_img, start_time)))
                threads[-1].start()


        time.sleep(0.01)

    for t in threads:
        t.join()
    fl_cnt = len(fl_img)
    print "=============== Bandwidth-aware EDF ========================"
    print "Total Deployment Time: %f(s)" % (time.time() - start_time)
    print "Deadline Missing Times: %d" % (fl_cnt)
    print "\n"




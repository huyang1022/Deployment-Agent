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

import paramiko, os
from vm_info import VmInfo
def install_manager(vm):
	try:
		print "%s: ====== Start Kubernetes Master Installing ======" % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		sftp = ssh.open_sftp()
		file_path = os.path.dirname(__file__)
		sftp.chdir('/tmp/')
		install_script = file_path + "/" + "docker_kubernetes.sh"
		sftp.put(install_script, "kubernetes_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo hostname ip-%s" % (vm.ip.replace('.','-')))
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo sh /tmp/kubernetes_setup.sh")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo kubeadm init --api-advertise-addresses=%s" % (vm.ip))
		retstr = stdout.readlines()
		stdin, stdout, stderr = ssh.exec_command("sudo cp /etc/kubernetes/admin.conf /tmp/")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo chown %s /tmp/admin.conf" % (vm.user))
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo chgrp %s /tmp/admin.conf" % (vm.user))
		stdout.read()
		sftp.get("/tmp/admin.conf", file_path+"/admin.conf")
		print "%s: ========= Kubernetes Master Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()
	return retstr[-1]

def install_worker(join_cmd, vm):
	try:
		print "%s: ====== Start Kubernetes Slave Installing ======" % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		sftp = ssh.open_sftp()
		sftp.chdir('/tmp/')
		file_path = os.path.dirname(__file__)
		install_script = file_path + "/" + "docker_kubernetes.sh"
		sftp.put(install_script, "kubernetes_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo hostname ip-%s" % (vm.ip.replace('.','-')))
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo sh /tmp/kubernetes_setup.sh")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo %s" % (join_cmd))
		stdout.read()
		print "%s: ========= Kubernetes Slave Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def run(vm_list):
	for i in vm_list:
		if i.role == "master": join_cmd = install_manager(i)

	join_cmd = join_cmd.encode()
	join_cmd = join_cmd.strip()

	for i in vm_list:
		if i.role == "slave": install_worker(join_cmd, i)

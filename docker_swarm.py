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
		print "%s: ====== Start Swarm Manager Installing ======" % (vm.ip)
		paramiko.util.log_to_file("deployment.log")
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo docker info | grep Swarm")
		temp_list = stdout.readlines()
		temp_str = ""
		for i in temp_list: temp_str += i
		if temp_str.find("Swarm: active") != -1: return "SUCCESS"
		stdin, stdout, stderr = ssh.exec_command("sudo docker swarm leave --force")
		retstr = stdout.readlines()
		stdin, stdout, stderr = ssh.exec_command("sudo docker swarm init --advertise-addr %s" % (vm.ip))
		retstr = stdout.readlines()
		print "%s: ========= Swarm Manager Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()
	return retstr[4] + retstr[5] + retstr[6]

def install_worker(join_cmd, vm):
	try:
		print "%s: ====== Start Swarm Worker Installing ======" % (vm.ip)
		paramiko.util.log_to_file("deployment.log")
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo docker swarm leave --force")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo %s" % (join_cmd))
		stdout.read()
		print "%s: ========= Swarm Worker Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def run(vm_list):
	for i in vm_list:
		if i.role == "master":
			join_cmd = install_manager(i)
			if "SUCCESS" in join_cmd:
				return join_cmd
			else:
				join_cmd = join_cmd.encode()
				join_cmd = join_cmd.replace("\n" , "")
				join_cmd = join_cmd.replace("\\" , "")
				join_cmd = join_cmd.strip()
			break


	for i in vm_list:
		if i.role == "slave": install_worker(join_cmd, i)

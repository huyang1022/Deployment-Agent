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
import threading
def install_engine(vm):
	try:
		print "%s: ====== Start Docker Engine Installing ======" % (vm.ip)
		paramiko.util.log_to_file("deployment.log")
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo dpkg --get-selections | grep docker")
		temp_list = stdout.readlines()
		temp_str = ""
		for i in temp_list: temp_str += i
		if temp_str.find("docker") != -1: return
		sftp = ssh.open_sftp()
		sftp.chdir('/tmp/')
		file_path = os.path.dirname(os.path.abspath(__file__))
		install_script = file_path + "/" + "docker_engine.sh"
		sftp.put(install_script, "engine_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo sh /tmp/engine_setup.sh")
		stdout.read()
		print "%s: ========= Docker Engine Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def run(vm_list):
	threads = []
	for i in vm_list:
		threads.append(threading.Thread(target = install_engine, args = (i, )))
		threads[-1].start()
	for t in threads:
		t.join()
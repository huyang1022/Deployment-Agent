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
def run(vm):
	try:
		print '%s: ====== Start Docker Executing ======' % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		sftp = ssh.open_sftp()
		sftp.chdir('/tmp/')
		sftp.put("TBD.sh", "execute_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo sh /tmp/execute_setup.sh")
		stdout.read()
		print '%s: ========= Docker Executed =========' % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def execute(vm_list):
	threads = []
	for i in vm_list:
		threads.append(threading.Thread(target = run, args = (i, )))
		threads[-1].start()
	for t in threads:
		t.join()




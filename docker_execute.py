#! /usr/bin/env python

__author__ = 'Yang Hu'

import paramiko, os
def execute(vm, execute_script):
	try:
		print '%s: ====== Start Docker Executing ======' % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		sftp = ssh.open_sftp()
		sftp.chdir('/root/')
		sftp.put(execute_script, "execute_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo sh /root/execute_setup.sh")
		stdout.read()
		print '%s: ========= Docker Executed =========' % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()





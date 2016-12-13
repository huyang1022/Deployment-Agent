#! /usr/bin/env python

__author__ = 'Yang Hu'

import paramiko, os
def install_engine(vm):
	try:
		print "%s: ====== Start Docker Engine Installing ======" % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		sftp = ssh.open_sftp()
		sftp.chdir('/root/')
		file_path = os.path.dirname(__file__)
		install_script = file_path + "/" + "docker_engine.sh"
		sftp.put(install_script, "engine_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo sh /root/engine_setup.sh")
		stdout.read()
		print "%s: ========= Docker Engine Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

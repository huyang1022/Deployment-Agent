#! /usr/bin/env python

__author__ = 'Yang Hu'

import paramiko, os
def install_registry(vm, install_script):
	try:
		print '%s: ====== Start Docker Registry Installing ======' % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		sftp = ssh.open_sftp()
		sftp.chdir('/root/')
		file_path = os.path.dirname(__file__)
		registry_script = file_path + "/" + "docker_registry.sh"
		sftp.put(registry_script, "registry_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo sh /root/registry_setup.sh")
		stdout.read()
		sftp.put(install_script, "images_setup.sh")
		stdin, stdout, stderr = ssh.exec_command("sudo sh /root/images_setup.sh")
		stdout.read()
		print '%s: ========= Docker Registry Installed =========' % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()





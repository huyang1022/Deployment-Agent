#! /usr/bin/env python

__author__ = 'Yang Hu'

import paramiko, os
from vm_info import VmInfo
def install_master(vm):
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

def install_slave(join_cmd, vm):
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
		stdin, stdout, stderr = ssh.exec_command("sudo sh /tmp/kubernetes_setup.sh")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo %s" % (join_cmd))
		stdout.read()
		print "%s: ========= Kubernetes Slave Installed =========" % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def install_kubernetes(in_file):
	vm_list = []
	while True:
		line = in_file.readline()
		file_list = line.split()
		if not file_list: break
		vm = VmInfo(file_list[0], file_list[1], file_list[2], file_list[3])
		vm_list.append(vm)


	for i in vm_list:
		if i.role == "master": join_cmd = install_master(i)

	join_cmd = join_cmd.encode()
	join_cmd = join_cmd.strip()

	for i in vm_list:
		if i.role == "slave": install_slave(join_cmd, i)

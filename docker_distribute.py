#! /usr/bin/env python

__author__ = 'Yang Hu'

import paramiko, os, time
from img_info import ImgInfo
from vm_info import VmInfo
import threading

def pull_img(img, in_img, fl_img, in_ip, in_flag, now_img, start_time):
	time1 = time.time()
	try:
		print "%s, %s: ======= Start Distributing =======" % (img.ip, img.image)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(img.ip, username=img.user, key_filename=img.key)
		# stdin, stdout, stderr = ssh.exec_command("sudo docker pull %s" % (img.image))
		# stdout.read()
		# stdin, stdout, stderr = ssh.exec_command("sudo docker rmi %s" % (img.image))
		# stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo iperf -c %s -n %s" % ("192.168.1.1", img.image))
		stdout.read()
		print "%s, %s: ======= Finish Distributing =======" % (img.ip, img.image)
	except Exception as e:\
		print '%s: %s' % (img.ip, e)
	ssh.close()
	time2 = time.time()
	finish_time = start_time + time2 - time1
	in_img.append(now_img)
	in_flag.remove(now_img)
	in_ip.remove(img.private_ip)
	if finish_time > img.start + img.deadline:
		fl_img.append(now_img)
	print "IP: %s, Image: %s, Deadline: %f, Start: %f, Finish: %f" % (img.ip, img.image, img.start + img.deadline, start_time, finish_time)

def tc_init(vm):
	try:
		print '%s: =========== TC Initializing =============' % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo tc qdisc del dev eth1 root")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo tc qdisc add dev eth1 root handle 1:0 htb")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo tc class add dev eth1 parent 1:0 classid 1:1 htb rate 1000mbit")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo tc class add dev eth1 parent 1:0 classid 1:2 htb rate 10kbit")
		stdout.read()
		print '%s: ========= Finish TC Initialization =======' % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def tc_add(vm, ip, bandwidth):
	try:
		print '%s, %s: =========== TC Adding =============' % (ip, bandwidth)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo tc filter del dev eth1 parent 1:0 prio 1")
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo tc class change dev eth1 parent 1:0 classid 1:1 htb rate %dmbit" % (bandwidth))
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo tc filter add dev eth1 parent 1:0 prio 1 u32 match ip dst %s flowid 1:1" %(ip))
		stdout.read()
		print '%s, %s: ========= Finish TC Adding =========' % (ip, bandwidth)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def tc_del(vm):
	try:
		print '%s: =========== TC Deleting =============' % (vm.ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo tc filter del dev eth1 parent 1:0 prio 1")
		stdout.read()
		print '%s: ========= Finish TC Deleting =========' % (vm.ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def tc_add_limit(vm, ip, priority):
	try:
		print '%s: =========== TC Adding Limit =============' % (ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo tc filter del dev eth1 parent 1:0 prio %d" % (priority))
		stdout.read()
		stdin, stdout, stderr = ssh.exec_command("sudo tc filter add dev eth1 parent 1:0 prio %d u32 match ip dst %s flowid 1:2" %(priority, ip))
		stdout.read()
		print '%s: ========= Finish TC Adding Limit =========' % (ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def tc_del_limit(vm, ip, priority):
	try:
		print '%s: =========== TC Deleting Limit =============' % (ip)
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(vm.ip, username=vm.user, key_filename=vm.key)
		stdin, stdout, stderr = ssh.exec_command("sudo tc filter del dev eth1 parent 1:0 prio %d" % (priority))
		stdout.read()
		print '%s: ========= Finish TC Deleting Limit =========' % (ip)
	except Exception as e:
		print '%s: %s' % (vm.ip, e)
	ssh.close()

def distribute(in_file):
	img_list = []
	while True:
		line = in_file.readline()
		file_list = line.split()
		if not file_list: break
		img = ImgInfo(file_list[0], file_list[1], file_list[2], file_list[3], float(file_list[4]), float(file_list[5]), file_list[6])
		img_list.append(img)
	
	img_cnt = len(img_list)
	ip_list = ["192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"]
	bd_list = [100, 70, 50, 20]
	tc_list = [0,0,0,0]
	vm_registry = VmInfo("145.100.133.159", "root", "/Users/Oceans/.ssh/id_dsa", "")
	total_bd = 100
	threads = []
# =============== Bandwidth-aware EDF ============================
	img_list.sort(key = lambda x: x.start + x.deadline)
	tc_init(vm_registry)
	in_flag = []
	in_ip = []
	in_img = []
	fl_img = []
	tc_bd = 0
	tc_img = 0
	start_time = time.time()

	while len(in_img) < img_cnt:
		now_time = time.time() - start_time
		now_img = 0
		now_bd = 0

		# for i in in_ip:
		# 	j = ip_list.index(i)
		# 	now_bd += bd_list[j]
		# if now_bd < total_bd:
		# 	if tc_bd != 0:
		# 		tc_del(vm_registry)
		# 		tc_bd = 0
		for i in img_list:
			now_img +=1
			if (now_img not in in_img) and (now_time > i.start) and (i.private_ip not in in_ip):
				in_flag.append(now_img)
				in_ip.append(i.private_ip)
				threads.append(threading.Thread(target = pull_img, args = (i, in_img, fl_img, in_ip, in_flag, now_img, now_time)))
				threads[-1].start()
				# break
			if (now_img in in_flag):
				j = ip_list.index(i.private_ip)
				if now_bd < total_bd:
					if (now_bd + bd_list[j] >= total_bd):
						if (tc_img != now_img) or (tc_bd != total_bd - now_bd):
							tc_img = now_img
							tc_bd = total_bd - now_bd
							tc_add(vm_registry, i.private_ip, tc_bd)
					else:
						if (tc_list[j] == -1):
							tc_list[j] = 0
							tc_del_limit(vm_registry, i.private_ip, now_img + 1)
				else:
					if (tc_list[j] == 0):
						tc_list[j] = -1
						tc_add_limit(vm_registry, i.private_ip, now_img + 1)
				now_bd += bd_list[j]

		if now_bd < total_bd:
			if tc_bd != 0:
				tc_del(vm_registry)
				tc_bd = 0
				tc_img = 0



		# else:
		# 	t_bd = bd_list[ip_list.index(in_ip[-1])]
		# 	t_bd = now_bd - t_bd
		# 	t_bd = total_bd - t_bd
		# 	if tc_bd != t_bd:
		# 		tc_add(vm_registry, in_ip[-1], t_bd)
		# 		tc_bd = t_bd


		time.sleep(0.01)

	for t in threads:
		t.join()	
	fl_cnt = len(fl_img)
	print "=============== Bandwidth-aware EDF ========================"
	print "Total time: %f" % (time.time()-start_time)
	print "Total image: %d" % (img_cnt)
	print "Failure times: %d" % (fl_cnt)
	print "Failure Rate: %f" % (fl_cnt * 1.0 / img_cnt)
	print "\n"

# ===============  EDF ============================
	img_list.sort(key = lambda x: x.start + x.deadline)
	tc_init(vm_registry)
	in_ip = []
	in_img = []
	fl_img = []
	start_time = time.time()

	while len(in_img) < img_cnt:
		now_time = time.time() - start_time
		now_img = 0
		if not len(in_ip):
			for i in img_list:
				now_img +=1
				if (now_img not in in_img) and (now_time > i.start) and (i.private_ip not in in_ip):
					in_flag.append(now_img)
					in_ip.append(i.private_ip)
					threads.append(threading.Thread(target = pull_img, args = (i, in_img, fl_img, in_ip, in_flag, now_img, now_time)))
					threads[-1].start()
					break
		time.sleep(0.01)

	for t in threads:
		t.join()	
	fl_cnt = len(fl_img)
	print "=============== EDF ========================"
	print "Total time: %f" % (time.time()-start_time)
	print "Total image: %d" % (img_cnt)
	print "Failure times: %d" % (fl_cnt)
	print "Failure Rate: %f" % (fl_cnt * 1.0 / img_cnt)
	print "\n"

	# ===============  FIFO ============================
	img_list.sort(lambda x,y: cmp(x.start, y.start))
	tc_init(vm_registry)
	in_ip = []
	in_img = []
	fl_img = []
	start_time = time.time()

	while len(in_img) < img_cnt:
		now_time = time.time() - start_time
		now_img = 0
		if not len(in_ip):
			for i in img_list:
				now_img +=1
				if (now_img not in in_img) and (now_time > i.start) and (i.private_ip not in in_ip):
					in_flag.append(now_img)
					in_ip.append(i.private_ip)
					threads.append(threading.Thread(target = pull_img, args = (i, in_img, fl_img, in_ip, in_flag, now_img, now_time)))
					threads[-1].start()
					break
		time.sleep(0.01)

	for t in threads:
		t.join()	
	fl_cnt = len(fl_img)
	print "=============== FIFO ========================"
	print "Total time: %f" % (time.time()-start_time)
	print "Total image: %d" % (img_cnt)
	print "Failure times: %d" % (fl_cnt)
	print "Failure Rate: %f" % (fl_cnt * 1.0 / img_cnt)
	print "\n"

	# ===============  PARALLEL ============================
	img_list.sort(lambda x,y: cmp(x.start, y.start))
	tc_init(vm_registry)
	in_ip = []
	in_img = []
	fl_img = []
	in_flag = []
	start_time = time.time()

	while len(in_img) < img_cnt:
		now_time = time.time() - start_time
		now_img = 0
		for i in img_list:
			now_img +=1
			if (now_img not in in_img) and (now_time > i.start) and (now_img not in in_flag):
				in_flag.append(now_img)
				in_ip.append(i.private_ip)
				threads.append(threading.Thread(target = pull_img, args = (i, in_img, fl_img, in_ip, in_flag, now_img, now_time)))
				threads[-1].start()
				break
		time.sleep(0.01)

	for t in threads:
		t.join()	
	fl_cnt = len(fl_img)
	print "=============== PARALLEL ========================"
	print "Total time: %f" % (time.time()-start_time)
	print "Total image: %d" % (img_cnt)
	print "Failure times: %d" % (fl_cnt)
	print "Failure Rate: %f" % (fl_cnt * 1.0 / img_cnt)
	print "\n"







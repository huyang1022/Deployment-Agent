#!/usr/bin/python

class ImgInfo:
	def __init__(self, ip, private_ip, user, key, start, deadline, image):
		self.ip = ip
		self.private_ip = private_ip
		self.user = user
		self.key = key
		self.start = start
		self.deadline = deadline
		self.image = image
		
	def displayVm(self):
		print "IP:", self.ip, " USER:", self.user



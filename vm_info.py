#!/usr/bin/python

class VmInfo:
	def __init__(self, ip, user, key, role):
		self.ip = ip
		self.user = user
		self.key = key
		self.role = role
	def displayVm(self):
		print "IP:", self.ip, " USER:", self.user



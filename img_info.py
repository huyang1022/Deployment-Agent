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
 

class ImgInfo:
	def __init__(self, ip, private_ip, user, key, bandwidth, throughput, start, deadline, image):
		self.ip = ip
		self.private_ip = private_ip
		self.user = user
		self.key = key
		self.bandwidth = bandwidth
		self.throughput = throughput
		self.start = start
		self.deadline = deadline
		self.image = image
		
	def displayVm(self):
		print "IP:", self.ip, " USER:", self.user



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
	def __init__(self, ip, user, key, name, image, deadline):
		self.ip = ip
		self.user = user
		self.key = key
		self.name = name
		self.image = image
		self.deadline = deadline

		
	def displayVm(self):
		print "IP:", self.ip, " USER:", self.user



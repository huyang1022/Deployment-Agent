#! /usr/bin/env python

__author__ = 'Yang Hu'


import commands

def execute_cmd(cmd):
	ret1, ret2 = commands.getstatusoutput(cmd)
    print ret2
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#shared code between client and server scripts
#Tilemachos Valkaniotis

class Statistics:
	cpu = None
	memory = None
	uptime = None
	attr_list = ["memory","uptime"]
	
	def __init__(self, cpu_usage, avail_memory, uptime):
		self.cpu = cpu_usage
		self.memory = avail_memory
		self.uptime = uptime
		
		
	def iter_cpus(self):
		for cpu_core in self.cpu:
			yield cpu_core
	
	def __iter__(self):
		for item in self.attr_list:
			yield item
			
    #def iter_cpus(self):
	#	for cpu_core in cpu:
	#		yield cpu_core 
		
def info(msg):
	print "[*]",msg

def error(msg):
	print "[!]",msg

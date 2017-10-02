#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#client.py
#Tilemachos Valkaniotis 

import time
import psutil
from shared import Statistics



def main(args):
	cpu = psutil.cpu_percent(interval = 1, percpu = True)
	memory = psutil.virtual_memory()[2] #percentage!
	boot_time = psutil.boot_time()
	time_now = float(time.time())
	uptime = time_now - boot_time
	print cpu
	print memory
	print uptime
	return 0
	#there is no need to mess with sockets and encryptions and stuff
	#like that.
	#just pipe the output back to the ssh channel.. :)
	#its already encrypted.
	#
	#
	#i should put this thingie in a loop
	#and write additional code to handle the loop
	#server side
	#in order to gain a continuous stream of data
	#or not. :)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

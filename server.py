#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#server.py
#Tilemachos Valkaniotis
#The whole system works.
#Im not crazy enough to give you a fully functional system :)

import xml.etree.ElementTree
import paramiko
import time
import smtplib
import sqlite3
from scp import SCPClient
from server_modules import Client
from server_modules import Alert
from server_config import CONFIG_FILE_PATH
from server_config import CLIENT_PATH_LOCAL,CLIENT_PATH_REMOTE
from server_config import CLIENT_CONFIG_PATH_LOCAL,CLIENT_CONFIG_PATH_REMOTE
from server_config import SHARED_MODULES_PATH_LOCAL,SHARED_MODULES_PATH_REMOTE
from server_config import EMAIL_ADDRESS
from server_config import EMAIL_PASSWORD
from server_config import MONITOR_ADDRESS
from server_config import SMTP_SERVER
from server_config import SMTP_PORT
from server_config import DB_PATH
from shared import info
from shared import error
from shared import Statistics

Client_dict = dict()

def main(args):
	initialize_main_activity()
	return 0

def initialize_main_activity():
	global Client_dict
	Xml_file = xml.etree.ElementTree.parse(CONFIG_FILE_PATH)
	Xml_root = Xml_file.getroot() 
	for Xml_client in Xml_root.iter('client'):
		New_client = Client(Xml_client.attrib['ip'])
		for Xml_alert in Xml_client.iter('alert'):
			New_alert = Alert(Xml_alert.attrib["type"],
							  Xml_alert.attrib["limit"])
			New_client.append_alert(New_alert)
		New_client.port = Xml_client.attrib["port"]
		New_client.username = Xml_client.attrib["username"]
		New_client.password = Xml_client.attrib["password"]
		New_client.email = Xml_client.attrib["mail"]
		Client_dict[New_client.ip] = New_client
	ssh_connect(New_client)
	#make this multithreaded if there is remaining time

def ssh_connect(client):
	ssh_client = paramiko.SSHClient()
	#thats a hack. i need to get this over with quickly
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(client.ip,port = int(client.port),
										username = client.username,
										password = client.password)
	scp = SCPClient(ssh_client.get_transport())
	scp.put(CLIENT_PATH_LOCAL, CLIENT_PATH_REMOTE)
	scp.put(CLIENT_CONFIG_PATH_LOCAL, CLIENT_CONFIG_PATH_REMOTE)
	scp.put(SHARED_MODULES_PATH_LOCAL,SHARED_MODULES_PATH_REMOTE)
	scp.close()
	stdin,stdout,stderr = ssh_client.exec_command("python "+CLIENT_PATH_REMOTE)
	data = []
	#data appears in that order 
	#cpu usage
	#avail memory
	#uptime
	#append everything on a list
	#then construct an object
	for line in stdout:
		data.append(line.strip("\n"))
	#okay, thats clearly a hack :D
	stats = Statistics(data[0],data[1],data[2]) 
	handle_object(client.ip,stats)
	ssh_client.close()
	
def handle_object(ip,stats):
	global Client_dict
	client = Client_dict[ip]
	alerts_to_mail = []
	for alert in client.alerts:
		alert_type = alert.alert_type
		alert_limit = alert.alert_limit
		if alert_type == "cpu":
			stats.cpu = stats.cpu.strip("[]").split(",")
			for core_percent in getattr(stats,alert_type):
				if alert_limit < core_percent:
					print "Alert! Cpu!",core_percent
					alerts_to_mail.append(("cpu",
											core_percent,
											alert_limit))
			continue
		if alert_limit < getattr(stats,alert_type):
			print "Alert!",alert_type+" limit ->",alert_limit
			alert_tuple = (
				alert_type,
				alert_limit,
				getattr(stats,alert_type)
				)
			alerts_to_mail.append(alert_tuple)
	#now write everything at the db.
	write_to_db(stats,ip)
	if alerts_to_mail:
		send_mail(ip,alerts_to_mail)

	
def write_to_db(stats,ip):
	db = sqlite3.connect(DB_PATH)
	cursor = db.cursor()
	timestamp = int(time.time()) 
	for item in stats: #will iter every stat except cpu cores
		log_type = item
		value = getattr(stats,item)
		params = (log_type,value,ip,timestamp)
		cursor.execute('''INSERT INTO logs (type,value,ip,timestamp) values(?,?,?,?)''',params)
	cpu_index = 0
	for cpu_core in stats.iter_cpus():
		#to create cpu0, cpu1, cpu2, etc. entries
		params = ("cpu"+str(cpu_index),cpu_core,ip,timestamp)
		cursor.execute('''INSERT INTO logs (type,value,ip,timestamp) values(?,?,?,?)''',params)
		cpu_index +=1
	db.commit() 
	#little sucker above got 30 mins of my time
	#db kept returning no data. jesus, it was so simple
	cursor.close()

	
def send_mail(ip,alerts):
	data = ""
	for alert in alerts:
		data += alert[0]+": Limit = "+str(alert[1]+" Current value = "+str(alert[2])+"%")
		data += "\n"
	data += ip
	server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) #587
	server.starttls() #now your email is encrypted
	server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	msg = "\r\n".join([
	"From: "+EMAIL_ADDRESS,
	"To: "+MONITOR_ADDRESS,
	"Subject: Alert!",
	"",
	data
	])
	server.sendmail(EMAIL_ADDRESS, MONITOR_ADDRESS, msg)
	server.quit()
	
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
# Tilemachos Valkaniotis

#if you dont know what these 2 do
#then you are not qualified enough
PORT = 8081
BIND_IP = "0.0.0.0"

#xml with the clients. path on the server's host
CONFIG_FILE_PATH = "config.xml" 

#where and how to save the client script on the client's host 
CLIENT_PATH_REMOTE = ""

#local path of client script
CLIENT_PATH_LOCAL = "client.py" 

#where and how to save the client config on the client's host
CLIENT_CONFIG_PATH_REMOTE = ""

#local path of client config file
CLIENT_CONFIG_PATH_LOCAL = "client_config.py"

#dont think i can change this
SHARED_MODULES_PATH_LOCAL = "shared.py"

#dont think i can change this either.
#folder can change.
#dont think i can change the file name.
#must investigate
SHARED_MODULES_PATH_REMOTE = "shared.py"

#Database settings
#i used sqlite so only path :)
DB_PATH = "testdb.sqlite3"

#email username and password variables
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""
MONITOR_ADDRESS = "" #where do you want to send the alert emails?
SMTP_SERVER = "smtp.gmail.com"
STMP_PORT = 587

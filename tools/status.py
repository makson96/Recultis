#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os

recultis_dir = os.getenv("HOME") + "/.recultis/"

def check(game, shop, engine_size, runtime_size):
	#Setting initial variables
	status = "Waiting for user action"
	percent = 0
	percent0 = 0
	percent1 = 0
	percent2 = 0
	#Checking runtime
	status, percent0 = runtime_status()
	#Checking shop
	if percent0 == 100:
		if shop == "none":
			weight = [0.5, 0, 0.5]
			status = "Download of game data completed"
			percent1 = 100
		elif shop == "steam":
			weight = [0.1, 0.8, 0.1]
			from tools import steam
			status, percent1 = steam.status()
		elif shop == "gog":
			weight = [0.1, 0.8, 0.1]
			from tools import gog
			status, percent1 = gog.status()
	#Checking game engine
	if percent1 == 100:
			status, percent2 = engine_status(game, engine_size)
	#Final calculation
	percent = int(percent0*weight[0]+percent1*weight[1]+percent2*weight[2])
	return status, percent

def runtime_status():
	#This is just dummy implementation
	return "Runtime installation done", 100

def engine_status(game, url_s):
	from games import installer
	from tools import update_do
	file_path = installer.game_info(game, ["deb_file_path"])[0]
	status = "Downloading engine"
	percent = 0
	disk_s = 0
	url_s = 1
	if os.path.isfile(file_path) == True:
		f = open(file_path, "rb")
		disk_s = int(len(f.read()))
		f.close()
		percent = 95 * disk_s / url_s
		status = "Downloading engine"
	elif os.path.isdir(recultis_dir + "tmp") == True:
		status = "Installing engine"
		percent = 96
	else:
		status = "Game installation completed"
		percent = 100
	return status, percent

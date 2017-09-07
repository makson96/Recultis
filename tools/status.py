#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, urllib

recultis_dir = os.getenv("HOME") + "/.recultis/"

def check(game):
	status = "Waiting for user action"
	percent = 0
	status, percent = steam_status()
	if status == "Download of game data completed":
		status, percent = engine_status(game)
	return status, percent
	
def steam_status():
	os.chdir(recultis_dir)
	status = "Downloading and installing game data"
	percent = 0
	try:
		steam_log_file = open("steam_log.txt", "r")
		steam_log_lines = steam_log_file.readlines()
		last_important_line_nr = -1
		#Don't count any garbages as a last line
		garbage_line_list = ["CWorkThreadPool", "committing, progress"]
		#This ca be done better...
		while garbage_line_list[0] in steam_log_lines[last_important_line_nr] or garbage_line_list[1] in steam_log_lines[last_important_line_nr]:
			last_important_line_nr -= 1
		steam_last_line = steam_log_lines[last_important_line_nr]
		steam_log_file.close()
	except:
		steam_last_line = "downloading, progress: 0,0 ("
	#This code handle steamcmd status if everything is ok
	if ("downloading, progress: " in steam_last_line) or ("validating, progress: " in steam_last_line):
		steam_value = steam_last_line.split("progress: ")[1]
		steam_value = steam_value.split(" (")[0]
		steam_value = steam_value.split(",")[0]
		steam_value = steam_value.split(".")[0]
		steam_value = int(steam_value) * 70 / 100
		status = "Downloading and installing game data"
		percent = steam_value
	elif "Success!" in steam_last_line:
		status = "Download of game data completed"
		percent = 75
	#this code handle steamcmd status if warning is present.
	elif "Steam Guard" in steam_last_line:
		status = "Warning: Waiting for Steam Guard authentication."
		percent = 0
	#this code handle steamcmd status if steam tool marked steam_log.txt file with error.
	if "Steamcmd Error." in steam_last_line:
		try:
			steam_log_file = open("steam_log.txt", "r")
			steam_log_lines = steam_log_file.readlines()
			steam_error_line = steam_log_lines[-3]
			steam_log_file.close()
		except:
			steam_error_line = "Steamcmd Error. Terminate."
		if "FAILED with result code 5" in steam_error_line:
			status = "Error: Steam - bad login or password. Please correct and start again."
			percent = 0
		elif "Login or password not provided." in steam_error_line:
			status = "Error: Steam - Login or password not provided. Try again with correct one."
			percent = 0
		elif "Failed to install app" in steam_error_line:
			status = "Error: Steam - you are not game owner. Please correct and start again."
			percent = 0
		elif "FAILED with result code 65" in steam_error_line:
			status = "Error: Could not perform Steam Guard authentication. Please try again."
			percent = 0
		else:
			status = "Error: Steamcmd internal error. Please contact Recultis project for support."
			percent = 0
	return status, percent

def engine_status(game):
	from games import installer
	game_info = installer.game_info(game, ["deb_url_path", "deb_file_path"])
	link = game_info[0]
	file_path = game_info[1]
	status = "Downloading engine"
	percent = 75
	disk_s = 0
	url_s = 1
	if os.path.isfile(file_path) == True:
		f = open(file_path, "rb")
		disk_s = int(len(f.read()))
		f.close()
		d = urllib.request.urlopen(link)
		url_s = int(d.getheaders()[2][1])
		percent = 20 * disk_s / url_s
		status = "Downloading engine"
		percent = percent + 75
	elif os.path.isdir(recultis_dir + "tmp") == True:
		status = "Installing engine"
		percent = 96
	else:
		status = "Game installation completed"
		percent = 100
	return status, percent

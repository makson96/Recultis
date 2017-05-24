#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, importlib

engineer_dir = os.getenv("HOME") + "/.free-engineer/"

def check(game):
	status = "Waiting for user action"
	percent = 0
	status, percent = steam_status()
	if status == "Download of game data completed":
		status, percent = engine_status(game)
	return status, percent
	
def steam_status():
	os.chdir(engineer_dir)
	status = "Downloading and installing game data"
	percent = 0
	try:
		steam_log_file = open("steam_log.txt", "r")
		steam_log_lines = steam_log_file.readlines()
		steam_last_line = steam_log_lines[-1]
		steam_log_file.close()
	except:
		steam_last_line = "progress: 0,0 ("
	if "Login Failure" in steam_last_line:
		status = "Error: Steam - bad login or password. Please correct and start again."
		percent = 0
	elif "Failed to install app" in steam_last_line:
		status = "Error: Steam - you are not game owner. Please correct and start again."
		percent = 0
	elif "progress: " in steam_last_line:
		steam_value = steam_last_line.split("progress: ")[1]
		steam_value = steam_value.split(" (")[0]
		steam_value = steam_value.split(",")[0]
		steam_value = int(steam_value) * 70 / 100
		status = "Downloading and installing game data"
		percent = steam_value
	elif "Success!" in steam_last_line:
		status = "Download of game data completed"
		percent = 75
	return status, percent

def engine_status(game):
	chosen_game = importlib.import_module(game+".chosen_game")
	game_info = chosen_game.info(["deb_url_path", "deb_file_path"])
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
	elif os.path.isdir(engineer_dir + "tmp/opt") == True:
		status = "Installing engine"
		percent = 96
	else:
		status = "Game installation completed"
		percent = 100
	return status, percent

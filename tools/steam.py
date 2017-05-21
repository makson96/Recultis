#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, pickle, time
from subprocess import Popen

def start(login, password, engineer_dir, s_appid, game_dir):
	status = "Downloading and installing game data"
	percent = 25
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
	os.chdir(engineer_dir)
	if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", engineer_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(engineer_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	if os.path.isfile(engineer_dir+"steam_log.txt") == True:
		os.remove(engineer_dir+"steam_log.txt")
	steam_download = Popen("./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit", shell=True, stdout=open("steam_log.txt", "wb"))
	while steam_download.poll() is None:
		try:
			steam_log_file = open("steam_log.txt", "r")
			steam_log_lines = steam_log_file.readlines()
			steam_last_line = steam_log_lines[-2]
			steam_log_file.close()
		except:
			steam_last_line = "progress: 0"
		print(steam_last_line) #debug
		if "Login Failure" in steam_last_line:
			status = "Error: Steam - bad login or password. Please correct and start again."
			percent = 0
			pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
			steam_download.terminate()
		elif "progress: " in steam_last_line:
			steam_value = steam_last_line.split("progress: ")[1]
			steam_value = steam_value.split(" (")[0]
			steam_value = steam_value.split(",")[0]
			steam_value = int(steam_value) * 70 / 100
			print(steam_value)
			status = "Downloading and installing game data"
			percent = 25 + steam_value
			pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
		time.sleep(2)
	status = "Finalising Installation"
	percent = 95
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, pickle, _thread, time
from subprocess import call
from free_engineer import engineer_dir

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
	_thread.start_new_thread(call("./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit > steam_log.txt", (shell=True,)))
	while 1 == 1:
		try:
			steam_log_file = open("steam_log.txt", "r")
			steam_log_lines = steam_log_file.readlines()
			steam_last_line = steam_log_lines[-1]
			steam_log_file.close()
		except:
			steam_last_line = "progress: 0"
		print(steam_last_line)
		if steam_last_line == "not yet downloading":
			print("TODO: not yet downloading"):
		elif steam_last_line == "bad login or password":
			print("TODO: not yet downloading"):
		elif steam_last_line == "dowloadaning":
			print("TODO: downloading"):
		status = "Downloading and installing game data"
		percent = 25
		pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
		time.sleep(2)
	status = "Finalising Installation"
	percent = 95
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))

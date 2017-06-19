#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time
from subprocess import Popen

def start(login, password, recultis_dir, s_appid, game_dir):
	os.chdir(recultis_dir)
	if os.path.isfile(recultis_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", recultis_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(recultis_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	if os.path.isfile(recultis_dir+"steam_log.txt") == True:
		os.remove(recultis_dir+"steam_log.txt")
	steam_download = Popen("script -q -c \"./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit\" /dev/null", shell=True, bufsize=1, stdout=open("steam_log.txt", "wb"))
	while steam_download.poll() is None:
		time.sleep(2)
		steam_log_file = open("steam_log.txt", "r")
		steam_log_lines = steam_log_file.readlines()
		steam_last_line = steam_log_lines[-1]
		steam_log_file.close()
		#Terminate the process if bad login or password
		if "Login Failure" in steam_last_line:
			steam_download.terminate()
		#Terminate the process if not owning the game
		elif "Failed to install app" in steam_last_line:
			steam_download.terminate()

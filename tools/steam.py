#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time
from subprocess import Popen

def start(login, password, engineer_dir, s_appid, game_dir):
	os.chdir(engineer_dir)
	if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", engineer_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(engineer_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	if os.path.isfile(engineer_dir+"steam_log.txt") == True:
		os.remove(engineer_dir+"steam_log.txt")
	steam_download = Popen("script -q -c \"./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit\" /dev/null", shell=True, bufsize=1, stdout=open("steam_log.txt", "wb"))
	while steam_download.poll() is None:
		#Terminate the process if bad login or password
		#steam_download.terminate()
		time.sleep(2)

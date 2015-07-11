#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, getpass, sys
from subprocess import call

user = sys.argv[1]
s_appid = sys.argv[2]
engineer_dir = sys.argv[3]
game_data_dir = sys.argv[4]

if os.path.isdir(engineer_dir) == False:
	os.makedirs(engineer_dir)
os.chdir(engineer_dir)
if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
	urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", engineer_dir + "steamcmd_linux.tar.gz")
	tar = tarfile.open(engineer_dir + "steamcmd_linux.tar.gz")
	tar.extractall()
	tar.close()
if os.path.isdir(game_data_dir) == False:
	password = getpass.getpass("Steam Password: ")
	s_download = call("./steamcmd.sh +@sSteamCmdForcePlatformType windows +login " + user + " " + password + " +force_install_dir " + game_data_dir + " +app_update " + s_appid + " validate +quit", shell=True)

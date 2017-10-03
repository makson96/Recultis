#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "Quake2/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Quake 2 on Yamagi Quake II engine"
description = """This will be description of Quake 2 game.






"""

shops = ["steam"]
s_appid = "2320"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/yquake2-screen.png"
icon1_name = "yquake2.png"
icon_list = [icon1_name]

launcher1_cmd = "bash -c 'cd $HOME/.recultis/Quake2; LD_LIBRARY_PATH=lib ./qauke2'"
launcher_cmd_list = [["Quake1", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Quake 2
Comment=Play Quake 2
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false"""
launcher_list = [["quake2.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	#Here is all game specific code
	print("Preparing game engine")
	for quake2_file_or_dir in os.listdir(recultis_dir + "tmp/yquake2"):
		if os.path.isfile(recultis_dir + "tmp/yquake2/" + quake2_file_or_dir):
			if os.path.isfile(install_dir + quake2_file_or_dir):
				os.remove(install_dir + quake2_file_or_dir)
			shutil.copy(recultis_dir + "tmp/yquake2/" + quake2_file_or_dir, install_dir + quake2_file_or_dir)
		if os.path.isdir(recultis_dir + "tmp/yquake2/" + quake2_file_or_dir) and quake2_file_or_dir != "baseq2":
			if os.path.isdir(install_dir + quake2_file_or_dir):
				shutil.rmtree(install_dir + quake2_file_or_dir)
			shutil.copytree(recultis_dir + "tmp/yquake2/" + quake2_file_or_dir, install_dir + quake2_file_or_dir)
	if os.path.isfile(install_dir + "baseq2/game.so"):
		os.remove(install_dir + "baseq2/game.so")
	shutil.copy(recultis_dir + "tmp/yquake2/baseq2/game.so", install_dir + "baseq2/game.so")
	print("Game engine ready")

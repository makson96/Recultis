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
description = """Quake II is the successor of great protagonist. It introduced better
graphic, new weapons, enemies and amazing multiplayer. The game is
great improvement to the original. It is first person shooter which was
most advanced game of its times. Original engine of the game was
open-sourced and is now developed under the project Yamagi Quake II.
Thanks to that we can all play this game with tons of improvements
and using modern technologies.
"""

shops = ["steam"]
s_appid = "2320"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/yquake2-screen.png"
icon1_name = "yquake2.png"
icon_list = [icon1_name]

runtime_version = "recultis1"
launcher1_cmd = "bash -c 'cd $HOME/.recultis/Quake2; LD_LIBRARY_PATH=lib ./quake2'"
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

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "AliensVsPredator/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Aliens vs Predator Classic 2000 on avp engine"
description = """Aliens vs Predator is revolutionary FPS, which combines the best of both
Aliens and Predator franchises. You can play as Colonial Marine, Alien or
Predator in great campaigns, single player skirmishes or in multiplayer.
Each species introduce completely different play-style - Colonial Marine
relies on guns; Alien who can run on walls, sneak and fast attack; and
Predator with, masking suit and hunting weapons.
Important shortcuts: ALT-ENTER for fullscreen; CTRL-G for mouse grab.
"""

shops = ["steam"]
s_appid = "3730"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/avp-screen.png"
icon_name="avp.png"

launcher1_cmd = "bash -c 'cd $HOME/.recultis/AliensVsPredator/; ./avp'"
launcher_cmd_list = [["Aliens vs Predator", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Aliens vs Predator Classic 2000
Comment=Play Aliens vs Predator Classic 2000
Exec=""" + launcher1_cmd + """
Icon=""" + icon_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["avp.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	print("Preparing game engine")
	#All content needs to be lowercase
	for avp_file_or_dir in os.listdir(install_dir):
		if os.path.isdir(install_dir + avp_file_or_dir) == True:
			print("entering dir " + avp_file_or_dir)
			for avp_file in os.listdir(install_dir + avp_file_or_dir):
				if avp_file != avp_file.lower():
					os.rename(install_dir + avp_file_or_dir + "/" + avp_file, install_dir + avp_file_or_dir + "/" + avp_file.lower())
		if avp_file_or_dir != avp_file_or_dir.lower():
			os.rename(install_dir + avp_file_or_dir, install_dir + avp_file_or_dir.lower())
	#Copy game engine and libs
	shutil.copy(recultis_dir + "tmp/avp/avp", install_dir + "avp")
	if os.path.isdir(install_dir + "lib/") == True:
		shutil.rmtree(install_dir + "lib/")
	shutil.copytree(recultis_dir + "tmp/avp/lib/", install_dir + "lib/", symlinks=True)
	print("Game engine ready")

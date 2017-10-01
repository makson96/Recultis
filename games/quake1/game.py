#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "Quake1/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Quake on darkplaces engine"
description = """This will be description of Quake game.






"""

shops = ["steam"]
s_appid = "2310"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/darkplaces-screen.png"
icon1_name = "darkplaces.png"
icon_list = [icon1_name]

launcher1_cmd = "bash -c 'cd $HOME/.recultis/Quake1; LD_LIBRARY_PATH=lib ./darkplaces-sdl -window'"
launcher_cmd_list = [["Quake1", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Quake
Comment=Play Quake
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false"""
launcher_list = [["quake1.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	#Here is all game specific code
	print("Preparing game engine")
	shutil.copy(recultis_dir + "tmp/darkplaces/darkplaces-sdl", install_dir + "darkplaces-sdl")
	shutil.copytree(recultis_dir + "tmp/darkplaces/lib", install_dir + "lib")
	if os.path.os.path.islink(install_dir + "id1") == False and os.path.isdir(install_dir + "id1") == False and os.path.isfile(install_dir + "id1") == False:
		if os.path.isdir(install_dir + "Id1") == True:
			os.symlink(install_dir + "Id1", install_dir + "id1")
	print("Game engine ready")

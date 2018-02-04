#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "JediOutcast/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Jedi Knight II: Jedi Outcast on OpenJK engine"
description = """Jedi Outcast is the third game from Star Wars Dark Forces series. In
this game you play as one of the heroes of New Republic. At the
beggining you use only conventional weapons, but as the game
evolves, you move to using force and the light saber. This game
is great TPP/FPP title for Star Wars fans. It can by played on Linux
thanks to OpenJO engine, which is developed by OpenJK Project. To
play this game you need to have it in your Steam library.
"""

shops = ["steam"]
s_appid = "6030"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/openjo-screen.png"
icon1_name = "openjk.png"
icon_list = [icon1_name]

engine = "openjk"
runtime_version = 2
env_var = "LD_LIBRARY_PATH=$HOME/.recultis/runtime/recultis" + str(runtime_version) + ":$HOME/.recultis/runtime/recultis" + str(runtime_version) + "/custom"
launcher1_cmd = "bash -c 'cd $HOME/.recultis/JediOutcast/GameData/; "+ env_var + " ./openjo_sp.x86_64'"
launcher_cmd_list = [["Jedi Outcast Single Player", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Jedi Knight II: Jedi Outcast
Comment=Play Jedi Knight II Outcast
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false"""
launcher_list = [["openjo_sp.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	#Here is all game specific code
	print("Preparing game engine")
	for binary in next(os.walk(recultis_dir + "tmp/JediOutcast/"))[2]:
		shutil.copy(recultis_dir + "tmp/JediOutcast/" + binary, install_dir + "GameData/" + binary)
	for directory in next(os.walk(recultis_dir + "tmp/JediOutcast/"))[1]:
		if os.path.isdir(install_dir + "GameData/" + directory) == False:
			os.makedirs(install_dir + "GameData/" + directory)
		for binary in next(os.walk(recultis_dir + "tmp/JediOutcast/" + directory))[2]:
			shutil.copy(os.path.join(recultis_dir, "tmp/JediOutcast/", directory, binary), os.path.join(install_dir, "GameData/", directory, binary))
	print("Game engine ready")

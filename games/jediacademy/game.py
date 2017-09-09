#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "JediAcademy/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Jedi Knight: Jedi Academy on OpenJK engine"
description = """Jedi Academy is fast and fun TPS set in Star Wars universe. Fight with
Lightsabers, train yourself in Lightside or Darkside of the force. Meet
your favorite characters from the original series and uncover the plot
of evil Empire. This great game was never released on Linux, but thanks
to the source code release, the engine is now developed in OpenJK
project. To run the game by Recultis, you need to have it in your Steam
Library.
"""

s_appid = "6020"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/openjk-screen.png"
icon_name = "openjk.png"

launcher1_cmd = "bash -c 'cd $HOME/.recultis/JediAcademy/GameData/; ./openjk_sp.x86_64'"
launcher2_cmd = "bash -c 'cd $HOME/.recultis/JediAcademy/GameData/; ./openjk.x86_64'"
launcher_cmd_list = [["Jedi Knight Single Player", launcher1_cmd], ["Jedi Knight Multi Player", launcher2_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Jedi Knight: Jedi Academy - SinglePlayer
Comment=Play Jedi Knights Academy
Exec=""" + launcher1_cmd + """
Icon=""" + icon_name + """
Categories=Game;
Terminal=false"""
launcher2_text = """[Desktop Entry]
Type=Application
Name=Jedi Knight: Jedi Academy - MultiPlayer
Comment=Play Jedi Knights Academy
Exec=""" + launcher2_cmd + """
Icon=""" + icon_name + """
Categories=Game;
Terminal=false"""
launcher_list = [["openjk_sp.desktop", launcher1_text], ["openjk_mp.desktop", launcher2_text]]

uninstall_files_list = []
uninstall_dir_list = []
#Legacy code for Recultis 1.1
uninstall_files_legacy = [desk_dir + "openjk_amd64_sp.desktop", desk_dir + "openjk_amd64_mp.desktop",
os.getenv("HOME") + "/.local/share/applications/openjk_amd64_sp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_mp.desktop"]
uninstall_files_list.extend(uninstall_files_legacy)
#End of legacy code

def prepare_engine():
	#Here is all game specific code
	print("Preparing game engine")
	for binary in next(os.walk(recultis_dir + "tmp/JediAcademy/"))[2]:
		shutil.copy(recultis_dir + "tmp/JediAcademy/" + binary, install_dir + "GameData/" + binary)
	for directory in next(os.walk(recultis_dir + "tmp/JediAcademy/"))[1]:
		if directory == "lib":
			if os.path.isdir(install_dir + "GameData/" + directory):
				shutil.rmtree(install_dir + "GameData/" + directory)
			shutil.copytree(recultis_dir + "tmp/JediAcademy/" + directory, install_dir + "GameData/" + directory, symlinks=True)
		else:
			if os.path.isdir(install_dir + "GameData/" + directory) == False:
				os.makedirs(install_dir + "GameData/" + directory)
			for binary in next(os.walk(recultis_dir + "tmp/JediAcademy/" + directory))[2]:
				shutil.copy(os.path.join(recultis_dir, "tmp/JediAcademy/", directory, binary), os.path.join(install_dir, "GameData/", directory, binary))
	print("Game engine ready")

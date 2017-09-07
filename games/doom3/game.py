#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "doom3/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

full_name = "Doom 3 BFG on RBDOOM-3-BFG engine"
description = """Doom 3: BFG is the remaster of classic Doom 3 with all expansions. It
features enhanced graphic and audio to original game. Doom 3 is one of
the best FPS games of all time. Unfortunately, it was never released
on Linux, but game engine was release open source. With many
enhancements and new features, game is now available on Linux and it
is better than ever before. Recultis uses RBDOOM-3-BFG flavor of the
engine and requires game to be present in your Steam Library.
"""

s_appid = "208200"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/rbdoom3-screen.png"
icon_name = "rbdoom-3-bfg.png"

launcher1_cmd = "bash -c 'cd $HOME/.recultis/doom3/; ./RBDoom3BFG'"
launcher_cmd_list = [["Doom3 BFG", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Doom 3 BFG
Comment=Play Doom 3 BFG
Exec=""" + launcher1_cmd + """
Icon=""" + icon_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["doom3.desktop", launcher1_text]]

uninstall_files_list = [os.getenv("HOME") + "/.local/share/icons/" + icon_name]
for launch_file in launcher_list:
	uninstall_files_list.append(desk_dir + launch_file[0])
	uninstall_files_list.append(os.getenv("HOME") + "/.local/share/applications/" + launch_file[0])
uninstall_dir_list = [install_dir]

def prepare_engine():
	print("prepare engine")
	try:
		os.remove(install_dir + "RBDoom3BFG")
		shutil.rmtree(install_dir + "lib")
	except:
		pass
	shutil.copy(recultis_dir + "tmp/rbdoom-3-bfg/RBDoom3BFG", install_dir + "RBDoom3BFG")
	shutil.copytree(recultis_dir + "tmp/rbdoom-3-bfg/lib", install_dir + "lib", symlinks=True)

def info(requested_list):
	if os.path.isfile(install_dir + "/version_link.txt"):
		version_file = open(install_dir + "/version_link.txt")
		version = version_file.read()
	else:
		version = "No proper install"
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	deb_file_path = recultis_dir + "tmp/doom3.deb"
	return_list = []
	for requested_item in requested_list:
		if requested_item == "deb_file_path":
			return_list.append(deb_file_path)
		elif requested_item == "deb_url_path":
			return_list.append(link)
		elif requested_item == "install_dir":
			return_list.append(install_dir)
		elif requested_item == "version":
			return_list.append(version)
	return return_list

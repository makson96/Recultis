#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "xcom/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

full_name = "X-COM: UFO Defense on OpenXcom engine"
description = """X-COM: UFO Defense is legendary game in which you lead X-COM
organization establish to fight against alien invasion. You need to arm and
prepare your soldiers to fight with the enemy from the stars, gain their
technology and use it against them. Fight on the battlefields, research
new technologies, interact with words political affairs. This game is deep
and multidimensional strategy.

"""

s_appid = "7760"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/openxcom-screen.png"
icon_name = "openxcom.png"

launcher1_cmd = "bash -c 'cd $HOME/.recultis/xcom/share/openxcom; ../../bin/openxcom'"
launcher_cmd_list = [["X-COM UFO Defense", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=X-COM: UFO Defense
Comment=Play X-COM: UFO Defense
Exec=""" + launcher1_cmd + """
Icon=""" + icon_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["openxcom.desktop", launcher1_text]]

uninstall_files_list = [os.getenv("HOME") + "/.local/share/icons/" + icon_name]
for launch_file in launcher_list:
	uninstall_files_list.append(desk_dir + launch_file[0])
	uninstall_files_list.append(os.getenv("HOME") + "/.local/share/applications/" + launch_file[0])
uninstall_dir_list = [install_dir]


def prepare_engine():
	print("prepare engine")
	if os.path.isdir(install_dir + "bin") == True:
		shutil.rmtree(install_dir + "bin")
	shutil.copytree(recultis_dir + "tmp/openxcom/bin", install_dir + "bin/", symlinks=True)
	if os.path.isdir(install_dir + "lib/") == True:
		shutil.rmtree(install_dir + "lib/")
	shutil.copytree(recultis_dir + "tmp/openxcom/lib/", install_dir + "lib/", symlinks=True)
	if os.path.isdir(install_dir + "share/") == True:
		shutil.rmtree(install_dir + "share/")
	shutil.copytree(recultis_dir + "tmp/openxcom/share/", install_dir + "share/", symlinks=True)
	local_data_dir = os.getenv("HOME") + "/.local/share/openxcom/UFO/"
	if os.path.isdir(local_data_dir) == False:
		os.makedirs(local_data_dir)
	print("symlinking game data to xcom local data")
	dirs = ["GEODATA", "GEOGRAPH", "MAPS", "ROUTES", "SOUND", "TERRAIN", "UFOGRAPH", "UFOINTRO", "UNITS"]
	for xdir in dirs:
		if os.path.islink(local_data_dir + xdir):
			os.unlink(local_data_dir + xdir)
		elif os.path.isfile(local_data_dir + xdir):
			os.remove(local_data_dir + xdir)
		elif os.path.isdir(local_data_dir + xdir):
			shutil.rmtree(local_data_dir + xdir)
		os.symlink(install_dir + "XCOM/" + xdir, local_data_dir + xdir)

def info(requested_list):
	if os.path.isfile(install_dir + "/version_link.txt"):
		version_file = open(install_dir + "/version_link.txt")
		version = version_file.read()
	else:
		version = "No proper install"
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	deb_file_path = recultis_dir + "tmp/xcomufodefense.deb"
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

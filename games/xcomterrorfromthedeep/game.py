#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "xcom2/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

full_name = "X-COM: Terror From the Deep"
description = """X-COM: Terror From the Deep is the second game from X-COM franchise.
This time aliens pose a threat from the oceans. Once again you have
to lead your soldiers int to the battle. Prepare their equipment and
vehicles. Build base, research technology, fight back aliens. This
game is complicated strategy. One of the best of its times. It runs on
OpenXcom engine and requires you to own the game in your Steam
library.
"""

shops = ["steam"]
s_appid = "7650"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/openxcom2-screen.png"
icon1_name = "openxcom.png"
icon_list = [icon1_name]

engine = "openxcom"
runtime_version = 2
env_var = "LD_LIBRARY_PATH=$HOME/.recultis/runtime/recultis" + str(runtime_version) + ":$HOME/.recultis/runtime/recultis" + str(runtime_version) + "/custom"
launcher1_cmd = "bash -c 'cd $HOME/.recultis/xcom2/share/openxcom; " + env_var + " ../../bin/openxcom -cfg .'"
launcher_cmd_list = [["X-COM: Terror From the Deep", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=X-COM: Terror From the Deep
Comment=Play X-COM: Terror From the Deep
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["openxcom2.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = [os.getenv("HOME") + "/.local/share/openxcom/TFTD"]

def prepare_engine():
	print("Preparing game engine")
	if os.path.isdir(install_dir + "bin") == True:
		shutil.rmtree(install_dir + "bin")
	shutil.copytree(recultis_dir + "tmp/openxcom/bin", install_dir + "bin/", symlinks=True)
	if os.path.isdir(install_dir + "share/") == True:
		shutil.rmtree(install_dir + "share/")
	shutil.copytree(recultis_dir + "tmp/openxcom/share/", install_dir + "share/", symlinks=True)
	shutil.copy(self_dir + "options.cfg", install_dir + "share/openxcom/options.cfg")
	local_data_dir = os.getenv("HOME") + "/.local/share/openxcom/TFTD/"
	if os.path.isdir(local_data_dir) == False:
		os.makedirs(local_data_dir)
	print("symlinking game data to xcom local data")
	dirs = ["ANIMS", "FLOP_INT", "GEODATA", "GEOGRAPH", "MAPS", "ROUTES", "SOUND", "TERRAIN", "UFOGRAPH", "UNITS"]
	for xdir in dirs:
		if os.path.islink(local_data_dir + xdir):
			os.unlink(local_data_dir + xdir)
		elif os.path.isfile(local_data_dir + xdir):
			os.remove(local_data_dir + xdir)
		elif os.path.isdir(local_data_dir + xdir):
			shutil.rmtree(local_data_dir + xdir)
		os.symlink(install_dir + "TFD/" + xdir, local_data_dir + xdir)
	print("Game engine ready")

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "morrowind/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

full_name = "The Elder Scrolls III: Morrowind on OpenMW engine"
description = """Morrowind is revolutionary RPG. With open world, endless possibilities
and interesting story. What is more, it has well done 3D art and
feature great character development. Morrowind was never released
on Linux. Fortunately team of developers are working hard on
OpenMW project to provide us drop in replacement for original
Morrowind engine with tons of new features. To run this game you
need to have it in your Steam Library.
"""

shops = ["steam"]
s_appid = "22320"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/openmw-screen.png"
icon1_name = "openmw.png"
icon_list = [icon1_name]

launcher1_cmd = "bash -c 'cd $HOME/.recultis/morrowind/bin/; OSG_LIBRARY_PATH=$HOME/.recultis/morrowind/lib/osgPlugins-3.4.0 ./openmw'"
launcher_cmd_list = [["Morrowind", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=The Elder Scrolls III: Morrowind
Comment=Play The Elder Scrolls III: Morrowind
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["morrowind.desktop", launcher1_text]]

uninstall_files_list = [os.getenv("HOME") + "/.config/openmw/openmw.cfg"]
uninstall_dir_list = []

def prepare_engine():
	print("Preparing game engine")
	for directory in next(os.walk(recultis_dir + "tmp/openmw-makson/"))[1]:
		try:
			shutil.rmtree(install_dir + directory)
		except:
			pass
		shutil.copytree(recultis_dir + "tmp/openmw-makson/" + directory, install_dir + directory, symlinks=True)
	print("copy config")
	if os.path.isdir(os.getenv("HOME") + "/.config/openmw/") == False:
		os.makedirs(os.getenv("HOME") + "/.config/openmw/")
	if os.path.isfile(os.getenv("HOME") + "/.config/openmw/openmw.cfg") == False:
		shutil.copy(self_dir + "openmw.cfg", os.getenv("HOME") + "/.config/openmw/openmw.cfg")
		openmw_cfg=open(os.getenv("HOME") + "/.config/openmw/openmw.cfg", "a")
		openmw_cfg.write('\ndata="' + install_dir + 'Data Files"')
		openmw_cfg.close()
	print("Game engine ready")

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "OpenRA/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Command and Conquer: Red Alert on OpenRA"
description = """This will be Red Alert description.






"""

shops = ["none"]
steam_link =  "non_needed"
screenshot_path = self_dir + "../../assets/html/openra-ra-screen.png"
icon_name="openra-ra.png"

launcher1_cmd = "bash -c 'cd $HOME/.recultis/OpenRA/; LD_LIBRARY_PATH=lib MONO_PATH=lib/4.5 lib/mono-sgen OpenRA.Game.exe Game.Mod=ra'"
launcher_cmd_list = [["Red Alert", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Command & Conquer: Red Alert on OpenRA
Comment=Play Command & Conquer: Red Alert on OpenRA
Exec=""" + launcher1_cmd + """
Icon=""" + icon_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["openra-ra.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	print("Preparing game engine")
	#Copy game engine and libs
	shutil.rmtree(install_dir)
	shutil.copytree(recultis_dir + "tmp/openra/", install_dir, symlinks=True)
	print("Game engine ready")

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

shops = ["steam"]
s_appid = "208200"
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../../assets/html/rbdoom3-screen.png"
icon1_name = "rbdoom-3-bfg.png"
icon_list = [icon1_name]

runtime_version = 2
env_var = "LD_LIBRARY_PATH=$HOME/.recultis/runtime/recultis" + str(runtime_version) + ":$HOME/.recultis/runtime/recultis" + str(runtime_version) + "/custom"
launcher1_cmd = "bash -c 'cd $HOME/.recultis/doom3/; " + env_var + " ./RBDoom3BFG'"
launcher_cmd_list = [["Doom3 BFG", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Doom 3 BFG
Comment=Play Doom 3 BFG
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["doom3.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	print("Prepare game engine")
	try:
		os.remove(install_dir + "RBDoom3BFG")
		shutil.rmtree(install_dir + "lib")
	except:
		pass
	shutil.copy(recultis_dir + "tmp/rbdoom-3-bfg/RBDoom3BFG", install_dir + "RBDoom3BFG")
	shutil.copytree(recultis_dir + "tmp/rbdoom-3-bfg/lib", install_dir + "lib", symlinks=True)
	print("Game engine ready")

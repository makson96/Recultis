#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output, call

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
install_dir = recultis_dir + "Heroes3/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

full_name = "Heroes III Complete on VCMI engine"
description = """Heroes of Might and Magic III Complete is one of the best turn
based strategy in the history of computer games. You develop your
castle, recruit soldiers who moves with your hero, engage in battles
and discover new land. All of this is set in rich fantasy world with
beautiful graphic. This game can be played natively on Linux thanks
to VCMI game engine. In order to play it, you need to have it in your
GOG library.
"""

shops = ["gog"]
s_appid = "heroes_of_might_and_magic_3_complete_edition"
gog_link =  "https://www.gog.com/game/heroes_of_might_and_magic_3_complete_edition"
screenshot_path = self_dir + "../../assets/html/vcmi-screen.png"
icon1_name="vcmi.png"
icon_list = [icon1_name]

engine = "vcmi"
runtime_version = 2
env_var = "LD_LIBRARY_PATH=$HOME/.recultis/runtime/recultis" + str(runtime_version) + ":$HOME/.recultis/runtime/recultis" + str(runtime_version) + "/custom"
launcher1_cmd = "bash -c 'cd $HOME/.recultis/Heroes3; "+ env_var + " ./vcmiclient'"
launcher_cmd_list = [["Heroes III", launcher1_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Heroes III Complete
Comment=Play Heroes III Complete
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false"""

launcher_list = [["vcmi.desktop", launcher1_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	print("Preparing game engine")
	for vcmi_file_or_dir in os.listdir(recultis_dir + "tmp/vcmi/"):
		if os.path.isdir(install_dir + vcmi_file_or_dir):
			shutil.rmtree(install_dir + vcmi_file_or_dir)
		os.rename(recultis_dir + "tmp/vcmi/" + vcmi_file_or_dir, install_dir + vcmi_file_or_dir)
	call(env_var + " " + install_dir + "vcmibuilder --data " + install_dir + "app", shell=True)
	print("Game engine ready")

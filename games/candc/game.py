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

full_name = "Command and Conquer on OpenRA"
description = """Classic Command and Conquer games are
one of the best real time strategies
in the history. OpenRA game engine allows you to
play following titles from the franchise:
Tiberian Dawn, Red Alert, Dune 2000,
Tiberian Sun (pre-alpha).

"""

shops = ["none"]
screenshot_path = self_dir + "../../assets/html/openra-ra-screen.png"
icon1_name="openra-cnc.png"
icon2_name="openra-ra.png"
icon3_name="openra-d2k.png"
icon4_name="openra-ts.png"
icon_list = [icon1_name, icon2_name, icon3_name, icon4_name]

launcher1_cmd = "bash -c 'cd $HOME/.recultis/OpenRA/; LD_LIBRARY_PATH=lib MONO_PATH=lib/4.5 lib/mono-sgen OpenRA.Game.exe Game.Mod=cnc'"
launcher2_cmd = "bash -c 'cd $HOME/.recultis/OpenRA/; LD_LIBRARY_PATH=lib MONO_PATH=lib/4.5 lib/mono-sgen OpenRA.Game.exe Game.Mod=ra'"
launcher3_cmd = "bash -c 'cd $HOME/.recultis/OpenRA/; LD_LIBRARY_PATH=lib MONO_PATH=lib/4.5 lib/mono-sgen OpenRA.Game.exe Game.Mod=d2k'"
launcher4_cmd = "bash -c 'cd $HOME/.recultis/OpenRA/; LD_LIBRARY_PATH=lib MONO_PATH=lib/4.5 lib/mono-sgen OpenRA.Game.exe Game.Mod=ts'"
launcher_cmd_list = [["Command and Conquer: Tiberian Dawn", launcher1_cmd], ["Command and Conquer: Red Alert", launcher2_cmd], ["Dune 2000", launcher3_cmd], ["Command and Conquer: Tiberian Sun (pre-alpha)", launcher4_cmd]]
launcher1_text = """[Desktop Entry]
Type=Application
Name=Command & Conquer: Tiberian Dawn on OpenRA
Comment=Play Command & Conquer: Tiberian Dawn on OpenRA
Exec=""" + launcher1_cmd + """
Icon=""" + icon1_name + """
Categories=Game;
Terminal=false
"""
launcher2_text = """[Desktop Entry]
Type=Application
Name=Command & Conquer: Red Alert on OpenRA
Comment=Play Command & Conquer: Red Alert on OpenRA
Exec=""" + launcher2_cmd + """
Icon=""" + icon2_name + """
Categories=Game;
Terminal=false
"""
launcher3_text = """[Desktop Entry]
Type=Application
Name=Dune 2000 on OpenRA
Comment=Play Dune 2000 on OpenRA
Exec=""" + launcher3_cmd + """
Icon=""" + icon3_name + """
Categories=Game;
Terminal=false
"""
launcher4_text = """[Desktop Entry]
Type=Application
Name=Command & Conquer: Tiberian Sun on OpenRA (pre-alpha)
Comment=Play Command & Conquer: Tiberian Sun on OpenRA (pre-alpha)
Exec=""" + launcher4_cmd + """
Icon=""" + icon4_name + """
Categories=Game;
Terminal=false
"""
launcher_list = [["openra-cnc.desktop", launcher1_text], ["openra-ra.desktop", launcher2_text], ["openra-d2k.desktop", launcher3_text], ["openra-ts.desktop", launcher4_text]]

uninstall_files_list = []
uninstall_dir_list = []

def prepare_engine():
	print("Preparing game engine")
	#Copy game engine and libs
	shutil.rmtree(install_dir)
	shutil.copytree(recultis_dir + "tmp/openra/", install_dir, symlinks=True)
	print("Game engine ready")

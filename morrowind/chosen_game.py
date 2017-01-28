#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

from free_engineer import engineer_dir
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = engineer_dir + "morrowind/"
s_appid = "22320"

def prepare_engine():
	print("prepare engine")
	for directory in next(os.walk(engineer_dir + "tmp/openmw-makson/"))[1]:
		try:
			shutil.rmtree(game_dir + directory)
		except:
			pass
		shutil.copytree(engineer_dir + "tmp/openmw-makson/" + directory, game_dir + directory, symlinks=True)
	shutil.rmtree(engineer_dir + "tmp")
	print("copy_config")
	if os.path.isdir(os.getenv("HOME") + "/.config/openmw/") == False:
		os.makedirs(os.getenv("HOME") + "/.config/openmw/")
	if os.path.isfile(os.getenv("HOME") + "/.config/openmw/openmw.cfg") == False:
		shutil.copy(self_dir + "openmw.cfg", os.getenv("HOME") + "/.config/openmw/openmw.cfg")
		openmw_cfg=open(os.getenv("HOME") + "/.config/openmw/openmw.cfg", "a")
		openmw_cfg.write('\ndata="' + game_dir + 'Data Files"')
		openmw_cfg.close()

def start_steam(user):
	print(user)
	steamcmd = call("x-terminal-emulator -e 'python3 " + self_dir + "tools/steam.py " + user + " " + s_appid + " " + engineer_dir + " " + game_dir + "'", shell=True)
	while os.path.isdir(game_dir + "Data Files/") == False:
		time.sleep(2)

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.icons") == False:
		os.makedirs(os.getenv("HOME") + "/.icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "openmw.png", os.getenv("HOME") + "/.icons/openmw.png")
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "morrowind.desktop", desk_dir + "/morrowind.desktop")
	shutil.copy(self_dir + "morrowind.desktop", os.getenv("HOME") + "/.local/share/applications/morrowind.desktop")

def start():
	game_dir = engineer_dir + "morrowind/"
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	if os.path.isdir(engineer_dir + "tmp") == False:
		os.makedirs(engineer_dir + "tmp")
	else:
		shutil.rmtree(engineer_dir + "tmp")
		os.makedirs(engineer_dir + "tmp")
	from tools import download_engine
	result = download_engine.download(link, engineer_dir + "tmp/openmw-makson.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(engineer_dir + "tmp/", "openmw-makson.deb")
	prepare_engine()
	start_steam(str("login text"))
	launchers()

def info():
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	deb_file_path = engineer_dir + "tmp/openmw-makson.deb"
	return deb_file_path, link

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = recultis_dir + "morrowind/"
s_appid = "22320"

name = "The Elder Scrolls III: Morrowind on OpenMW engine"
description = """Morrowind is revolutionary RPG. With open world, endless possibilities
and interesting story. What is more, it has well done 3D art and
feature great character development. Morrowind was never released
on Linux. Fortunately team of developers are working hard on
OpenMW project to provide us drop in replacement for original
Morrowind engine with tons of new features. To run this game you
need to have it in your Steam Library.
"""
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../assets/html/openmw-screen.png"

def prepare_engine():
	print("prepare engine")
	for directory in next(os.walk(recultis_dir + "tmp/openmw-makson/"))[1]:
		try:
			shutil.rmtree(game_dir + directory)
		except:
			pass
		shutil.copytree(recultis_dir + "tmp/openmw-makson/" + directory, game_dir + directory, symlinks=True)
	print("copy config")
	if os.path.isdir(os.getenv("HOME") + "/.config/openmw/") == False:
		os.makedirs(os.getenv("HOME") + "/.config/openmw/")
	if os.path.isfile(os.getenv("HOME") + "/.config/openmw/openmw.cfg") == False:
		shutil.copy(self_dir + "openmw.cfg", os.getenv("HOME") + "/.config/openmw/openmw.cfg")
		openmw_cfg=open(os.getenv("HOME") + "/.config/openmw/openmw.cfg", "a")
		openmw_cfg.write('\ndata="' + game_dir + 'Data Files"')
		openmw_cfg.close()

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "openmw.png", os.getenv("HOME") + "/.local/share/icons/openmw.png")
	print("make launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "morrowind.desktop", desk_dir + "/morrowind.desktop")
	shutil.copy(self_dir + "morrowind.desktop", os.getenv("HOME") + "/.local/share/applications/morrowind.desktop")

def start(shop, shop_login, shop_password):
	print("start install openmw")
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	if os.path.isdir(recultis_dir + "tmp") == False:
		os.makedirs(recultis_dir + "tmp")
	else:
		shutil.rmtree(recultis_dir + "tmp")
		os.makedirs(recultis_dir + "tmp")
	open(recultis_dir + "tmp/openmw-makson.deb", 'a').close()
	if shop == "steam":
		from tools import steam
		print("start steam")
		steam.start(shop_login, shop_password, recultis_dir, s_appid, game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	print("download game engine")
	from tools import download_engine
	result = download_engine.download(link, recultis_dir + "tmp/openmw-makson.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "openmw-makson.deb")
	prepare_engine()
	launchers()
	#Mark installed version by coping link file
	shutil.copy(self_dir + "link.txt", game_dir + "/version_link.txt")
	shutil.rmtree(recultis_dir + "tmp")

def info(requested_list):
	if os.path.isfile(game_dir + "/version_link.txt"):
		version_file = open(game_dir + "/version_link.txt")
		version = version_file.read()
	else:
		version = "Update needed or no intall"
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	deb_file_path = recultis_dir + "tmp/openmw-makson.deb"
	return_list = []
	for requested_item in requested_list:
		if requested_item == "deb_file_path":
			return_list.append(deb_file_path)
		elif requested_item == "deb_url_path":
			return_list.append(link)
		elif requested_item == "game_dir":
			return_list.append(game_dir)
		elif requested_item == "version":
			return_list.append(version)
	return return_list

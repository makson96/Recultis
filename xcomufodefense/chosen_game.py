#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = recultis_dir + "xcom/"
s_appid = "7760"

name = "X-COM: UFO Defense on OpenXcom engine"
description = """X-COM: UFO Defense is legendary game in which you lead X-COM
organization establish to fight against alien invasion. You need to arm and
prepare your soldiers to fight with the enemy from the stars, gain their
technology and use it against them. Fight on the battlefields, research
new technologies, interact with words political affairs. This game is deep
and multidimensional strategy.

"""
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../assets/html/openxcom-screen.png"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

def prepare_engine():
	print("prepare engine")
	if os.path.isdir(game_dir + "bin") == True:
		shutil.rmtree(game_dir + "bin")
	shutil.copytree(recultis_dir + "tmp/openxcom/bin", game_dir + "bin/", symlinks=True)
	if os.path.isdir(game_dir + "lib/") == True:
		shutil.rmtree(game_dir + "lib/")
	shutil.copytree(recultis_dir + "tmp/openxcom/lib/", game_dir + "lib/", symlinks=True)
	if os.path.isdir(game_dir + "share/") == True:
		shutil.rmtree(game_dir + "share/")
	shutil.copytree(recultis_dir + "tmp/openxcom/share/", game_dir + "share/", symlinks=True)
	local_data_dir = os.getenv("HOME") + "/.local/share/openxcom/data/"
	if os.path.isdir(local_data_dir) == False:
		os.makedirs(local_data_dir)
	print("symlinking game data to xcom local data")
	dirs = ["GEODATA", "GEOGRAPH", "MAPS", "ROUTES", "SOUND", "TERRAIN", "UFOGRAPH", "UFOINTRO", "UNITS"]
	for xdir in dirs:
		if os.path.exists(local_data_dir + xdir) == False:
			os.symlink(game_dir + "XCOM/" + xdir, local_data_dir + xdir)
	dirs = ["Language", "Resources", "Ruleset", "Shaders", "SoldierName"]
	for xdir in dirs:
		if os.path.exists(local_data_dir + xdir) == False:
			os.symlink(game_dir + "/share/openxcom/data/" + xdir, local_data_dir + xdir)
	dirs = ["MAPS/FIRES.MAP", "MAPS/INTERC.MAP", "ROUTES/FIRES.RMP", "ROUTES/INTERC.RMP"]
	for xdir in dirs:
		if os.path.exists(game_dir + "XCOM/" + xdir) == False:
			os.symlink(game_dir + "/share/openxcom/data/" + xdir, game_dir + "XCOM/" + xdir)

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "openxcom.png", os.getenv("HOME") + "/.local/share/icons/openxcom.png")
	print("make_launchers")
	shutil.copy(self_dir + "openxcom.desktop", desk_dir + "/openxcom.desktop")
	shutil.copy(self_dir + "openxcom.desktop", os.getenv("HOME") + "/.local/share/applications/openxcom.desktop")

def start(shop, shop_login, shop_password):
	print("start install openxcom")
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	if os.path.isdir(recultis_dir + "tmp") == False:
		os.makedirs(recultis_dir + "tmp")
	else:
		shutil.rmtree(recultis_dir + "tmp")
		os.makedirs(recultis_dir + "tmp")
	open(recultis_dir + "tmp/openxcom.deb", 'a').close()
	if shop == "steam":
		from tools import steam
		print("start steam")
		steam.start(shop_login, shop_password, recultis_dir, s_appid, game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	print("download game engine")
	from tools import download_engine
	result = download_engine.download(link, recultis_dir + "tmp/openxcom.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "openxcom.deb")
	prepare_engine()
	launchers()
	#Mark installed version by coping link file
	shutil.copy(self_dir + "link.txt", game_dir + "/version_link.txt")
	shutil.rmtree(recultis_dir + "tmp")

def uninstall():
	if os.path.isfile(desk_dir + "/openxcom.desktop"):
		os.remove(desk_dir + "/openxcom.desktop")
	if os.path.isfile(os.getenv("HOME") + "/.local/share/applications/openxcom.desktop"):
		os.remove(os.getenv("HOME") + "/.local/share/applications/openxcom.desktop")
	if os.path.isfile(os.getenv("HOME") + "/.local/share/icons/openxcom.png"):
		os.remove(os.getenv("HOME") + "/.local/share/icons/openxcom.png")
	if os.path.isdir(game_dir):
		shutil.rmtree(game_dir)

def info(requested_list):
	if os.path.isfile(game_dir + "/version_link.txt"):
		version_file = open(game_dir + "/version_link.txt")
		version = version_file.read()
	else:
		version = "Update needed or no intall"
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	deb_file_path = recultis_dir + "tmp/openxcom.deb"
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

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = recultis_dir + "AliensVsPredator/"
s_appid = "3730"

name = "Aliens vs Predator Classic 2000 on avp engine"
description = """Aliens vs Predator is revolutionary FPS, which combines the best of both
Aliens and Predator franchises. You can play as Colonial Marine, Alien or
Predator in great campaigns, single player skirmishes or in multiplayer.
Each species introduce completely different play-style - Colonial Marine
relies on guns; Alien who can run on walls, sneak and fast attack; and
Predator with, masking suit and hunting weapons.
Important shortcuts: ALT-ENTER for fullscreen; CTRL-G for mouse grab.
"""
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../assets/html/avp-screen.png"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

def prepare_engine():
	print("prepare engine")
	#All content needs to be lowercase
	for avp_file_or_dir in os.listdir(game_dir):
		if os.path.isdir(game_dir + avp_file_or_dir) == True:
			print("entering dir " + avp_file_or_dir)
			for avp_file in os.listdir(game_dir + avp_file_or_dir):
				os.rename(game_dir + avp_file_or_dir + "/" + avp_file, game_dir + avp_file_or_dir + "/" + avp_file.lower())
		if os.path.isdir(game_dir + avp_file_or_dir.lower()):
			shutil.rmtree(game_dir + avp_file_or_dir.lower())
		os.rename(game_dir + avp_file_or_dir, game_dir + avp_file_or_dir.lower())
	#Copy game engine and libs
	shutil.copy(recultis_dir + "tmp/avp/avp", game_dir + "avp")
	if os.path.isdir(game_dir + "lib/") == True:
		shutil.rmtree(game_dir + "lib/")
	shutil.copytree(recultis_dir + "tmp/avp/lib/", game_dir + "lib/", symlinks=True)

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "avp.png", os.getenv("HOME") + "/.local/share/icons/avp.png")
	print("make_launchers")
	shutil.copy(self_dir + "avp.desktop", desk_dir + "/avp.desktop")
	shutil.copy(self_dir + "avp.desktop", os.getenv("HOME") + "/.local/share/applications/avp.desktop")

def start(shop, shop_login, shop_password):
	print("start install avp")
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	if os.path.isdir(recultis_dir + "tmp") == False:
		os.makedirs(recultis_dir + "tmp")
	else:
		shutil.rmtree(recultis_dir + "tmp")
		os.makedirs(recultis_dir + "tmp")
	open(recultis_dir + "tmp/avp.deb", 'a').close()
	if shop == "steam":
		from tools import steam
		print("start steam")
		steam.start(shop_login, shop_password, recultis_dir, s_appid, game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	print("download game engine")
	from tools import download_engine
	result = download_engine.download(link, recultis_dir + "tmp/avp.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "avp.deb")
	prepare_engine()
	launchers()
	#Mark installed version by coping link file
	shutil.copy(self_dir + "link.txt", game_dir + "/version_link.txt")
	shutil.rmtree(recultis_dir + "tmp")

def uninstall():
	if os.path.isfile(desk_dir + "/avp.desktop"):
		os.remove(desk_dir + "/avp.desktop")
	if os.path.isfile(os.getenv("HOME") + "/.local/share/applications/avp.desktop"):
		os.remove(os.getenv("HOME") + "/.local/share/applications/avp.desktop")
	if os.path.isfile(os.getenv("HOME") + "/.local/share/icons/avp.png"):
		os.remove(os.getenv("HOME") + "/.local/share/icons/avp.png")
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
	deb_file_path = recultis_dir + "tmp/avp.deb"
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

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = engineer_dir + "doom3/"
s_appid = "208200"

def prepare_engine():
	print("prepare engine")
	try:
		os.remove(game_dir + "RBDoom3BFG")
		shutil.rmtree(game_dir + "lib")
	except:
		pass
	shutil.copy(engineer_dir + "tmp/rbdoom-3-bfg/RBDoom3BFG", game_dir + "RBDoom3BFG")
	shutil.copytree(engineer_dir + "tmp/rbdoom-3-bfg/lib", game_dir + "lib", symlinks=True)
	shutil.rmtree(engineer_dir + "tmp")

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.icons") == False:
		os.makedirs(os.getenv("HOME") + "/.icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "rbdoom-3-bfg.png", os.getenv("HOME") + "/.icons/rbdoom-3-bfg.png")
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "doom3.desktop", desk_dir + "/doom3.desktop")
	shutil.copy(self_dir + "doom3.desktop", os.getenv("HOME") + "/.local/share/applications/doom3.desktop")

def start(shop, shop_login, shop_password):
	print("start install rbdoom-3-bfg")
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	if os.path.isdir(engineer_dir + "tmp") == False:
		os.makedirs(engineer_dir + "tmp")
	else:
		shutil.rmtree(engineer_dir + "tmp")
		os.makedirs(engineer_dir + "tmp")
	print("download game engine")
	from tools import download_engine
	result = download_engine.download(link, engineer_dir + "tmp/rbdoom-3-bfg.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(engineer_dir + "tmp/", "rbdoom-3-bfg.deb")
	prepare_engine()
	if shop == "steam":
		from tools import steam
		print("start steam")
		steam.start(shop_login, shop_password, engineer_dir, s_appid, game_dir)
	launchers()
	#Mark installed version by coping link file
	shutil.copy(self_dir + "link.txt", game_dir + "/version_link.txt")

def info(requested_list):
	if os.path.isfile(game_dir + "/version_link.txt"):
		version_file = open(game_dir + "/version_link.txt")
		version = version_file.read()
	else:
		version = "Update needed or no intall"
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	deb_file_path = engineer_dir + "tmp/rbdoom-3-bfg.deb"
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

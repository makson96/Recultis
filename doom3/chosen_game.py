#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = recultis_dir + "doom3/"
s_appid = "208200"

name = "Doom 3 BFG on RBDOOM-3-BFG engine"
description = """Doom 3: BFG is the remaster of classic Doom 3 with all expansions. It
features enhanced graphic and audio to original game. Doom 3 is one of
the best FPS games of all time. Unfortunately, it was never released
on Linux, but game engine was release open source. With many
enhancements and new features, game is now available on Linux and it
is better than ever before. Recultis uses RBDOOM-3-BFG flavor of the
engine and requires game to be present in your Steam Library.
"""
steam_link =  "http://store.steampowered.com/app/"+s_appid+"/"
screenshot_path = self_dir + "../assets/html/rdoom3-screen.png"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]

def prepare_engine():
	print("prepare engine")
	try:
		os.remove(game_dir + "RBDoom3BFG")
		shutil.rmtree(game_dir + "lib")
	except:
		pass
	shutil.copy(recultis_dir + "tmp/rbdoom-3-bfg/RBDoom3BFG", game_dir + "RBDoom3BFG")
	shutil.copytree(recultis_dir + "tmp/rbdoom-3-bfg/lib", game_dir + "lib", symlinks=True)

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "rbdoom-3-bfg.png", os.getenv("HOME") + "/.local/share/icons/rbdoom-3-bfg.png")
	print("make_launchers")
	shutil.copy(self_dir + "doom3.desktop", desk_dir + "/doom3.desktop")
	shutil.copy(self_dir + "doom3.desktop", os.getenv("HOME") + "/.local/share/applications/doom3.desktop")

def start(shop, shop_login, shop_password):
	print("start install rbdoom-3-bfg")
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	if os.path.isdir(recultis_dir + "tmp") == False:
		os.makedirs(recultis_dir + "tmp")
	else:
		shutil.rmtree(recultis_dir + "tmp")
		os.makedirs(recultis_dir + "tmp")
	open(recultis_dir + "tmp/rbdoom-3-bfg.deb", 'a').close()
	if shop == "steam":
		from tools import steam
		print("start steam")
		steam.start(shop_login, shop_password, recultis_dir, s_appid, game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	print("download game engine")
	from tools import download_engine
	result = download_engine.download(link, recultis_dir + "tmp/rbdoom-3-bfg.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "rbdoom-3-bfg.deb")
	prepare_engine()
	launchers()
	#Mark installed version by coping link file
	shutil.copy(self_dir + "link.txt", game_dir + "/version_link.txt")
	shutil.rmtree(recultis_dir + "tmp")

def uninstall():
	if os.path.isfile(desk_dir + "/doom3.desktop"):
		os.remove(desk_dir + "/doom3.desktop")
	if os.path.isfile(os.getenv("HOME") + "/.local/share/applications/doom3.desktop"):
		os.remove(os.getenv("HOME") + "/.local/share/applications/doom3.desktop")
	if os.path.isfile(os.getenv("HOME") + "/.local/share/icons/rbdoom-3-bfg.png"):
		os.remove(os.getenv("HOME") + "/.local/share/icons/rbdoom-3-bfg.png")
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
	deb_file_path = recultis_dir + "tmp/rbdoom-3-bfg.deb"
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

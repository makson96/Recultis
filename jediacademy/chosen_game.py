#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

recultis_dir = os.getenv("HOME") + "/.recultis/"
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
game_dir = recultis_dir + "JediAcademy/"
s_appid = "6020"

def prepare_engine():
	print("prepare engine")
	for binary in next(os.walk(recultis_dir + "tmp/JediAcademy/"))[2]:
		shutil.copy(recultis_dir + "tmp/JediAcademy/" + binary, game_dir + "GameData/" + binary)
	for directory in next(os.walk(recultis_dir + "tmp/JediAcademy/"))[1]:
		try:
			shutil.rmtree(game_dir + "GameData/" + directory)
		except:
			pass
		shutil.copytree(recultis_dir + "tmp/JediAcademy/" + directory, game_dir + "GameData/" + directory, symlinks=True)

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.icons") == False:
		os.makedirs(os.getenv("HOME") + "/.icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "openjk.png", os.getenv("HOME") + "/.icons/openjk.png")
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "openjk_amd64_sp.desktop", desk_dir + "/openjk_amd64_sp.desktop")
	shutil.copy(self_dir + "openjk_amd64_sp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_sp.desktop")
	shutil.copy(self_dir + "openjk_amd64_mp.desktop", desk_dir + "/openjk_amd64_mp.desktop")
	shutil.copy(self_dir + "openjk_amd64_mp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_mp.desktop")

def start(shop, shop_login, shop_password):
	print("start install openjk")
	if os.path.isdir(game_dir) == False:
		os.makedirs(game_dir)
	if os.path.isdir(game_dir + "GameData/") == False:
		os.makedirs(game_dir + "GameData/")
	if shop == "steam":
		from tools import steam
		print("start steam")
		steam.start(shop_login, shop_password, recultis_dir, s_appid, game_dir)
	link_file = open(self_dir + "link.txt")
	link = link_file.read()
	if os.path.isdir(recultis_dir + "tmp") == False:
		os.makedirs(recultis_dir + "tmp")
	else:
		shutil.rmtree(recultis_dir + "tmp")
		os.makedirs(recultis_dir + "tmp")
	print("download game engine")
	from tools import download_engine
	result = download_engine.download(link, recultis_dir + "tmp/openjk.deb")		
	from tools import unpack_deb
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "openjk.deb")
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
	deb_file_path = recultis_dir + "tmp/openjk.deb"
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

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil
from subprocess import check_output

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
recultis_dir = os.getenv("HOME") + "/.recultis/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

#List available games
def get_game_list():
	forbidden_dir = ["__pycache__"]
	all_dirs_and_files_list = os.listdir(self_dir)
	game_list = []
	for file_or_dir in all_dirs_and_files_list:
		if os.path.isdir(self_dir + file_or_dir):
			if file_or_dir not in forbidden_dir:
				#Status -1 Checking for update...
				game_list.append([file_or_dir, -1])
	game_list = sorted(game_list)
	print("list of all supported games:")
	print(game_list)
	return game_list

#Install game
def install(game_name, shop, shop_login, shop_password):
	#Import game specific data
	previous_dir = os.getcwd()
	os.chdir(self_dir + game_name)
	import game
	os.chdir(previous_dir)
	print("Start installing " + game.full_name)
	print("Preparing directory structure")
	if os.path.isdir(game.install_dir) == False:
		os.makedirs(game.install_dir)
	if os.path.isdir(recultis_dir + "tmp") == False:
		os.makedirs(recultis_dir + "tmp")
	else:
		shutil.rmtree(recultis_dir + "tmp")
		os.makedirs(recultis_dir + "tmp")
	open(recultis_dir + "tmp/" + game_name + ".deb", 'a').close()
	print("Download game content from digital distribution platform")
	if shop == "steam":
		from tools import steam
		print("Start Steam")
		shop_status_ok = steam.start(shop_login, shop_password, recultis_dir, game.s_appid, game.install_dir)
	else:
		print("No data download, only engine update")
		shop_status_ok = True
	if shop_status_ok == True:
		print("Downloading game engine")
		link_file = open(self_dir + game_name +"/link.txt")
		link = link_file.read()
		from tools import download_engine
		result = download_engine.download(link, recultis_dir + "tmp/" + game_name + ".deb")		
		from tools import unpack_deb
		unpack_deb.unpack_deb(recultis_dir + "tmp/", game_name + ".deb")
		game.prepare_engine()
		#launchers()
		#Mark installed version by coping link file
		shutil.copy(self_dir + "link.txt", game.install_dir + "/version_link.txt")
		shutil.rmtree(recultis_dir + "tmp")

def uninstall(game_name):
	#Import game specific data
	previous_dir = os.getcwd()
	os.chdir(self_dir + game_name)
	import game
	os.chdir(previous_dir)
	#We need to add here some kind of sandbox
	print("Uninstalling files")
	for u_file in game.uninstall_files_list:
		if os.path.isfile(u_file):
			os.remove(u_file)
	print("Uninstalling directories")
	for u_dir in game.uninstall_dir_list:
		if os.path.isdir(u_dir):
			shutil.rmtree(u_dir)

def make_launchers(game_name):
	#Import game specific data
	previous_dir = os.getcwd()
	os.chdir(self_dir + game_name)
	import game
	os.chdir(previous_dir)
	if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	print("Copy icon")
	shutil.copy(self_dir + game_name + "/" + game.icon_name, os.getenv("HOME") + "/.local/share/icons/" + game.icon_name)
	print("Make_launchers")
	for launcher in game.launcher_list:
		desktop_file = open(desk_dir + launcher[0], "w")
		desktop_file.write(launcher[1])
		desktop_file.close()
		os.chmod(desk_dir + launcher[0], 0o755)
		menu_file = open(os.getenv("HOME") + "/.local/share/applications/" + launcher[0] , "w")
		menu_file.write(launcher[1])
		menu_file.close()
		os.chmod(os.getenv("HOME") + "/.local/share/applications/" + launcher[0], 0o755)

def game_info(game_name, info_list):
	#Import game specific data
	previous_dir = os.getcwd()
	os.chdir(self_dir + game_name)
	import game
	os.chdir(previous_dir)
	#Game info still needs to be done
	return game.info(info_list)

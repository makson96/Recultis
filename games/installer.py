#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, shutil, importlib
from subprocess import check_output

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
recultis_dir = os.getenv("HOME") + "/.recultis/"
desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3] + "/"

#List available games
def get_game_list():
	print("Starting preparing game list")
	forbidden_dir = ["__pycache__"]
	all_dirs_and_files_list = os.listdir(self_dir)
	game_list = []
	for file_or_dir in all_dirs_and_files_list:
		if os.path.isdir(self_dir + file_or_dir):
			if file_or_dir not in forbidden_dir:
				#Status -1 Checking for update...
				game_list.append([file_or_dir, -1])
	game_list = sorted(game_list)
	print("List of all supported games:")
	print(game_list)
	return game_list

#Install game
def install(game_name, shop, shop_login, shop_password):
	#Import game specific data
	game = importlib.import_module("games." + game_name + ".game")
	#Run install
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
		from tools import update_do, download_engine, unpack_deb
		print("Download and prepare runtime")
		if os.path.isfile(recultis_dir + "runtime/recults2/version_link.txt") == True:
			runtime_version_file = open(self_dir + game_name + "/link.txt")
			runtime_version = runtime_version_file.read()
			runtime_link = update_do.get_link_string("runtime", self_dir)
			if runtime_version == runtime_link:
				runtime_update_needed = 0
			else:
				runtime_update_needed = 1
		else:
			runtime_update_needed = 1
		if runtime_update_needed == 1:
			result = download_engine.download(link, recultis_dir + "tmp/recultis-runtime.deb")		
			unpack_deb.unpack_deb(recultis_dir + "tmp/", "recultis-runtime.deb")
			if os.path.isdir(recultis_dir + "runtime/") == False:
				os.mkdirs(recultis_dir + "runtime/")
			if os.path.isdir(recultis_dir + "runtime/recultis2") == True:
				hutil.rmtree(recultis_dir + "runtime/recultis2")
			shutil.move(recultis_dir + "tmp/runtime/recultis2", recultis_dir + "runtime/")
			print("Runtime ready")
		else:
			print("Runtime up to date.")
		print("Downloading game engine")
		link = update_do.get_link_string(game_name, self_dir)
		result = download_engine.download(link, recultis_dir + "tmp/" + game_name + ".deb")		
		unpack_deb.unpack_deb(recultis_dir + "tmp/", game_name + ".deb")
		game.prepare_engine()
		#Mark installed version by coping link file
		version_link_file = open(game.install_dir + "/version_link.txt","w")
		version_link_file.write(link)
		version_link_file.close()
		shutil.rmtree(recultis_dir + "tmp")

def uninstall(game_name):
	#Import game specific data
	game = importlib.import_module("games." + game_name + ".game")
	#Run uninstall
	print("Preparing list of files and directories to uninstall")
	uninstall_files_list = []
	for icon_name in game.icon_list:
		uninstall_files_list.append(os.getenv("HOME") + "/.local/share/icons/" + icon_name)
	for launch_file in game.launcher_list:
		uninstall_files_list.append(desk_dir + launch_file[0])
		uninstall_files_list.append(os.getenv("HOME") + "/.local/share/applications/" + launch_file[0])
	uninstall_dir_list = [game.install_dir]
	#Add game specific files to uninstall list
	uninstall_files_list.extend(game.uninstall_files_list)
	uninstall_dir_list.extend(game.uninstall_dir_list)
	#We need to add here some kind of sandbox
	print("Uninstalling files:")
	print(uninstall_files_list)
	for u_file in uninstall_files_list:
		if os.path.isfile(u_file):
			os.remove(u_file)
	print("Uninstalling directories:")
	print(uninstall_dir_list)
	for u_dir in uninstall_dir_list:
		if os.path.isdir(u_dir):
			shutil.rmtree(u_dir)

def make_launchers(game_name):
	#Import game specific data
	game = importlib.import_module("games." + game_name + ".game")
	#Run creating launchers
	if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	print("Copy icon")
	for icon_name in game.icon_list:
		shutil.copy(self_dir + game_name + "/" + icon_name, os.getenv("HOME") + "/.local/share/icons/" + icon_name)
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

def game_info(game_name, requested_list):
	#Import game specific data
	game_module = importlib.import_module("games." + game_name + ".game")
	#Run info gathering
	if os.path.isfile(game_module.install_dir + "/version_link.txt"):
		version_file = open(game_module.install_dir + "/version_link.txt")
		version = version_file.read()
	else:
		version = "No proper install"
	link_file = open(self_dir + game_name + "/link.txt")
	link = link_file.read()
	deb_file_path = recultis_dir + "tmp/" + game_name + ".deb"
	return_list = []
	for requested_item in requested_list:
		if requested_item == "deb_file_path":
			return_list.append(deb_file_path)
		elif requested_item == "deb_url_path":
			return_list.append(link)
		elif requested_item == "install_dir":
			return_list.append(game.install_dir)
		elif requested_item == "version":
			return_list.append(version)
	return return_list

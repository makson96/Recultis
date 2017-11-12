#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, urllib.request, tarfile, shutil, importlib

#Status: -1 - Checking for update...; 0 - Not installed; 1 - Installed; 2 - Update available; 3 - Installing...	
def game_update_desc(info_list):
	game_fname = info_list[0]
	status = info_list[1]
	game_module = importlib.import_module("games." + game_fname + ".game")
	full_name = game_module.full_name
	rest_name = ""
	if status == -1:
		rest_name = " (Checking for update...)"
	elif status == 0:
		rest_name = " (Not installed)"
	elif status == 1:
		rest_name = " (Installed)"
	elif status == 2:
		rest_name = " (Update available)"
	elif status == 3:
		rest_name = " (Installing...)"
	return full_name + rest_name

#This function will return game status and update link if possible.
def game_update_status(game, self_dir, recultis_dir):
	link_string = get_link_string(game, self_dir + "games/")
	from games import installer
	game_info = installer.game_info(game, ["version"])
	version = game_info[0]
	if version != "No proper install":
		status = 1
		if version != link_string:
			status = 2
	else:
		status = 0
	print(game + " status is " + str(status))
	return status

def get_link_string(game, self_dir_games, legacy = 1): #legacy parameter for Recultis 1.2
	if game == "runtime":
		print("Getting runtime download link")
		target_url = "https://raw.githubusercontent.com/makson96/Recultis/master/games/runtime_link.txt"
	else:
		print("Getting game engine download link")
		#start of legacy code for Recultis 1.2
		if legacy = 1:
			target_url = "https://raw.githubusercontent.com/makson96/Recultis/1.2/games/" + game+ "/link.txt"
		#end of legacy code for Recultis 1.2
		else:
			target_url = "https://raw.githubusercontent.com/makson96/Recultis/master/games/" + game+ "/link.txt"
	try:
		data = urllib.request.urlopen(target_url)
		download_link = data.read().decode("utf-8")
	except urllib.request.URLError:
		if game == "runtime":
			print("Can't get runtime link from the server. Using local copy.")
			link_file = open(self_dir_games + "/runtime_link.txt")
		else:
			print("Can't get game engine link from the server. Using local copy.")
			link_file = open(self_dir_games + game +"/link.txt")
		download_link = link_file.read()
		link_file.close()
	print("Downalod link is:")
	print(download_link)
	return download_link

def recultis_update_do(self_dir, patch_link):
	print("Starting autoupdate.")
	#download patch
	patch_file = "patch.tar.gz"
	urllib.request.urlretrieve(patch_link, self_dir + patch_file)
	#remove old files
	for the_file in os.listdir(self_dir):
		file_path = os.path.join(self_dir, the_file)
		if os.path.isfile(file_path) and the_file != patch_file:
			os.remove(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)
	#unpack patch
	tar = tarfile.open(self_dir + patch_file)
	tar.extractall()
	tar.close()
	#remove patch file
	os.remove(self_dir + patch_file)
	#copy everything one directory backs
	patch_dir = os.listdir(self_dir)[0]
	for the_file_or_dir in os.listdir(patch_dir):
		shutil.move(os.path.join(patch_dir, the_file_or_dir), os.path.join(self_dir, the_file_or_dir))
	shutil.rmtree(patch_dir)
	print("Autoupdate complete.")

def recultis_update_check(self_dir, recultis_version):
	print("Checking if Recultis update is available")
	v_major = str(int(recultis_version[0]) + 1) + ".0.0"
	v_minor = recultis_version[0:2] + str(int(recultis_version[2]) + 1) + ".0"
	v_patch = recultis_version[0:4] + str(int(recultis_version[4]) + 1)
	update_list = [v_major, v_minor, v_patch]
	if os.path.isfile(self_dir + "patch_link.txt"):
		os.remove(self_dir + "patch_link.txt")
	status = 1
	for potential_patch in update_list:
		try:
			patch_url = "https://github.com/makson96/Recultis/archive/v" + potential_patch + ".tar.gz"
			urllib.request.urlopen(patch_url, timeout=1)
			patch_link_file = open(self_dir + "patch_link.txt", "a")
			patch_link_file.write(patch_url + "\n")
			patch_link_file.close()
			status = 2		
			print("Found following Recultis patch:")
			print(patch_url)		
		except urllib.request.URLError:
				pass
	print("Return Recultis update status: " + str(status))
	return status

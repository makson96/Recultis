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
def game_update_status(game, self_dir):
	target_url = "https://raw.githubusercontent.com/makson96/Recultis/master/games/" + game+ "/link.txt"
	from games import installer
	game_info = installer.game_info(game, ["version"])
	version = game_info[0]
	try:
		data = urllib.request.urlopen(target_url)
		download_link_new = data.read().decode("utf-8")
	#If can't get link assume that local link is most recent.
	except urllib.request.URLError:
		download_link_new = version
	if version != "No proper install":
		status = 1
		if version != download_link_new:
			status = 2
	else:
		status = 0
	#Update link only if needed
	if version != download_link_new:
		target_file_path = self_dir + "games/" +game + "/link.txt"
		target_file = open(target_file_path, "w")
		target_file.write(download_link_new)
		target_file.close()
		print("Game engine link updated.")
	print(game + " status is " + str(status))
	return status

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

def recultis_update_check(self_dir, update_list):
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
		except urllib.request.URLError:
				pass
	return status

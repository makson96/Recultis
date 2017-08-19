#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, urllib.request, importlib

def start(game, self_dir):
	target_url = "https://raw.githubusercontent.com/makson96/Recultis/master/games" + game+ "/link.txt"
	#this is legacy link to be removed in recultis 1.2
	target_url_legacy = "https://raw.githubusercontent.com/makson96/Recultis/master/" + game+ "/link.txt"
	chosen_game = importlib.import_module(game+".chosen_game")
	game_info = chosen_game.info(["version"])
	version = game_info[0]
	
	try:
		data = urllib.request.urlopen(target_url)
		download_link_new = data.read().decode("utf-8")
	#If can't get link assume that local link is most recent.
	except urllib.request.URLError:
		#this is legacy code to be removed in recultis 1.2
		try:
			data = urllib.request.urlopen(target_url_legacy)
			download_link_new = data.read().decode("utf-8")
		except urllib.request.URLError:
		#end of legacy code
			download_link_new = version
	if version != "No proper install":
		status = "Installed"
		if version != download_link_new:
			status = "Update available"
	else:
		status = "Not installed"
	#Update link only if needed
	if version != download_link_new:
		update_link(game, self_dir, download_link_new)
	print(game + " status is " + status)
	return status

def update_link(game, self_dir, download_link_new):
	target_file_path = self_dir + game + "/link.txt"
	target_file = open(target_file_path, "w")
	target_file.write(download_link_new)
	target_file.close()
	print("Game engine link updated.")
	return 0

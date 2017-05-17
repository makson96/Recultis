#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, urllib.request, importlib

def start(game):
	target_url = "https://raw.githubusercontent.com/makson96/free-engineer/master/" + game+ "/link.txt"
	chosen_game = importlib.import_module(game+".chosen_game")
	game_info = chosen_game.info(["game_dir", "version"])
	game_dir = game_info[0]
	version = game_info[1]
	
	data = urllib.request.urlopen(target_url)
	download_link_new = data.read().decode("utf-8")
	if os.path.isdir(game_dir) == True:
		status = "Installed"
		if version != download_link_new:
			status = "Update available"
	else:
		status = "Not installed"
	update_link(game)
	print(game + " status is " + status)
	return status

def update_link(game):
	target_url = "https://raw.githubusercontent.com/makson96/free-engineer/master/" + game+ "/link.txt"
	target_file = os.getcwd() + "/" + game + "/link.txt"
	urllib.request.urlretrieve(target_url, target_file)
	print("Game engine link updated")
	return 0

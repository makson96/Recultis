#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import urllib.request

def start(game, self_dir):
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
		status = "Installed"
		if version != download_link_new:
			status = "Update available"
	else:
		status = "Not installed"
	#Update link only if needed
	if version != download_link_new:
		update_link(game, self_dir, download_link_new)
	print(game + " status is " + status)
	if status == "Checking for update...":
		status_nr = -1
	elif status == "Not installed":
		status_nr = 0
	elif status == "Installed":
		status_nr = 1
	elif status == "Update available":
		status_nr = 2
	elif status == "Installing...":
		status_nr = 3
	return status_nr

def update_link(game, self_dir, download_link_new):
	target_file_path = self_dir + "games/" +game + "/link.txt"
	target_file = open(target_file_path, "w")
	target_file.write(download_link_new)
	target_file.close()
	print("Game engine link updated.")
	return 0

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time, shutil
from subprocess import Popen, PIPE

def start(login, password, recultis_dir, s_appid, game_dir):
	shop_install_dir = recultis_dir + "shops/gog/"
	print("Download lgogdownloader")
	from tools import update_do, download_engine, unpack_deb
	lgog_link = update_do.get_link_string("lgogdownloader", "recultis2")
	result = download_engine.download(lgog_link, recultis_dir + "tmp/lgogdownloader.deb")		
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "lgogdownloader.deb")
	if os.path.isdir(shop_install_dir) == False:
		os.makedirs(shop_install_dir)
	else:
		shutil.rmtree(shop_install_dir)
		os.makedirs(shop_install_dir)
	shutil.move(recultis_dir + "tmp/lgogdownloader/bin/lgogdownloader", shop_install_dir)
	print("Download innoextract")
	print("Download game using lgogdownloader")
	os.chdir(shop_install_dir)
	gog_error = run(login, password, shop_install_dir, s_appid, game_dir)
	print("Extract game using innoextract")
	return True

def run(login, password, shop_install_dir, s_appid, game_dir):
	if os.path.isfile(shop_install_dir+"gog_log.txt") == True:
		os.remove(shop_install_dir+"gog_log.txt")
	print("Running following gog command:")
	print("./lgogdownloader --download --game " + s_appid + " --directory " + game_dir + " --no-color --no-unicode")
	print("Check " + shop_install_dir + "gog_log.txt for more details.")
	env_var = "LD_LIBRARY_PATH=$HOME/.recultis/runtime/recultis2:$HOME/.recultis/runtime/recultis2/custom"
	gog_download = Popen(env_var + " stdbuf -oL -eL ./lgogdownloader --download --game " + s_appid + " --directory " + game_dir + " --no-color --no-unicode", shell=True, stdout=open("gog_log.txt", "wb"), stdin=PIPE)
	while gog_download.poll() is None:
		time.sleep(2)
		gog_last_line = get_last_log_line()
		#Insert login
		if "Email" in gog_last_line:
			gog_download.stdin.write(bytes(login + '\n', 'ascii'))
			gog_download.stdin.flush()
		#Insert Password
		if "Password" in gog_last_line:
			gog_download.stdin.write(bytes(password + '\n', 'ascii'))
			gog_download.stdin.flush()
		#If computer is not registered on GOG, handle GOG Security code
		elif 'Security code' in gog_last_line:
			gog_guard_code = steam_guard(shop_install_dir)
			gog_download.stdin.write(bytes(steam_guard_code + '\n', 'ascii'))
			gog_download.stdin.flush()
	#if there is only 1 line after gog finished working, it means it crashed.
	if sum(1 for line in open('gog_log.txt')) == 1:
		rc = 0
	else:
		rc = 1
	return rc

def get_last_log_line():
	gog_log_file = open("gog_log.txt", "r")
	gog_log_lines = gog_log_file.readlines()
	if len(gog_log_lines) > 0:
		gog_last_line = gog_log_lines[-1]
	else:
		gog_last_line = ""
	gog_log_file.close()
	return gog_last_line

def gog_guard(shop_install_dir):
	while os.path.isfile(shop_install_dir + "gog_guard_key.txt") == False:
		time.sleep(2)
	print('GOG Security code detected. Verifying...')
	gog_guard_file = open(shop_install_dir + "gog_guard_key.txt", "r")
	gog_guard_code = gog_guard_file.readline()
	gog_guard_file.close()
	os.remove(shop_install_dir + "gog_guard_key.txt")
	print(str(gog_guard_code).upper())
	return str(gog_guard_code.upper())

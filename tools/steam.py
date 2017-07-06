#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time
from subprocess import Popen, PIPE

def start(login, password, recultis_dir, s_appid, game_dir):
	os.chdir(recultis_dir)
	if os.path.isfile(recultis_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", recultis_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(recultis_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	steam_error = 1
	retry_nr = 0
	while steam_error == 1:
		steam_error = run(login, password, recultis_dir, s_appid, game_dir)
		if steam_error == 1:
			print("Steamcmd error. Retry.")
			retry_nr = retry_nr + 1
			if retry_nr > 4:
				steam_log_file = open("steam_log.txt", "a")
				steam_log_file.write("\nSteamcmd Error. Terminate.")
				steam_log_file.close()
				print("Steamcmd Error. Terminate.")
				break
			

def get_last_log_line():
	steam_log_file = open("steam_log.txt", "r")
	steam_log_lines = steam_log_file.readlines()
	steam_last_line = steam_log_lines[-1]
	steam_log_file.close()
	return steam_last_line

def steam_guard(recultis_dir):
	print('Steam Guard')
	while os.path.isfile(recultis_dir + "steam_guard_key.txt") == False:
		time.sleep(2)
	steam_guard_file = open(recultis_dir + "steam_guard_key.txt", "r")
	steam_guard_code = steam_guard_file.readline()
	steam_guard_file.close()
	os.remove(recultis_dir + "steam_guard_key.txt")
	print(str(steam_guard_code).upper())
	return str(steam_guard_code.upper())
	

def run(login, password, recultis_dir, s_appid, game_dir):
	if os.path.isfile(recultis_dir+"steam_log.txt") == True:
		os.remove(recultis_dir+"steam_log.txt")
	steam_download = Popen("script -q -c \"./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit\" /dev/null", shell=True, bufsize=1, stdout=open("steam_log.txt", "wb"), stdin=PIPE)
	while steam_download.poll() is None:
		time.sleep(2)
		steam_last_line = get_last_log_line()
		#Terminate the process if bad login or password
		if "Login Failure" in steam_last_line:
			steam_download.terminate()
		#Terminate the process if not owning the game
		elif "Failed to install app" in steam_last_line:
			steam_download.terminate()
		#Retry 5 times if steamcmd has memory access error
		elif '$DEBUGGER "$STEAMEXE" "$@"' in steam_last_line:
			return 1
		#If computer is not registered on Steam, handle Steam Guard
		elif 'Steam Guard' in steam_last_line:
			steam_guard_code = steam_guard(recultis_dir)
			steam_download.stdin.write(bytes(steam_guard_code + '\n', 'ascii'))
			steam_download.stdin.flush()
	return 0

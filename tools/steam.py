#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time, shutil
from subprocess import Popen, PIPE

def start(login, password, recultis_dir, s_appid, game_dir):
	os.chdir(recultis_dir)
	if login == "" or password == "":
		steam_log_file = open("steam_log.txt", "w")
		steam_log_file.write("Steamcmd error. Login or password not provided.")
		steam_log_file.close()
		print("Steamcmd error. Login or password not provided. try again with correct one.")
		steam_error = 0
	else:
		steamcmd_install(recultis_dir)
		steam_error = 2
		retry_nr = 0
	while steam_error == 2:
		steam_error = run(login, password, recultis_dir, s_appid, game_dir)
		if steam_error == 2:
			print("Steamcmd error. Retry.")
			retry_nr = retry_nr + 1
			if retry_nr == 5:
				print("Steamcmd error. Reinstall steamcmd.")
				steamcmd_reinstall(recultis_dir)
			elif retry_nr == 8:
				steam_error = 0
	if steam_error == 0:
		steam_log_file = open("steam_log.txt", "a")
		steam_log_file.write("\nSteamcmd Error. Terminate.")
		steam_log_file.close()
		print("Steamcmd Error. Terminate.")
	return steam_error

def steamcmd_install(recultis_dir):
	if os.path.isfile(recultis_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", recultis_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(recultis_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()

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
	print("Running following steamcmd command:")
	print("./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '******' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit")
	print("Check " + recultis_dir + "steam_log.txt for more details.")
	steam_download = Popen("script -q -c \"./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '" + password + "' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit\" /dev/null", shell=True, stdout=open("steam_log.txt", "wb"), stdin=PIPE)
	while steam_download.poll() is None:
		time.sleep(2)
		steam_last_line = get_last_log_line()
		#Terminate the process if bad login or password
		if "FAILED with result code" in steam_last_line:
			steam_download.terminate()
			return 0
		#Terminate the process if not owning the game
		elif "Failed to install app" in steam_last_line:
			steam_download.terminate()
			return 0
		#Retry 5 times if steamcmd has memory access error
		elif '$DEBUGGER "$STEAMEXE" "$@"' in steam_last_line:
			return 2
		#If computer is not registered on Steam, handle Steam Guard
		elif 'Steam Guard' in steam_last_line:
			steam_guard_code = steam_guard(recultis_dir)
			steam_download.stdin.write(bytes(steam_guard_code + '\n', 'ascii'))
			steam_download.stdin.flush()
	#if there is only 1 line after steamcmd finished working, it means it crashed.
	if sum(1 for line in open('steam_log.txt')) == 1:
		rc = 0
	else:
		rc = 1
	return rc

def steamcmd_reinstall(recultis_dir):
	if os.path.isfile(recultis_dir+"steam.sh") == True:
		os.remove(recultis_dir+"steam.sh")
	if os.path.isfile(recultis_dir+"steamcmd.sh") == True:
		os.remove(recultis_dir+"steamcmd.sh")
	if os.path.isfile(recultis_dir+"steamcmd_linux.tar.gz") == True:
		os.remove(recultis_dir+"steamcmd_linux.tar.gz")
	if os.path.isdir(recultis_dir+"linux32") == True:
		shutil.rmtree(recultis_dir+"linux32")
	if os.path.isdir(recultis_dir+"linux64") == True:
		shutil.rmtree(recultis_dir+"linux64")
	if os.path.isdir(recultis_dir+"package") == True:
		shutil.rmtree(recultis_dir+"package")
	if os.path.isdir(recultis_dir+"public") == True:
		shutil.rmtree(recultis_dir+"public")
	steamcmd_install(recultis_dir)

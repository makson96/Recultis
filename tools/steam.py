#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time, shutil
from subprocess import Popen, PIPE

recultis_dir = os.getenv("HOME") + "/.recultis/"
steam_dir = recultis_dir + "shops/steam/"

def start(login, password, recultis_dir, s_appid, game_dir):
	print("Starting SteamCMD procedure")
	shop_install_dir = recultis_dir + "shops/steam/"
	if os.path.isdir(shop_install_dir) == False:
		os.makedirs(shop_install_dir)
		#start of legacy code for Recultis 1.2
		if os.path.isfile(recultis_dir+"steam.sh") == True:
			shutil.move(recultis_dir+"steam.sh", shop_install_dir)
		if os.path.isfile(recultis_dir+"steamcmd.sh") == True:
			shutil.move(recultis_dir+"steamcmd.sh", shop_install_dir)
		if os.path.isfile(recultis_dir+"steamcmd_linux.tar.gz") == True:
			shutil.move(recultis_dir+"steamcmd_linux.tar.gz", shop_install_dir)
		if os.path.isfile(recultis_dir+"steam_log.txt") == True:
			shutil.move(recultis_dir+"steam_log.txt", shop_install_dir)
		if os.path.isdir(recultis_dir+"linux32") == True:
			shutil.move(recultis_dir+"linux32", shop_install_dir)
		if os.path.isdir(recultis_dir+"linux64") == True:
			shutil.move(recultis_dir+"linux64", shop_install_dir)
		if os.path.isdir(recultis_dir+"package") == True:
			shutil.move(recultis_dir+"package", shop_install_dir)
		if os.path.isdir(recultis_dir+"public") == True:
			shutil.move(recultis_dir+"public", shop_install_dir)
		#end of legacy code for Recultis 1.2
	os.chdir(shop_install_dir)
	if login == "" or password == "":
		steam_log_file = open("steam_log.txt", "w")
		steam_log_file.write("Steamcmd Error. Login or password not provided.\n")
		steam_log_file.close()
		print("Steamcmd Error. Login or password not provided. try again with correct one.")
		steam_error = 0
	else:
		steamcmd_install(shop_install_dir)
		steam_error = 2
		retry_nr = 0
	while steam_error == 2:
		steam_error = run(login, password, shop_install_dir, s_appid, game_dir)
		if steam_error == 2:
			print("Steamcmd error. Retry.")
			retry_nr = retry_nr + 1
			if retry_nr == 5:
				print("Steamcmd error. Reinstall steamcmd.")
				steamcmd_reinstall(shop_install_dir)
			elif retry_nr == 8:
				steam_error = 0
	if steam_error == 0:
		steam_log_file = open("steam_log.txt", "a")
		steam_log_file.write("\nSteamcmd Error. Terminate.")
		steam_log_file.close()
		print("Steamcmd Error. Terminate.")
	return steam_error

def steamcmd_install(shop_install_dir):
	print("Installing SteamCMD")
	if os.path.isfile(shop_install_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", shop_install_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(shop_install_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()

def get_last_log_line():
	try:
		steam_log_file = open("steam_log.txt", "r")
		steam_log_lines = steam_log_file.readlines()
		if len(steam_log_lines) > 0:
			steam_last_line = steam_log_lines[-1]
		else:
			steam_last_line = ""
		steam_log_file.close()
	except FileNotFoundError:
		steam_last_line = ""
	return steam_last_line

def steam_guard(shop_install_dir):
	while os.path.isfile(shop_install_dir + "guard_key.txt") == False:
		time.sleep(2)
	print('Steam Guard Key detected. Verifying...')
	steam_guard_file = open(shop_install_dir + "guard_key.txt", "r")
	steam_guard_code = steam_guard_file.readline()
	steam_guard_file.close()
	os.remove(shop_install_dir + "guard_key.txt")
	print(str(steam_guard_code).upper())
	return str(steam_guard_code.upper())
	

def run(login, password, shop_install_dir, s_appid, game_dir):
	if os.path.isfile(shop_install_dir+"steam_log.txt") == True:
		os.remove(shop_install_dir+"steam_log.txt")
	print("Running following steamcmd command:")
	print("./steamcmd.sh +@sSteamCmdForcePlatformType windows +login '" + login + "' '******' +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit")
	print("Check " + shop_install_dir + "steam_log.txt for more details.")
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
			steam_guard_code = steam_guard(shop_install_dir)
			steam_download.stdin.write(bytes(steam_guard_code + '\n', 'ascii'))
			steam_download.stdin.flush()
	#if there is only 1 line after steamcmd finished working, it means it crashed.
	if sum(1 for line in open('steam_log.txt')) == 1:
		rc = 0
	else:
		rc = 1
	return rc

def steamcmd_reinstall(shop_install_dir):
	print("Reinstalling SteamCMD")
	print("Removing SteamCMD")
	if os.path.isfile(shop_install_dir+"steam.sh") == True:
		os.remove(shop_install_dir+"steam.sh")
	if os.path.isfile(shop_install_dir+"steamcmd.sh") == True:
		os.remove(shop_install_dir+"steamcmd.sh")
	if os.path.isfile(shop_install_dir+"steamcmd_linux.tar.gz") == True:
		os.remove(shop_install_dir+"steamcmd_linux.tar.gz")
	if os.path.isdir(shop_install_dir+"linux32") == True:
		shutil.rmtree(shop_install_dir+"linux32")
	if os.path.isdir(shop_install_dir+"linux64") == True:
		shutil.rmtree(shop_install_dir+"linux64")
	if os.path.isdir(shop_install_dir+"package") == True:
		shutil.rmtree(shop_install_dir+"package")
	if os.path.isdir(shop_install_dir+"public") == True:
		shutil.rmtree(shop_install_dir+"public")
	steamcmd_install(shop_install_dir)

def status():
	os.chdir(steam_dir)
	status = "Downloading and installing game data"
	percent = 0
	steam_last_line = get_last_log_line()
	if steam_last_line == "":
		steam_last_line = "downloading, progress: 0,0 ("
	#This code handle steamcmd status if everything is ok
	if ("downloading, progress: " in steam_last_line) or ("validating, progress: " in steam_last_line):
		steam_value = steam_last_line.split("progress: ")[1]
		steam_value = steam_value.split(" (")[0]
		steam_value = steam_value.split(",")[0]
		steam_value = steam_value.split(".")[0]
		steam_value = int(steam_value)
		status = "Downloading and installing game data"
		percent = steam_value
	elif "Success!" in steam_last_line:
		status = "Download of game data completed"
		percent = 100
	#this code handle steamcmd status if warning is present.
	elif "Steam Guard" in steam_last_line:
		status = "Warning: Waiting for Steam Guard authentication."
		percent = 0
	#this code handle steamcmd status if steam tool marked steam_log.txt file with error.
	if "Steamcmd Error." in steam_last_line:
		try:
			steam_log_file = open("steam_log.txt", "r")
			steam_log_lines = steam_log_file.readlines()
			steam_error_line = steam_log_lines[-3]
			steam_log_file.close()
		except:
			steam_error_line = "Steamcmd Error. Terminate."
		if "FAILED with result code 5" in steam_error_line:
			status = "Error: Steam - bad login or password. Please correct and start again."
			percent = 0
		elif "Login or password not provided." in steam_error_line:
			status = "Error: Steam - Login or password not provided. Try again with correct one."
			percent = 0
		elif "Failed to install app" in steam_error_line:
			status = "Error: Steam - you are not game owner. Please correct and start again."
			percent = 0
		elif "FAILED with result code 65" in steam_error_line:
			status = "Error: Could not perform Steam Guard authentication. Please try again."
			percent = 0
		else:
			status = "Error: Steamcmd internal error. Please contact Recultis project for support."
			percent = 0
	return status, percent

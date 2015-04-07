#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os, tarfile, time, shutil, fileinput
from subprocess import call, check_output

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self_dir = "/opt/free-engineer/"
engine_dir = "/opt/openraider/"
local_openraider_dir = os.getenv("HOME") + "/.OpenRaider/"

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_data_dir1 = engineer_dir + "tb1/"
game_data_dir2 = engineer_dir + "tb2/"
game_data_dir3 = engineer_dir + "tb3/"
s_appid1 = "224960"
s_appid2 = "225300"
s_appid3 = "225320"

def start_steam(user):
	import steam
	steam.steamcmd(user, s_appid, engineer_dir, game_data_dir)
	while os.path.isdir(game_data_dir + "data") == False:
		time.sleep(2)
	copy_config()
	launchers()

def copy_config():
	if os.path.isdir(local_openraider_dir) == False:
		os.makedirs(local_openraider_dir)
	if os.path.exists(local_openraider_dir + "OpenRaider.ini") == False:
		print("copying OpenRaider.ini")
		#shutil.copy(engine_dir + "share/OpenRaider/OpenRaider.ini", local_openraider_dir + "OpenRaider.ini")
		if s_appid == s_appid1:
			shutil.copy(self_dir + "tombraider/OpenRaider_tb1.ini", local_openraider_dir + "OpenRaider.ini")
		elif s_appid == s_appid2:
			shutil.copy(self_dir + "tombraider/OpenRaider_tb2.ini", local_openraider_dir + "OpenRaider.ini")
		elif s_appid == s_appid3:
			shutil.copy(self_dir + "tombraider/OpenRaider_tb3.ini", local_openraider_dir + "OpenRaider.ini")
		for line in fileinput.FileInput(local_openraider_dir + "OpenRaider.ini",inplace=1):
			line = line.replace("^^^^", os.getenv("HOME"))
			print(line, end='')
	if os.path.exists(game_data_dir + "data/splash.tga") == False:
		shutil.copy(engine_dir + "share/OpenRaider/splash.tga", game_data_dir + "data/splash.tga")
	print("symlinking")
	if os.path.exists(game_data_dir + "OpenRaider") == False:
		os.symlink(engine_dir + "bin/OpenRaider", game_data_dir + "OpenRaider")

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	if s_appid == s_appid1:
		shutil.copy(self_dir + "tombraider/tb1.desktop", desk_dir + "/tb1.desktop")
		shutil.copy(self_dir + "tombraider/tb1.desktop", os.getenv("HOME") + "/.local/share/applications/tb1.desktop")
	elif s_appid == s_appid2:
		shutil.copy(self_dir + "tombraider/tb2.desktop", desk_dir + "/tb2.desktop")
		shutil.copy(self_dir + "tombraider/tb2.desktop", os.getenv("HOME") + "/.local/share/applications/tb2.desktop")
	elif s_appid == s_appid3:
		shutil.copy(self_dir + "tombraider/tb3.desktop", desk_dir + "/tb3.desktop")
		shutil.copy(self_dir + "tombraider/tb3.desktop", os.getenv("HOME") + "/.local/share/applications/tb3.desktop")
	
	msgBox = QMessageBox.information(qw, "Game is ready", "Have fun!")
	qw.close()

class Game:
	
	nested = 0
	
	def __init__(self, rootWindow = 0, nested = 0, game_variant = 1):
		global qw, game_data_dir, s_appid
		if game_variant == 1:
			game_data_dir = game_data_dir1
			s_appid = s_appid1
		elif game_variant == 2:
			game_data_dir = game_data_dir2
			s_appid = s_appid2
		elif game_variant == 3:
			game_data_dir = game_data_dir3
			s_appid = s_appid3
		
		self.nested = nested
		if self.nested == 0:
			s_app = QApplication(sys.argv)
		#tutaj okno z wyborem skad pobrac game data
		nameLabel = QLabel("Choose the platfrom from which you want to get game data:")
		p_group = QButtonGroup()
		r0 = QRadioButton("Steam")
		p_group.addButton(r0)
		#self.r1 = QRadioButton("1")
		#p_group.addButton(r1)
		r0.setChecked(True)
		loginLabel = QLabel("Enter your Steam login:")
		loginText = QLineEdit()
		chooseButton = QPushButton("Choose")
		exitButton = QPushButton("Exit")
		
		vbox1 = QVBoxLayout()
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		qw = QWidget()

		vbox1.addWidget(nameLabel)
		vbox1.addWidget(r0)
		#vbox1.addWidget(r1)
		hbox1.addWidget(loginLabel)
		hbox1.addWidget(loginText)
		hbox2.addWidget(chooseButton)
		hbox2.addWidget(exitButton)
		vbox1.addLayout(hbox1)
		vbox1.addLayout(hbox2)
		
		chooseButton.clicked.connect(lambda : start_steam(str(loginText.text())))
		exitButton.clicked.connect(qw.close)
 
		mainLayout = QGridLayout()
		mainLayout.addLayout(vbox1, 0, 1)
		
		qw.setLayout(mainLayout)
		qw.setWindowTitle("Choose Game Data Platform")
		qw.show()
		if self.nested == 0:
			s_app.exec_()

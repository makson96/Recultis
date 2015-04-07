#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, time, shutil
from subprocess import check_output

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self_dir = "/opt/free-engineer/"
engine_dir = "/opt/dxx-rebirth/"

local_descent1_dir = os.getenv("HOME") + "/.d1x-rebirth/"
local_descent2_dir = os.getenv("HOME") + "/.d2x-rebirth/"

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_data_dir1 = engineer_dir + "descent1/"
game_data_dir2 = engineer_dir + "descent2/"
s_appid1 = "273570"
s_appid2 = "273580"

def start_steam(user):
	import steam
	steam.steamcmd(user, s_appid, engineer_dir, game_data_dir)
	while os.path.isdir(game_data_dir + "missions") == False:
		time.sleep(2)
	symlink()
	launchers()

def symlink():
	if os.path.exists(local_descent_dir) == False:
		os.makedirs(local_descent_dir)
	print("symlinking")
	if os.path.exists(local_descent_dir + "Data") == False:
		os.symlink(game_data_dir, local_descent_dir + "Data")

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	if s_appid == s_appid1:
		shutil.copy(self_dir + "descent/descent1.desktop", desk_dir + "/descent1.desktop")
		shutil.copy(self_dir + "descent/descent1.desktop", os.getenv("HOME") + "/.local/share/applications/descent1.desktop")
	elif s_appid == s_appid2:
		shutil.copy(self_dir + "descent/descent2.desktop", desk_dir + "/descent2.desktop")
		shutil.copy(self_dir + "descent/descent2.desktop", os.getenv("HOME") + "/.local/share/applications/descent2.desktop")
	
	msgBox = QMessageBox.information(qw, "Game is ready", "Have fun!")
	qw.close()

class Game:
	
	nested = 0
	
	def __init__(self, rootWindow = 0, nested = 0, game_variant = 1):
		global qw, game_data_dir, s_appid
		if game_variant == 1:
			game_data_dir = game_data_dir1
			s_appid = s_appid1
			local_descent_dir = local_descent1_dir
		elif game_variant == 2:
			game_data_dir = game_data_dir2
			s_appid = s_appid2
			local_descent_dir = local_descent2_dir
		
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

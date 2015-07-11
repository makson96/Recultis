#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, time, shutil
from subprocess import call, check_output

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self_dir = "/opt/free-engineer/"
engine_dir = "/opt/openxcom/"

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_data_dir = engineer_dir + "xcom/"
local_data_dir = os.getenv("HOME") + "/.local/share/openxcom/data/"
s_appid = "7760"

def start_steam(user):
	print(user)
	steamcmd = call("x-terminal-emulator -e 'python3 " + self_dir + "steam.py " + user + " " + s_appid + " " + engineer_dir + " " + game_data_dir + "'", shell=True)
	while os.path.isdir(game_data_dir + "XCOM/") == False:
		time.sleep(2)
	symlink()
	launchers()

def symlink():
	if os.path.isdir(local_data_dir) == False:
		os.makedirs(local_data_dir)
	print("symlinking1")
	dirs = ["GEODATA", "GEOGRAPH", "MAPS", "ROUTES", "SOUND", "TERRAIN", "UFOGRAPH", "UFOINTRO", "UNITS"]
	for xdir in dirs:
		if os.path.exists(local_data_dir + xdir) == False:
			os.symlink(game_data_dir + "XCOM/" + xdir, local_data_dir + xdir)
	print("symlinking2")
	dirs = ["Language", "Resources", "Ruleset", "Shaders", "SoldierName"]
	for xdir in dirs:
		if os.path.exists(local_data_dir + xdir) == False:
			os.symlink(engine_dir + "/share/openxcom/data/" + xdir, local_data_dir + xdir)
	dirs = ["MAPS/FIRES.MAP", "MAPS/INTERC.MAP", "ROUTES/FIRES.RMP", "ROUTES/INTERC.RMP"]
	for xdir in dirs:
		if os.path.exists(game_data_dir + "XCOM/" + xdir) == False:
			os.symlink(engine_dir + "/share/openxcom/data/" + xdir, game_data_dir + "XCOM/" + xdir)

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "xcom/xcom.desktop", desk_dir + "/xcom.desktop")
	shutil.copy(self_dir + "xcom/xcom.desktop", os.getenv("HOME") + "/.local/share/applications/xcom.desktop")
		
	msgBox = QMessageBox.information(qw, "Game is ready", "Have fun!")
	qw.close()

class Game:
	
	nested = 0
	
	def __init__(self, rootWindow = 0, nested = 0):
		global qw
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

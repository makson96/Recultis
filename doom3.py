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
engine_dir = "/opt/rbdoom-3-bfg/"

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_data_dir = engineer_dir + "doom3/"
s_appid = "208200"

def start_steam(user):
	import steam
	steam.steamcmd(user, s_appid, engineer_dir, game_data_dir)
	while os.path.isdir(game_data_dir + "base/") == False:
		time.sleep(2)
	symlink()
	launchers()

def symlink():
		print("symlinking")
		if os.path.exists(game_data_dir + "RBDoom3BFG") == False:
			os.symlink(engine_dir + "RBDoom3BFG", game_data_dir + "RBDoom3BFG")

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "doom3/doom3.desktop", desk_dir + "/doom3.desktop")
	shutil.copy(self_dir + "doom3/doom3.desktop", os.getenv("HOME") + "/.local/share/applications/doom3.desktop")
		
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

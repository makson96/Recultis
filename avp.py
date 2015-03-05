#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os, tarfile, time
from subprocess import call, check_output

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self_dir = "/opt/free-engineer/"
engine_dir = "/opt/avp/"

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_data_dir = engineer_dir + "AliensVsPredator/"
s_appid = "3730"

def steamcmd(user):
	if os.path.isdir(engineer_dir) == False:
		os.makedirs(engineer_dir)
	os.chdir(engineer_dir)
	if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
		tar = tarfile.open(self_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	print(user)
	if os.path.isdir(game_data_dir) == False:
		s_download = call("x-terminal-emulator -e './steamcmd.sh +@sSteamCmdForcePlatformType windows +login " + user + " +force_install_dir " + game_data_dir + " +app_update " + s_appid + " validate +quit'", shell=True)
	while os.path.isdir(game_data_dir+"avp_huds") == False:
		time.sleep(2)
	files_lowercase()
	launchers()

def files_lowercase():
	for avp_file_or_dir in os.listdir(game_data_dir):
		if os.path.isdir(game_data_dir + avp_file_or_dir) == True:
			print("entering dir " + avp_file_or_dir)
			for avp_file in os.listdir(game_data_dir + avp_file_or_dir):
				os.rename(game_data_dir + avp_file_or_dir + "/" + avp_file, game_data_dir + avp_file_or_dir + "/" + avp_file.lower())
			os.rename(game_data_dir + avp_file_or_dir, game_data_dir + avp_file_or_dir.lower())
		elif os.path.isfile(game_data_dir + avp_file_or_dir) == True:
			os.rename(game_data_dir + avp_file_or_dir, game_data_dir + avp_file_or_dir.lower())

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	print("symlinking desktop")
	os.symlink(self_dir + "avp.desktop", desk_dir + "/avp.desktop")
	os.symlink(self_dir + "avp.desktop", os.getenv("HOME") + "/.local/share/applications/avp.desktop")
		
	msgBox = QMessageBox.information(qw, "Game is ready", "Have fun!")
	qw.close()

class Steam:
	
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
		
		chooseButton.clicked.connect(lambda : steamcmd(str(loginText.text())))
		exitButton.clicked.connect(qw.close)
 
		mainLayout = QGridLayout()
		mainLayout.addLayout(vbox1, 0, 1)
		
		qw.setLayout(mainLayout)
		qw.setWindowTitle("Choose Game Data Platform")
		qw.show()
		if self.nested == 0:
			s_app.exec_()

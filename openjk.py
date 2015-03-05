#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os, tarfile, time
from subprocess import call, check_output

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self_dir = "/opt/free-engineer/"
engine_dir = "/opt/OpenJK/"
local_openjk_dir = os.getenv("HOME") + "/.local/share/openjk/base/"

engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_data_dir = engineer_dir + "JediAcademy/GameData/"
s_appid = "6020"

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
		s_download = call("x-terminal-emulator -e './steamcmd.sh +@sSteamCmdForcePlatformType windows +login " + user + " +force_install_dir " + engineer_dir + "JediAcademy/ +app_update " + s_appid + " validate +quit'", shell=True)
	while os.path.isdir(game_data_dir) == False:
		time.sleep(2)
	symlink()
	launchers()

def symlink():
	for binary in next(os.walk(engine_dir))[2]:
		if os.path.exists(game_data_dir + binary) == False:
			print("symlinking " + binary)
			os.symlink(engine_dir + binary, game_data_dir + binary)
		if os.path.isdir(local_openjk_dir) == False:
			os.makedirs(local_openjk_dir)
		for library in next(os.walk(engine_dir + "OpenJK/"))[2]:
			if os.path.exists(local_openjk_dir + library) == False:
				print("symlinking " + library)
				os.symlink(engine_dir + "OpenJK/" + library, local_openjk_dir + library)

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	if os.uname()[4] == "x86_64":
		print("symlinking desktop amd64")
		os.symlink(self_dir + "openjk_amd64_sp.desktop", desk_dir + "/openjk_amd64_sp.desktop")
		os.symlink(self_dir + "openjk_amd64_sp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_sp.desktop")
		os.symlink(self_dir + "openjk_amd64_mp.desktop", desk_dir + "/openjk_amd64_mp.desktop")
		os.symlink(self_dir + "openjk_amd64_mp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_mp.desktop")
	else:
		print("symlinking desktop i386")
		os.symlink(self_dir + "openjk_i386_sp.desktop", desk_dir + "/openjk_i386_sp.desktop")
		os.symlink(self_dir + "openjk_i386_sp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_i386_sp.desktop")
		os.symlink(self_dir + "openjk_i386_mp.desktop", desk_dir + "/openjk_i386_mp.desktop")
		os.symlink(self_dir + "openjk_i386_mp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_i386_mp.desktop")
		
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

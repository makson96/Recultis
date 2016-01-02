#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, tarfile, time, shutil, urllib.request
from subprocess import call, check_output

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
local_openjk_dir = os.getenv("HOME") + "/.local/share/openjk/base/"
engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_dir = engineer_dir + "JediAcademy/"
s_appid = "6020"

def prepare_engine():
	for binary in next(os.walk(engineer_dir + "tmp/JediAcademy/"))[2]:
		shutil.copy(engineer_dir + "tmp/JediAcademy/" + binary, game_dir + "GameData/" + binary)
	for directory in next(os.walk(engineer_dir + "tmp/JediAcademy/"))[1]:
		try:
			shutil.rmtree(game_dir + "GameData/" + directory)
		except:
			pass
		shutil.copytree(engineer_dir + "tmp/JediAcademy/" + directory, game_dir + "GameData/" + directory, symlinks=True)
	shutil.rmtree(engineer_dir + "tmp")

def start_steam(user):
	print(user)
	steamcmd = call("x-terminal-emulator -e 'python3 " + self_dir + "steam.py " + user + " " + s_appid + " " + engineer_dir + " " + game_dir + "'", shell=True)
	while os.path.isdir(game_dir + "GameData/") == False:
		time.sleep(2)
	#symlink()
	launchers()

def symlink():
	for binary in next(os.walk(engine_dir))[2]:
		if os.path.exists(game_dir + "GameData/" + binary) == False:
			print("symlinking " + binary)
			os.symlink(engine_dir + binary, game_dir + "GameData/" + binary)
	if os.path.isdir(local_openjk_dir) == False:
		os.makedirs(local_openjk_dir)
	for library in next(os.walk(engine_dir + "OpenJK/"))[2]:
		if os.path.exists(local_openjk_dir + library) == False:
			print("symlinking " + library)
			os.symlink(engine_dir + "OpenJK/" + library, local_openjk_dir + library)

def launchers():
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "jediacademy/openjk_amd64_sp.desktop", desk_dir + "/openjk_amd64_sp.desktop")
	shutil.copy(self_dir + "jediacademy/openjk_amd64_sp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_sp.desktop")
	shutil.copy(self_dir + "jediacademy/openjk_amd64_mp.desktop", desk_dir + "/openjk_amd64_mp.desktop")
	shutil.copy(self_dir + "jediacademy/openjk_amd64_mp.desktop", os.getenv("HOME") + "/.local/share/applications/openjk_amd64_mp.desktop")
		
	msgBox = QMessageBox.information(qw, "Game is ready", "Have fun!")
	qw.close()

class Game:
	
	nested = 0
	
	def __init__(self, rootWindow = 0, nested = 0):
		if os.path.isdir(engineer_dir) == False:
			os.makedirs(engineer_dir)
		if os.path.isdir(game_dir) == False:
			os.makedirs(game_dir)
		if os.path.isdir(game_dir + "GameData/") == False:
			os.makedirs(game_dir + "GameData/")
		self.engine(rootWindow, nested)
		self.data(rootWindow, nested)
		
	def engine(self, rootWindow = 0, nested = 0):
		self.nested = nested
		if self.nested == 0:
			s_app = QApplication(sys.argv)
		else:
			rootWindow.hide()
		qw = QWidget()
		#Window about game engine installation
		rootWindow.hide()
		install_engine_inform = QMessageBox.information(qw, "Installing engine", "After you click OK, game engine will be downloaded and installed. It may take a while.", QMessageBox.Ok)
		if QMessageBox.Ok:
			link_file = open(self_dir + "jediacademy/link.txt")
			link = link_file.read()
			#try:
			if os.path.isfile(local_openjk_dir) == False:
				urllib.request.urlretrieve(link, engineer_dir + "openjk.tar.xz")
				tar = tarfile.open(engineer_dir + "openjk.tar.xz")
				tar.extractall(engineer_dir + "tmp")
				tar.close()
			os.remove(engineer_dir + "openjk.tar.xz")
			prepare_engine()
		#except:
		#	print("Engine file not found please use latest version of Free-Engineer")
		if self.nested == 0:
			s_app.exec_()
	
	def data(self, rootWindow = 0, nested = 0):
		global qw
		self.nested = nested
		if self.nested == 0:
			s_app = QApplication(sys.argv)
		else:
			rootWindow.show()
		#Window for choosing game data source
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

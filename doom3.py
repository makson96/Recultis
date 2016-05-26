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
engineer_dir = os.getenv("HOME") + "/.free-engineer/"
game_dir = engineer_dir + "doom3/"
s_appid = "208200"

def prepare_engine():
	print("prepare engine")
	try:
		os.remove(game_dir + "RBDoom3BFG")
		shutil.rmtree(game_dir + "lib")
	except:
		pass
	shutil.copy2(engineer_dir + "tmp/rbdoom-3-bfg/RBDoom3BFG", game_dir + "RBDoom3BFG")
	shutil.copytree(engineer_dir + "tmp/rbdoom-3-bfg/lib", game_dir + "lib", symlinks=True)
	shutil.rmtree(engineer_dir + "tmp")

def start_steam(user):
	print(user)
	steamcmd = call("x-terminal-emulator -e 'python3 " + self_dir + "steam.py " + user + " " + s_appid + " " + engineer_dir + " " + game_dir + "'", shell=True)
	while os.path.isdir(game_dir + "base/") == False:
		time.sleep(2)
	launchers()

def launchers():
	print("copy icon")
	if os.path.isdir(os.getenv("HOME") + "/.icons") == False:
		os.makedirs(os.getenv("HOME") + "/.icons")
	if os.path.isdir(os.getenv("HOME") + "/.local/share/applications/") == False:
		os.makedirs(os.getenv("HOME") + "/.local/share/applications/")
	shutil.copy(self_dir + "doom3/rbdoom-3-bfg.png", os.getenv("HOME") + "/.icons/rbdoom-3-bfg.png")
	print("make_launchers")
	desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
	shutil.copy(self_dir + "doom3/doom3.desktop", desk_dir + "/doom3.desktop")
	shutil.copy(self_dir + "doom3/doom3.desktop", os.getenv("HOME") + "/.local/share/applications/doom3.desktop")
	qw.close()

class Game:
	
	nested = 0
	
	def __init__(self, rootWindow = 0, nested = 0):
		if os.path.isdir(engineer_dir) == False:
			os.makedirs(engineer_dir)
		if os.path.isdir(game_dir) == False:
			os.makedirs(game_dir)
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
			link_file = open(self_dir + "doom3/link.txt")
			link = link_file.read()
			if os.path.isfile(engineer_dir + "rbdoom-3-bfg.tar.xz") == False:
				urllib.request.urlretrieve(link, engineer_dir + "rbdoom-3-bfg.tar.xz")
				tar = tarfile.open(engineer_dir + "rbdoom-3-bfg.tar.xz")
				tar.extractall(engineer_dir + "tmp")
				tar.close()
			os.remove(engineer_dir + "rbdoom-3-bfg.tar.xz")
			prepare_engine()
	
	def data(self, rootWindow = 0, nested = 0):
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

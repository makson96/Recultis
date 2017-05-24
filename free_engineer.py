#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, _thread, time, urllib

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from tools import update_check, status

free_engine_version = "1.0.0pre"

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
engineer_dir = os.getenv("HOME") + "/.free-engineer/"

r0_description = "Jedi Knight: Jedi Academy on OpenJK engine"
r1_description = "The Elder Scrolls III: Morrowind on OpenMW engine"
r2_description = "Doom 3 BFG on RBDOOM-3-BFG"

class Window(QWidget):
	
	radio_list = []
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		self.app_staus_label = QLabel("Free Enginner status is: Waiting...")
		self.app_updateButton = QPushButton("Update Now")
		self.app_updateButton.setEnabled(False)
		choose_game_Label = QLabel("Choose the game to install:")
		game_group = QButtonGroup()
		self.r0 = QRadioButton(r0_description)
		game_group.addButton(self.r0)
		self.r1 = QRadioButton(r1_description)
		game_group.addButton(self.r1)
		self.r2 = QRadioButton(r2_description)
		game_group.addButton(self.r2)
		self.r0.setChecked(True)
		choose_data_Label = QLabel("Choose digital distribution platform to download game data:")
		data_group = QButtonGroup()
		self.r0a = QRadioButton("Steam")
		data_group.addButton(self.r0a)
		self.r0a.setChecked(True)
		loginLabel = QLabel("Login:")
		self.loginText = QLineEdit()
		passwordLabel = QLabel("Password:")
		self.passwordText = QLineEdit()
		self.passwordText.setEchoMode(QLineEdit.Password)
		statusLabel1 = QLabel("Status: ")
		self.statusLabel2 = QLabel("Waiting for user action")
		self.statusLabel2.setAlignment(Qt.AlignCenter)
		self.progress = QProgressBar(self)
		self.installButton = QPushButton("Install")
		self.exitButton = QPushButton("Exit")
		choose_game_Label = QLabel("Choose the game to install:")
		
		vbox1 = QVBoxLayout()
		hbox0 = QHBoxLayout()
		hbox1 = QHBoxLayout()
		grid1 = QGridLayout()
		
		hbox0.addWidget(self.app_staus_label)
		hbox0.addWidget(self.app_updateButton)
		vbox1.addLayout(hbox0)
		vbox1.addWidget(choose_game_Label)
		vbox1.addWidget(self.r0)
		vbox1.addWidget(self.r1)
		vbox1.addWidget(self.r2)
		vbox1.addWidget(choose_data_Label)
		vbox1.addWidget(self.r0a)
		grid1.addWidget(loginLabel, 0, 0)
		grid1.addWidget(self.loginText, 0, 1)
		grid1.addWidget(passwordLabel, 1, 0)
		grid1.addWidget(self.passwordText, 1, 1)
		grid1.addWidget(statusLabel1, 2, 0)
		grid1.addWidget(self.statusLabel2, 2, 1)
		vbox1.addLayout(grid1)
		vbox1.addWidget(self.progress)
		hbox1.addWidget(self.installButton)
		hbox1.addWidget(self.exitButton)
		vbox1.addLayout(hbox1)
		
		self.installButton.clicked.connect(self.choose)
		self.exitButton.clicked.connect(self.close)
 
		self.setLayout(vbox1)
		self.setWindowTitle("Free Engineer " + free_engine_version)
		
		#After Windows is drawn, lets check status of the games
		self.radio_list = [self.r0, self.r1, self.r2]
		self.update_game_thread = UpdateApp(self.app_staus_label, self.app_updateButton, self.installButton, self.radio_list)
		self.update_game_thread.start()
	
	def choose(self):
		self.installButton.setEnabled(False)
		if self.r0.isChecked():
			from jediacademy import chosen_game
			game = "jediacademy"
		elif self.r1.isChecked():
			from morrowind import chosen_game
			game = "morrowind"
		elif self.r2.isChecked():
			from doom3 import chosen_game
			game = "doom3"
		if os.path.isdir(engineer_dir) == False:
			os.makedirs(engineer_dir)
		_thread.start_new_thread(chosen_game.start, ("steam", str(self.loginText.text()), str(self.passwordText.text())))
		print("new thread started")
		percent = 0
		time.sleep(1)
		while percent != 100:
			result, percent = status.check(game)
			time.sleep(1)
			self.statusLabel2.setText(result)
			self.progress.setValue(percent)
			if "Error" in result:
				break
		#Installation is complete. Unlock Intall button and update games descriptions
		self.installButton.setEnabled(True)
		self.r0.setText(game_descriptor(0))
		self.r1.setText(game_descriptor(1))
		self.r2.setText(game_descriptor(2))

class UpdateApp(QThread):

	def __init__(self, status_label, update_button, install_button, radio_list):
		QThread.__init__(self)
		self.status_label = status_label
		self.update_button = update_button
		self.install_button = install_button
		self.radio_list = radio_list

	def __del__(self):
		self.wait()

	def run(self):
		#Check for internet connection
		try:
			urllib.request.urlopen("https://github.com", timeout=1)
			connection = 1
		except urllib.request.URLError:
			connection = 0
			self.status_label.setText("Free Enginner status is: No internet connection")
			self.install_button.setEnabled(False)
		if connection == 1:
			#Check if update is available
			v_major = str(int(free_engine_version[0]) + 1) + ".0.0"
			v_minor = free_engine_version[0:2] + str(int(free_engine_version[2]) + 1) + ".0"
			v_patch = free_engine_version[0:4] + str(int(free_engine_version[4]) + 1)
			update_list = [v_major, v_minor, v_patch]
			patch_url = ""
			for potential_patch in update_list:
				try:
					patch_url = "https://github.com/makson96/free-engineer/archive/" + potential_patch + ".tar.gz"
					print(patch_url)
					urllib.request.urlopen(patch_url, timeout=1)
					self.update_button.setEnabled(True)
					self.status_label.setText("Free Enginner status is: Updata available")
					break					
				except urllib.request.URLError:
					patch_url = ""
			if patch_url == "":
				self.status_label.setText("Free Enginner status is: Up to date")
			#Check game status (if internet connection)
			self.radio_list[0].setText(game_descriptor(0))
			self.radio_list[1].setText(game_descriptor(1))
			self.radio_list[2].setText(game_descriptor(2))

def game_descriptor(game_nr):
	game_description = ""
	if game_nr == 0:
		game_description = r0_description + " (" + update_check.start("jediacademy", self_dir) + ")"
	elif game_nr == 1:
		game_description = r1_description + " (" + update_check.start("morrowind", self_dir) + ")"
	elif game_nr == 2:
		game_description = r2_description + " (" + update_check.start("doom3", self_dir) + ")"
	return game_description
	
app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())

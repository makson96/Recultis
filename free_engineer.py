#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, _thread, time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from tools import status, update_check

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
engineer_dir = os.getenv("HOME") + "/.free-engineer/"

class Window(QWidget):
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		choose_game_Label = QLabel("Choose the game to install:")
		game_group = QButtonGroup()
		self.r0 = QRadioButton("Jedi Knight: Jedi Academy on OpenJK engine (")# + update_check.start("jediacademy") + ")")
		game_group.addButton(self.r0)
		self.r1 = QRadioButton("The Elder Scrolls III: Morrowind on OpenMW engine (" + update_check.start("morrowind") + ")")
		game_group.addButton(self.r1)
		self.r2 = QRadioButton("Doom 3 BFG on RBDOOM-3-BFG (")# + update_check.start("doom3") + ")")
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
		statusLabel = QLabel("Status: ")
		self.status1Label = QLabel("Waiting for user action")
		self.progress = QProgressBar(self)
		self.installButton = QPushButton("Install")
		self.exitButton = QPushButton("Exit")
		
		vbox1 = QVBoxLayout()
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()
		hbox4 = QHBoxLayout()

		vbox1.addWidget(choose_game_Label)
		vbox1.addWidget(self.r0)
		vbox1.addWidget(self.r1)
		vbox1.addWidget(self.r2)
		vbox1.addWidget(choose_data_Label)
		vbox1.addWidget(self.r0a)
		hbox1.addWidget(loginLabel)
		hbox1.addWidget(self.loginText)
		vbox1.addLayout(hbox1)
		hbox2.addWidget(passwordLabel)
		hbox2.addWidget(self.passwordText)
		vbox1.addLayout(hbox2)
		hbox3.addWidget(statusLabel)
		hbox3.addWidget(self.status1Label)
		vbox1.addLayout(hbox3)
		vbox1.addWidget(self.progress)
		hbox4.addWidget(self.installButton)
		hbox4.addWidget(self.exitButton)
		vbox1.addLayout(hbox4)
		
		self.installButton.clicked.connect(self.choose)
		self.exitButton.clicked.connect(self.close)
 
		mainLayout = QGridLayout()
		mainLayout.addLayout(vbox1, 0, 1)
		
		self.setLayout(mainLayout)
		self.setWindowTitle("Free Engineer")
	
	def choose(self):
		if self.r0.isChecked():
			from jediacademy import chosen_game
		elif self.r1.isChecked():
			from morrowind import chosen_game
		elif self.r2.isChecked():
			from doom3 import chosen_game
		if os.path.isdir(engineer_dir) == False:
			os.makedirs(engineer_dir)
		_thread.start_new_thread(chosen_game.start, ("steam", str(self.loginText.text()), str(self.passwordText.text())))
		print("new_thread_started")
		deb_info = chosen_game.info(["deb_file_path", "deb_url_path"])
		deb_file_path = deb_info[0]
		deb_url_path = deb_info[1]
		percent = 0
		while percent != 100:
			time.sleep(2)
			status.write_status(engineer_dir, deb_file_path, deb_url_path)
			result_list = status.read_status(engineer_dir)
			result = result_list[0]
			percent = result_list[1]
			self.progress.setValue(percent)
		self.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen = Window()
	screen.show()
	sys.exit(app.exec_())

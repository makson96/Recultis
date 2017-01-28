#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, urllib.request

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

games = [ "Jedi Knight: Jedi Academy on OpenJK engine", "The Elder Scrolls III: Morrowind on OpenMW engine", "Doom 3 BFG on RBDOOM-3-BFG" ]
self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

class Window(QWidget):
	
	#status_list is a list of lists containing - status, target_url, target_file for each game
	status_list = []
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		nameLabel = QLabel("Choose the game to install:")
		game_group = QButtonGroup()
		self.status_list.append(self.check_status(games[0]))
		self.r0 = QRadioButton(games[0] + " (" + self.status_list[0][0] + ")")
		game_group.addButton(self.r0)
		self.status_list.append(self.check_status(games[1]))
		self.r1 = QRadioButton(games[1] + " (" + self.status_list[1][0] + ")")
		game_group.addButton(self.r1)
		self.status_list.append(self.check_status(games[2]))
		self.r2 = QRadioButton(games[2] + " (" + self.status_list[2][0] + ")")
		game_group.addButton(self.r2)
		self.r0.setChecked(True)
		self.chooseButton = QPushButton("Choose")
		self.exitButton = QPushButton("Exit")
		
		vbox1 = QVBoxLayout()
		hbox1 = QHBoxLayout()

		vbox1.addWidget(nameLabel)
		vbox1.addWidget(self.r0)
		vbox1.addWidget(self.r1)
		vbox1.addWidget(self.r2)
		hbox1.addWidget(self.chooseButton)
		hbox1.addWidget(self.exitButton)
		vbox1.addLayout(hbox1)
		
		self.chooseButton.clicked.connect(self.choose)
		self.exitButton.clicked.connect(self.close)
 
		mainLayout = QGridLayout()
		mainLayout.addLayout(vbox1, 0, 1)
		
		self.setLayout(mainLayout)
		self.setWindowTitle("Free Engineer")
	
	def check_status(self, game):
		if game == games[0]:
			target_url = "https://raw.githubusercontent.com/makson96/free-engineer/master/jediacademy/link.txt"
			target_file = self_dir + "jediacademy/link.txt"
			game_dir = os.getenv("HOME") + "/.free-engineer/JediAcademy/"
		elif game == games[1]:
			target_url = "https://raw.githubusercontent.com/makson96/free-engineer/master/morrowind/link.txt"
			target_file = self_dir + "morrowind/link.txt"
			game_dir = os.getenv("HOME") + "/.free-engineer/morrowind/"
		elif game == games[2]:
			target_url = "https://raw.githubusercontent.com/makson96/free-engineer/master/doom3/link.txt"
			target_file = self_dir + "doom3/link.txt"
			game_dir = os.getenv("HOME") + "/.free-engineer/doom3/"
		data = urllib.request.urlopen(target_url)
		download_link_new = data.read().decode("utf-8")
		link_file = open(target_file)
		download_link_old = link_file.read()
		print(download_link_new)
		print(download_link_old)
		if os.path.isdir(game_dir) == True:
			status = "Installed"
			if download_link_old != download_link_new:
				status = "Update available"
		else:
			status = "Not installed"
			if download_link_old != download_link_new:
				urllib.request.urlretrieve(target_url, target_file)
		return [status,target_url,target_file]
	
	def choose(self):
		if self.r0.isChecked():
			from jediacademy import chosen_game
			if self.status_list[0][0] == "Update available":
				urllib.request.urlretrieve(self.status_list[0][1], self.status_list[0][2])
		elif self.r1.isChecked():
			from morrowind import chosen_game
			if self.status_list[1][0] == "Update available":
				urllib.request.urlretrieve(self.status_list[1][1], self.status_list[1][2])
		elif self.r2.isChecked():
			from doom3 import chosen_game
			if self.status_list[2][0] == "Update available":
				urllib.request.urlretrieve(self.status_list[2][1], self.status_list[2][2])
		download_game = chosen_game.Game(self, 1)
		self.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen = Window()
	screen.show()
	sys.exit(app.exec_())

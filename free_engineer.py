#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
from subprocess import check_output, CalledProcessError, call#, PIPE

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

games = [ ["Jedi Knight: Jedi Academy on OpenJK engine", "openjk"], ["Aliens vs Predator Classic 2000 on avp", "avp"], ["Doom 3 BFG on RBDOOM-3-BFG", "rbdoom-3-bfg"], ["The Elder Scrolls III: Morrowind on OpenMW","openmw-makson"]]

class Window(QWidget):
	
	game_nr = 0
	engine_installed = 0
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		nameLabel = QLabel("Choose the game to install:")
		game_group = QButtonGroup()
		self.r0 = QRadioButton(games[0][0])
		game_group.addButton(self.r0)
		self.r1 = QRadioButton(games[1][0])
		game_group.addButton(self.r1)
		self.r2 = QRadioButton(games[2][0])
		game_group.addButton(self.r2)
		self.r3 = QRadioButton(games[3][0])
		game_group.addButton(self.r3)
		self.r0.setChecked(True)
		self.chooseButton = QPushButton("Choose")
		self.exitButton = QPushButton("Exit")
		
		vbox1 = QVBoxLayout()
		hbox1 = QHBoxLayout()

		vbox1.addWidget(nameLabel)
		vbox1.addWidget(self.r0)
		vbox1.addWidget(self.r1)
		vbox1.addWidget(self.r2)
		vbox1.addWidget(self.r3)
		hbox1.addWidget(self.chooseButton)
		hbox1.addWidget(self.exitButton)
		vbox1.addLayout(hbox1)
		
		self.chooseButton.clicked.connect(self.choose)
		self.exitButton.clicked.connect(self.close)
 
		mainLayout = QGridLayout()
		mainLayout.addLayout(vbox1, 0, 1)
		
		self.setLayout(mainLayout)
		self.setWindowTitle("Free Engineer")
	
	def choose(self):
		if self.r0.isChecked():
			self.game_nr = 0
		elif self.r1.isChecked():
			self.game_nr = 1
		elif self.r2.isChecked():
			self.game_nr = 2
		elif self.r3.isChecked():
			self.game_nr = 3
		
		try:
			check_dep = check_output("dpkg-query -W --showformat='${Status}\n' " + games[self.game_nr][1], shell=True)
			result = str(check_dep)
			print(result)
			result = result[2:-3]
		except CalledProcessError as e:
			print(e.returncode)
			result = "non-installed1"
		print(result)
		if result != "install ok installed":
			dep_pack = QMessageBox.question(self, "Install Engine", "You need to install following packages (root password required):<br><b>" + games[self.game_nr][1] +"</b><br>Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if dep_pack == QMessageBox.Yes:
				print("Yes")
				dep_install = call("""x-terminal-emulator -e 'gksudo "apt-get -y install """  + games[self.game_nr][1] + """"'""", shell=True)
				self.engine_installed = 1
			else:
				print("No")
				self.engine_installed = 0
		else:
			self.engine_installed = 1

		if self.engine_installed == 1:
			if self.game_nr == 0:
				import openjk as game_data
			elif self.game_nr == 1:
				import avp as game_data
			elif self.game_nr == 2:
				import doom3 as game_data
			elif self.game_nr == 3:
				import morrowind as game_data
			download_data = game_data.Steam(self, 1)
			self.close()	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen = Window()
	screen.show()
	sys.exit(app.exec_())

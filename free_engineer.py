#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os, time
from subprocess import check_output, CalledProcessError, call

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

games = [ ["Jedi Knight: Jedi Academy on OpenJK engine", "openjk"],
["Aliens vs Predator Classic 2000 on avp", "avp"],
["Doom 3 BFG on RBDOOM-3-BFG", "rbdoom-3-bfg"],
["The Elder Scrolls III: Morrowind on OpenMW","openmw-makson"],
["Tomb Raider I","openraider"],
["Tomb Raider II","openraider"],
["Tomb Raider III","openraider"]]

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
		self.r4 = QRadioButton(games[4][0])
		game_group.addButton(self.r4)
		self.r5 = QRadioButton(games[5][0])
		game_group.addButton(self.r5)
		self.r6 = QRadioButton(games[6][0])
		game_group.addButton(self.r6)
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
		vbox1.addWidget(self.r4)
		vbox1.addWidget(self.r5)
		vbox1.addWidget(self.r6)
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
		elif self.r4.isChecked():
			self.game_nr = 4
		elif self.r5.isChecked():
			self.game_nr = 5
		elif self.r6.isChecked():
			self.game_nr = 6
		
		self.check_dep()
		if self.engine_installed == 0:
			dep_pack = QMessageBox.question(self, "Install Engine", "You need to install following packages (root password required):<br><b>" + games[self.game_nr][1] +"</b><br>Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if dep_pack == QMessageBox.Yes:
				print("Yes")
				dep_install = call("""x-terminal-emulator -e 'gksudo "apt-get -y install """  + games[self.game_nr][1] + """"'""", shell=True)
				print("""x-terminal-emulator -e 'gksudo "apt-get -y install """  + games[self.game_nr][1] + """"'""")
				while self.engine_installed == 0:
					self.check_dep()
					time.sleep(2)
			else:
				print("No")
				self.check_dep()

		if self.engine_installed == 1:
			if self.game_nr == 0:
				import openjk as game_data
			elif self.game_nr == 1:
				import avp as game_data
			elif self.game_nr == 2:
				import doom3 as game_data
			elif self.game_nr == 3:
				import morrowind as game_data
			elif self.game_nr == 4 or self.game_nr == 5 or self.game_nr == 6:
				import tombraider as game_data
			
			if self.game_nr == 4:
				download_data = game_data.Steam(self, 1, 1)
			elif self.game_nr == 5:
				download_data = game_data.Steam(self, 1, 2)
			elif self.game_nr == 6:
				download_data = game_data.Steam(self, 1, 3)
			else:
				download_data = game_data.Steam(self, 1)
			self.close()
	
	def check_dep(self):
		try:
			check_dep = check_output("dpkg-query -W --showformat='${Status}\n' " + games[self.game_nr][1], shell=True)
			result = str(check_dep)
			print(result)
			result = result[2:-3]
		except CalledProcessError as e:
			print(e.returncode)
			result = "non-installed1"
		print(result)
		if result == "install ok installed":
			self.engine_installed = 1
		else:
			self.engine_installed = 0
		print(self.engine_installed)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen = Window()
	screen.show()
	sys.exit(app.exec_())

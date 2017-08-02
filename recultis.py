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

recultis_version = "1.1.0pre"

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
recultis_dir = os.getenv("HOME") + "/.recultis/"

from jediacademy.chosen_game import name
r0_name = name
from morrowind.chosen_game import name
r1_name = name
from doom3.chosen_game import name
r2_name = name

class Window(QWidget):
	
	radio_list = []
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		self.app_staus_label = QLabel("Recultis status is: Checking for update...")
		self.app_updateButton = QPushButton("Update Now")
		self.app_updateButton.setEnabled(False)
		choose_game_Label = QLabel("Choose the game to install:")
		game_group = QButtonGroup()
		self.r0 = QRadioButton(r0_name + " (Checking for update...)")
		self.r0.toggled.connect(self.r0_clicked)
		game_group.addButton(self.r0)
		self.r1 = QRadioButton(r1_name + " (Checking for update...)")
		self.r1.toggled.connect(self.r1_clicked)
		game_group.addButton(self.r1)
		self.r2 = QRadioButton(r2_name + " (Checking for update...)")
		self.r2.toggled.connect(self.r2_clicked)
		game_group.addButton(self.r2)
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
		
		#Default game selection
		self.description_image = QLabel() 
		self.description_label = QLabel()
		self.description_steam_link = QLabel()
		self.description_steam_link.setOpenExternalLinks(True)
		self.r0.setChecked(True)
		
		vbox1 = QVBoxLayout()
		vbox2 = QVBoxLayout()
		hbox0 = QHBoxLayout()
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		grid1 = QGridLayout()
		
		hbox1.addWidget(self.app_staus_label)
		hbox1.addWidget(self.app_updateButton)
		vbox1.addLayout(hbox1)
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
		hbox2.addWidget(self.installButton)
		hbox2.addWidget(self.exitButton)
		vbox1.addLayout(hbox2)
		vbox2.addWidget(self.description_image)
		vbox2.addWidget(self.description_label)
		vbox2.addWidget(self.description_steam_link)
		hbox0.addLayout(vbox1)
		hbox0.addLayout(vbox2)
		
		self.app_updateButton.clicked.connect(self.autoupdate)
		self.installButton.clicked.connect(self.choose)
		self.exitButton.clicked.connect(self.close)
 
		self.setLayout(hbox0)
		self.setWindowTitle("Recultis " + recultis_version)
		
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
		if os.path.isdir(recultis_dir) == False:
			os.makedirs(recultis_dir)
		print("tarting new thread, which will install: " + game)
		_thread.start_new_thread(chosen_game.start, ("steam", str(self.loginText.text()), str(self.passwordText.text())))
		percent_update_loop(game)

	def autoupdate(self):
		self.app_staus_label.setText("Recultis status is: Updating. Please wait.")
		patch_link_file = open(self_dir + "patch_link.txt", "r")
		patch_link = patch_link_file.read()
		from tools import update_tool
		update_tool.autoupdate(self_dir, patch_link)
		QMessageBox.information(self, "Message", "Update complete. Recultis will now turn off. Please start it again to apply patch.")
		self.close()
	
	def r0_clicked(self, enabled):
		if enabled:
			from jediacademy.chosen_game import description, screenshot_path, steam_link
			description_pixmap = QPixmap(screenshot_path)
			self.description_image.setPixmap(description_pixmap)
			self.description_label.setText(description)
			self.description_steam_link.setText("<a href='" + steam_link + "'>Link to the game on Steam.</a>")
	
	def r1_clicked(self, enabled):
		if enabled:
			from morrowind.chosen_game import description, screenshot_path, steam_link
			description_pixmap = QPixmap(screenshot_path)
			self.description_image.setPixmap(description_pixmap)
			self.description_label.setText(description)
			self.description_steam_link.setText("<a href='" + steam_link + "'>Link to the game on Steam.</a>")
	
	def r2_clicked(self, enabled):
		if enabled:
			from doom3.chosen_game import description, screenshot_path, steam_link
			description_pixmap = QPixmap(screenshot_path)
			self.description_image.setPixmap(description_pixmap)
			self.description_label.setText(description)
			self.description_steam_link.setText("<a href='" + steam_link + "'>Link to the game on Steam.</a>")

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
			urllib.request.urlopen("https://github.com", timeout=3)
			connection = 1
		except urllib.request.URLError:
			connection = 0
			self.status_label.setText("Recultis status is: No internet connection")
			self.install_button.setEnabled(False)
		if connection == 1:
			#Check if update is available
			v_major = str(int(recultis_version[0]) + 1) + ".0.0"
			v_minor = recultis_version[0:2] + str(int(recultis_version[2]) + 1) + ".0"
			v_patch = recultis_version[0:4] + str(int(recultis_version[4]) + 1)
			update_list = [v_major, v_minor, v_patch]
			patch_url = ""
			for potential_patch in update_list:
				try:
					patch_url = "https://github.com/makson96/Recultis/archive/v" + potential_patch + ".tar.gz"
					urllib.request.urlopen(patch_url, timeout=1)
					patch_link_file = open(self_dir + "patch_link.txt", "w")
					patch_link_file.write(patch_url)
					patch_link_file.close()
					self.update_button.setEnabled(True)
					self.status_label.setText("Recultis status is: Updata available")
					break					
				except urllib.request.URLError:
					patch_url = ""
			if patch_url == "":
				self.status_label.setText("Recultis status is: Up to date")
			#Check game status (if internet connection)
			self.radio_list[0].setText(game_descriptor(0))
			self.radio_list[1].setText(game_descriptor(1))
			self.radio_list[2].setText(game_descriptor(2))

class AskWindow(QMainWindow):
	#Available reasons: 1 - Steam Guard, ...
	
	reason = 0
	game = "No title"
	
	def __init__(self, reason, game, parent=None):
		super(AskWindow, self).__init__(parent)
		self.reason = reason
		self.game = game
		if self.reason == 1:
			self.title = 'Steam Guard authentication.'
			self.MessageLabel = QLabel("Please provide Steam Guard code, which was just send via email.", self)
		self.setWindowTitle(self.title)
		self.textbox = QLineEdit(self)
		self.button = QPushButton('OK', self)
		self.button.clicked.connect(self.on_click)
		self.MessageLabel.move(0,0)
		self.MessageLabel.resize(self.MessageLabel.minimumSizeHint())
		self.textbox.move(0,27)
		self.textbox.resize(400, 30)
		self.button.move(150,60)
		self.setGeometry(250, 250, 400, 90)
		
	def on_click(self):
		steam_guard_key = self.textbox.text()
		steam_guard_key_file = open(recultis_dir + "steam_guard_key.txt", "w")
		steam_guard_key_file.write(steam_guard_key)
		steam_guard_key_file.close()
		self.close()
		time.sleep(1)
		percent_update_loop(self.game)

def game_descriptor(game_nr):
	game_description = ""
	if game_nr == 0:
		game_description = r0_name + " (" + update_check.start("jediacademy", self_dir) + ")"
	elif game_nr == 1:
		game_description = r1_name + " (" + update_check.start("morrowind", self_dir) + ")"
	elif game_nr == 2:
		game_description = r2_name + " (" + update_check.start("doom3", self_dir) + ")"
	return game_description

def percent_update_loop(game):
	time.sleep(0.5)
	percent = 0
	while percent != 100:
		result, percent = status.check(game)
		time.sleep(1)
		screen.statusLabel2.setText(result)
		screen.progress.setValue(percent)
		if "Warning" in result:
			print(result)
			nw = AskWindow(1, game, screen) #This should not allways be 1
			nw.show()
			break
		elif "Error" in result:
			print(result)
			break
	#Installation is complete or error occured. Unlock Intall button and update games descriptions
	if (percent == 100) or ("Error" in result):
		screen.installButton.setEnabled(True)
		time.sleep(1)
		screen.r0.setText(game_descriptor(0))
		screen.r1.setText(game_descriptor(1))
		screen.r2.setText(game_descriptor(2))

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())

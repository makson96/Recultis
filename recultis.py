#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, _thread, time, urllib, importlib
from subprocess import check_output, call

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from tools import update_do, status
from games import installer

recultis_version = "1.2.4pre"

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
recultis_dir = os.getenv("HOME") + "/.recultis/"

#This is the list of lists. It is sorted in alphabetic order. Every position is list wich contains game name (as game directory name) and game status.
game_list = installer.get_game_list()

class Window(QWidget):
	
	game_r_list = []
	push_buttons_list = []
	installing_game = "" #This will track which game name is currently installed
	clicked_game = "" #This will track which game name is currently clicked
	playing_game = "" #This will track which game name is currently playing
	
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		
		self.app_staus_label = QLabel("Recultis status is: Checking for update...")
		self.app_updateButton = QPushButton("Update Now")
		self.app_updateButton.setEnabled(False)
		self.app_create_launcher = QPushButton("Add Desktop Launcher")
		choose_game_box = QGroupBox("Choose the game to install:")
		for game_position in game_list:
			self.game_r_list.append(QRadioButton(update_do.game_update_desc(game_position)))
			self.game_r_list[-1].toggled.connect(self.game_radiobutton_effect)
		choose_data_box = QGroupBox("Choose digital distribution platform to download game data:")
		self.r0a = QRadioButton("None needed")
		self.r0a.setEnabled(False)
		self.r0a.toggled.connect(self.r0a_clicked)
		self.r1a = QRadioButton("Steam")
		self.r1a.setChecked(True)
		self.r1a.toggled.connect(self.r1a_clicked)
		self.shop_r_list = [self.r0a, self.r1a]
		loginLabel = QLabel("Login:")
		self.loginText = QLineEdit()
		passwordLabel = QLabel("Password:")
		self.passwordText = QLineEdit()
		self.passwordText.setEchoMode(QLineEdit.Password)
		statusLabel1 = QLabel("Status: ")
		self.statusLabel2 = QLabel("Waiting for user action")
		self.statusLabel2.setAlignment(Qt.AlignCenter)
		self.progress = QProgressBar(self)
		self.playButton = QPushButton("Play")
		self.launcherButton = QPushButton("Add Launcher")
		self.installButton = QPushButton("Install")
		self.uninstallButton = QPushButton("Uninstall")
		self.exitButton = QPushButton("Exit")
		choose_game_Label = QLabel("Choose the game to install:")
		
		#Default game selection
		self.description_image = QLabel() 
		self.description_label = QLabel()
		self.description_shop_link = QLabel()
		self.description_shop_link.setOpenExternalLinks(True)
		self.game_r_list[0].setChecked(True)
		
		vbox1 = QVBoxLayout()
		vbox1_1 = QVBoxLayout()
		choose_game_box.setLayout(vbox1_1)
		vbox1_2 = QVBoxLayout()
		choose_data_box.setLayout(vbox1_2)
		vbox2 = QVBoxLayout()
		hbox0 = QHBoxLayout()
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		grid1 = QGridLayout()
		
		hbox1.addWidget(self.app_staus_label)
		hbox1.addWidget(self.app_updateButton)
		hbox1.addWidget(self.app_create_launcher)
		vbox1.addLayout(hbox1)
		vbox1.addWidget(choose_game_box)
		for r_button in self.game_r_list:
			vbox1_1.addWidget(r_button)
		vbox1.addWidget(choose_data_box)
		vbox1_2.addWidget(self.r0a)
		vbox1_2.addWidget(self.r1a)
		grid1.addWidget(loginLabel, 0, 0)
		grid1.addWidget(self.loginText, 0, 1)
		grid1.addWidget(passwordLabel, 1, 0)
		grid1.addWidget(self.passwordText, 1, 1)
		grid1.addWidget(statusLabel1, 2, 0)
		grid1.addWidget(self.statusLabel2, 2, 1)
		vbox1.addLayout(grid1)
		vbox1.addWidget(self.progress)
		hbox2.addWidget(self.playButton)
		hbox2.addWidget(self.launcherButton)
		hbox2.addWidget(self.installButton)
		hbox2.addWidget(self.uninstallButton)
		hbox2.addWidget(self.exitButton)
		vbox1.addLayout(hbox2)
		vbox2.addWidget(self.description_image)
		vbox2.addWidget(self.description_label)
		vbox2.addWidget(self.description_shop_link)
		hbox0.addLayout(vbox1)
		hbox0.addLayout(vbox2)
		
		self.app_updateButton.clicked.connect(self.autoupdate)
		self.app_create_launcher.clicked.connect(self.add_launcher)
		self.playButton.clicked.connect(self.play_game)
		self.launcherButton.clicked.connect(self.add_game_launcher)
		self.installButton.clicked.connect(self.install_game)
		self.uninstallButton.clicked.connect(self.uninstall_game)
		self.exitButton.clicked.connect(self.close)
 
		self.setLayout(hbox0)
		self.setWindowTitle("Recultis " + recultis_version)
		
		#After Windows is drawn, lets check status of the games
		self.push_buttons_list = [self.playButton, self.launcherButton, self.installButton, self.uninstallButton]
		self.second_thread_list = [self.app_staus_label, self.app_updateButton, self.push_buttons_list, self.game_r_list, self.r0a, self.installing_game]
		#Don't allow to update Recultis if can't write to its directory.
		if os.access(self_dir, os.W_OK):
			self.update_app_thread = SecondThread(1, self.second_thread_list)
			self.update_app_thread.start()
		else:
			self.app_staus_label.setText("Recultis status is: Update disabled")
		self.update_game_thread = SecondThread(2, self.second_thread_list)
		self.update_game_thread.start()
	
	def play_game(self):
		print("Game to be played:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				self.playing_game = game_list[r_list_nr][0]
				print(self.playing_game)
				rbutton = game_fname
			r_list_nr += 1
		game_module = importlib.import_module("games." + self.playing_game + ".game")
		launcher_cmd_list = game_module.launcher_cmd_list
		if len(launcher_cmd_list) > 1:
			print("Starting Ask Window to choose launcher")
			l_nr = self.ask_window_start(2)
			if l_nr == "no":
				print("Choose launcher windows closed without decision")
				return 0
		else:
			l_nr = 0
		print("Starting game")
		call(launcher_cmd_list[l_nr][1], shell=True)
		self.playing_game = ""
		print("Finished Playing game")

	def add_game_launcher(self):
		print("Game for which launcher will be created:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				game = game_list[r_list_nr][0]
				print(game)
				rbutton = game_fname
			r_list_nr += 1
		installer.make_launchers(game)
		QMessageBox.information(self, "Message", "Desktop and Menu launchers for selected game are now successfully created.")
	
	def install_game(self):
		global game_list
		print("Game to be installed:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				self.installing_game = game_list[r_list_nr][0]
				print(self.installing_game)
			else:
				r_list_nr += 1
		if os.path.isdir(recultis_dir) == False:
			os.makedirs(recultis_dir)
		print("starting new thread, which will install: " + self.installing_game)
		if self.r0a.isChecked():
			game_shop = "none"
		else:
			game_shop = "steam"
		#This is game install/update thread
		_thread.start_new_thread(installer.install, (self.installing_game, game_shop, str(self.loginText.text()), str(self.passwordText.text())))
		#This is thread for GUI
		self.update_status_bar_thread = SecondThread(3, self.second_thread_list)
		self.update_status_bar_thread.result_text.connect(self.statusLabel2.setText)
		self.update_status_bar_thread.percent_num.connect(self.progress.setValue)
		self.update_status_bar_thread.steam_warning.connect(self.ask_window_start)
		self.update_status_bar_thread.start()
	
	def uninstall_game(self):
		self.installButton.setEnabled(False)
		print("Game to be uninstalled:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				uninstall_game = game_list[r_list_nr][0]
				print(uninstall_game)
			r_list_nr += 1
		installer.uninstall(uninstall_game)
		self.update_game_thread = SecondThread(2, self.second_thread_list)
		self.update_game_thread.start()
		QMessageBox.information(self, "Message", "Game uninstallation complete.")

	def autoupdate(self):
		print("Starting autopupdate window")
		self.app_staus_label.setText("Recultis status is: Updating. Please wait.")
		result = self.ask_window_start(3)
		if result == "ok":
			QMessageBox.information(self, "Message", "Update complete. Recultis will now turn off. Please start it again to apply patch.")
			self.close()
	
	def add_launcher(self):
		print("Creating Recultis launcher")
		launcher_text = """[Desktop Entry]
Type=Application
Name=Recultis
Comment=Install free game engines with proprietary content.
Exec=bash -c 'cd \"""" + self_dir + """\"; python3 main.py'
Icon=recultis.png
Categories=Game;
Terminal=false"""
		desk_dir = str(check_output(['xdg-user-dir', 'DESKTOP']))[2:-3]
		desktop_file = open(desk_dir + "/recultis.desktop", "w")
		desktop_file.write(launcher_text)
		desktop_file.close()
		os.chmod(desk_dir + "/recultis.desktop", 0o755)
		menu_file = open(os.getenv("HOME") + "/.local/share/applications/recultis.desktop", "w")
		menu_file.write(launcher_text)
		menu_file.close()
		os.chmod(os.getenv("HOME") + "/.local/share/applications/recultis.desktop", 0o755)
		QMessageBox.information(self, "Message", "Desktop and Menu launchers for Recultis are now successfully created.")
	
	def game_radiobutton_effect(self, enabled):
		if enabled == False:
			return
		print("Game selected:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				self.clicked_game = game_list[r_list_nr][0]
				clicked_game_status = game_list[r_list_nr][1]
				print(self.clicked_game)
			r_list_nr += 1
		game_module = importlib.import_module("games." + self.clicked_game + ".game")
		description = game_module.description
		screenshot_path = game_module.screenshot_path
		supported_shops = game_module.shops
		description_pixmap = QPixmap(screenshot_path)
		self.description_image.setPixmap(description_pixmap)
		self.description_label.setText(description)
		#Set correct radiobuttons enabled depending on available shops
		if ("none" in supported_shops) or (clicked_game_status == 2):
			self.r0a.setEnabled(True)
		else:
			self.r0a.setEnabled(False)
		if "steam" in supported_shops:
			self.r1a.setEnabled(True)
		else:
			self.r1a.setEnabled(False)
		#Change clicked radiobutton to enabled one if selected is disabled
		for shop_button in self.shop_r_list:
			if (shop_button.isChecked() == True) and (shop_button.isEnabled() == False):
				shop_button.setChecked(False)
				for shop_button2 in self.shop_r_list:
					if shop_button2.isEnabled() == True:
						shop_button2.setChecked(True)
						break
		#Display proper link to the shop
		shop_nr = 0
		for shop_button in self.shop_r_list:
			if shop_button.isChecked() == True:
				if shop_nr == 0:
					self.description_shop_link.setText("")
				elif shop_nr == 1:
					steam_link = game_module.steam_link
					self.description_shop_link.setText("<a href='" + steam_link + "'>Link to the game on Steam.</a>")
			shop_nr += 1
		#Adjust available buttons depending on game status
		if clicked_game_status == 0 or clicked_game_status == -1:
			self.playButton.setEnabled(False)
			self.launcherButton.setEnabled(False)
			self.installButton.setEnabled(True)
			self.installButton.setText("Install")
			self.uninstallButton.setEnabled(False)
		elif clicked_game_status == 1:
			self.playButton.setEnabled(True)
			self.launcherButton.setEnabled(True)
			self.installButton.setEnabled(True)
			self.installButton.setText("Install")
			self.uninstallButton.setEnabled(True)
		elif clicked_game_status == 2:
			self.playButton.setEnabled(True)
			self.launcherButton.setEnabled(True)
			self.installButton.setEnabled(True)
			self.installButton.setText("Update")
			self.uninstallButton.setEnabled(True)
		elif clicked_game_status == 3:
			self.playButton.setEnabled(False)
			self.launcherButton.setEnabled(False)
			self.installButton.setEnabled(False)
			self.installButton.setText("Install")
			self.uninstallButton.setEnabled(False)
		#Workaround bug, when enabled buttons sometimes are not returning to black color
		for push_button in self.push_buttons_list:
			if push_button.isEnabled():
				push_button.setStyleSheet('QPushButton {color: black}')
			else:
				push_button.setStyleSheet('QPushButton {color: gray}')
		print("Game list looks like:")
	
	def r0a_clicked(self, enabled):
		if enabled:
			print("No shop radiobutton clicked")
			self.loginText.setEnabled(False)
			self.passwordText.setEnabled(False)
			self.description_shop_link.setText("")
	
	def r1a_clicked(self, enabled):
		if enabled:
			print("Steam shop radiobutton clicked")
			self.loginText.setEnabled(True)
			self.passwordText.setEnabled(True)
			game_module = importlib.import_module("games." + self.clicked_game + ".game")
			steam_link = game_module.steam_link
			self.description_shop_link.setText("<a href='" + steam_link + "'>Link to the game on Steam.</a>")

	def ask_window_start(self, wr_nr):
		print("Starting ask window with reason: " + str(wr_nr))
		nw = AskWindow(wr_nr, self)
		nw.show()
		while nw.isVisible() == True:
			app.processEvents()
		print("ask window finished with the result: " + str(nw.result))
		return nw.result

class SecondThread(QThread):
	
	result_text = pyqtSignal(str)
	percent_num = pyqtSignal(int)
	steam_warning = pyqtSignal(int)

	def __init__(self, task_nr, widget_list):
		print("Initializing SecondThread for Qt")
		QThread.__init__(self)
		len_widget_list = 6
		if len(widget_list) != len_widget_list:
			print("SecondThread error: widget list for has wrong size. Should be: " + str(len_widget_list) + " ,but is: " + str(len(widget_list)))
			return 0
		self.status_label = widget_list[0]
		self.update_button = widget_list[1]
		self.push_buttons_list = widget_list[2]
		self.play_button = widget_list[2][0]
		self.launcher_button = widget_list[2][1]
		self.install_button = widget_list[2][2]
		self.uninstall_button = widget_list[2][3]
		self.radio_list = widget_list[3]
		self.only_engine_radio = widget_list[4]
		self.installing_game = widget_list[5]
		self.connection = 1
		self.task_nr = task_nr

	def __del__(self):
		self.wait()

	def run(self):
		#Check for net connection
		self.check_net_connection()
		if self.connection == 0:
			print("SecondThread error: no internet connection.")
			return 0
		#Check task
		if self.task_nr == 1:
			print("SecondThread: Update app status")
			self.check_app_update()
		#Check if game installed/updated
		elif self.task_nr == 2:
			print("SecondThread: Update game status")
			self.check_games_update()
		#Update progress bar
		elif self.task_nr == 3:
			print("SecondThread: Update progress bar in a loop")
			self.update_progress_bar()
			self.check_games_update()
			print("SecondThread: Progress bar loop finished")
		else:
			print("SecondThread error: wrong task_nr.")
			return 0
		print("SecondThread: Finished")		
					
	def check_net_connection(self):
		try:
			urllib.request.urlopen("https://gitlab.com", timeout=3)
			self.connection = 1
		except urllib.request.URLError:
			self.connection = 0
			self.status_label.setText("Recultis status is: No internet connection")
			self.install_button.setEnabled(False)
	
	def check_app_update(self):
		status = update_do.recultis_update_check(self_dir, recultis_version)
		if status == 2:
			self.update_button.setEnabled(True)
			self.status_label.setText("Recultis status is: Updata available")
		elif status == 1:
			self.status_label.setText("Recultis status is: Up to date")
			
	def check_games_update(self):
		global game_list
		game_nr = 0
		for radio_button in self.radio_list:
			game_status_description = update_do.game_update_status(game_list[game_nr][0], self_dir, recultis_dir)
			game_list[game_nr] = [game_list[game_nr][0], game_status_description]
			radio_button.setText(update_do.game_update_desc(game_list[game_nr]))
			if radio_button.isChecked() == True:
				if game_list[game_nr][1] == 1:
					self.play_button.setEnabled(True)
					self.launcher_button.setEnabled(True)
					self.install_button.setEnabled(True)
					self.install_button.setText("Install")
					self.uninstall_button.setEnabled(True)
					self.only_engine_radio.setEnabled(False)
				elif game_list[game_nr][1] == 2:
					self.play_button.setEnabled(True)
					self.launcher_button.setEnabled(True)
					self.install_button.setEnabled(True)
					self.install_button.setText("Update")
					self.uninstall_button.setEnabled(True)
					self.only_engine_radio.setEnabled(True)
				elif game_list[game_nr][1] == 0:
					self.play_button.setEnabled(False)
					self.launcher_button.setEnabled(False)
					self.install_button.setEnabled(True)
					self.install_button.setText("Install")
					self.uninstall_button.setEnabled(False)
					self.only_engine_radio.setEnabled(False)
			game_nr += 1
		#Workaround bug, when enabled buttons sometimes are not returning to black color
		for push_button in self.push_buttons_list:
			if push_button.isEnabled():
				push_button.setStyleSheet('QPushButton {color: black}')
			else:
				push_button.setStyleSheet('QPushButton {color: gray}')
		print("Game list looks like:")
		print(game_list)
	
	def update_progress_bar(self):
		global game_list
		game_nr = 0
		for radio_button in self.radio_list:
			if radio_button.isChecked() == True:
				game_list[game_nr] = [game_list[game_nr][0], 3]
				game = game_list[game_nr][0]				
				radio_button.setText(update_do.game_update_desc(game_list[game_nr]))
			else:
				game_nr += 1
		print("Game list looks like:")
		print(game_list)
		for push_button in self.push_buttons_list:
			push_button.setEnabled(False)
			#Workaround bug, when enabled buttons sometimes are not returning to black color
			push_button.setStyleSheet('QPushButton {color: gray}')
		time.sleep(0.5)
		percent = 0
		while percent != 100:
			result, percent = status.check(game)
			self.result_text.emit(result)
			self.percent_num.emit(percent)
			time.sleep(1)
			if "Warning" in result:
				print(result)
				self.steam_warning.emit(1) #This should not allways be 1. 1 Represent Steam Guard.
				while "Warning" in result:
					result, percent = status.check(game)
					time.sleep(1)
			elif "Error" in result:
				print(result)
				#Clear currently installing game value after installation finished
				self.installing_game = ""
				return 0
		#Clear currently installing game value after installation finished
		self.installing_game = ""
		game_list[game_nr] = [game_list[game_nr][0], 1]

class AskWindow(QMainWindow):
	#Available reasons: 1 - Steam Guard, 2 - Choose game launcher, 3 - Choose app update version
	
	reason = 0
	game = ""
	result = "no"
	
	def __init__(self, reason, parent=None):
		print("Initializing AskWindow")
		super(AskWindow, self).__init__(parent)
		self.reason = reason
		move_offset = 50
		if self.reason == 1:
			print("Reason: " + str(self.reason) + " - Steam Guard authentication")
			self.game = parent.installing_game
			self.title = 'Steam Guard authentication.'
			self.MessageLabel = QLabel("Please provide Steam Guard code, which was just send via email.", self)
			self.textbox = QLineEdit(self)
			self.button = QPushButton('OK', self)
			self.button.clicked.connect(self.on_click_steam_guard)
			self.textbox.move(0,move_offset)
			self.textbox.resize(400, 30)
		elif self.reason == 2:
			print("Reason: " + str(self.reason) + " - Choosing game launcher")
			self.game = parent.playing_game
			self.title = 'Choose game launcher.'
			self.MessageLabel = QLabel("Please choose game launcher.", self)
			game_module = importlib.import_module("games." + self.game + ".game")
			launcher_cmd_list = game_module.launcher_cmd_list
			self.r_button_list = []
			for launcher in launcher_cmd_list:
				self.r_button_list.append(QRadioButton(launcher[0], self))
			self.button = QPushButton('OK', self)
			self.button.clicked.connect(self.on_click_launcher)
			for r_button in self.r_button_list:
				r_button.move(0, move_offset)
				move_offset = move_offset + 27
				r_button.resize(400, 30)
			self.r_button_list[0].setChecked(True)
		elif self.reason == 3:
			print("Reason: " + str(self.reason) + " - Choosing update version")
			self.title = 'Choose update version.'
			self.MessageLabel = QLabel("Choose version of Recultis to which you want to update.\nPlease note that major version updates may break\ncompatibility for older systems.", self)
			patch_link_file = open(self_dir + "patch_link.txt", "r")
			self.patch_link_list = []
			for line in patch_link_file:
				if not line.strip():
					pass
				else:
					self.patch_link_list.append(line.strip())
			self.r_button_list = []
			for link in self.patch_link_list:
				self.r_button_list.append(QRadioButton("Recultis version " + link[-12:-7], self))
			self.button = QPushButton('OK', self)
			self.button.clicked.connect(self.on_click_autoupdate)
			for r_button in self.r_button_list:
				r_button.move(0, move_offset)
				move_offset = move_offset + 27
				r_button.resize(400, 30)
			self.r_button_list[0].setChecked(True)
		else:
			print("Error, wrong reason nr: " + str(self.reason))
			return 0
		self.setWindowTitle(self.title)
		self.MessageLabel.move(0,0)
		self.MessageLabel.resize(self.MessageLabel.minimumSizeHint())
		self.button.move(50, move_offset + 40)
		self.cancel_button = QPushButton('Cancel', self)
		self.cancel_button.clicked.connect(self.close)
		self.cancel_button.move(200, move_offset + 40)
		self.setGeometry(250, 250, 400, move_offset + 90)
		
	def on_click_steam_guard(self):
		print("Steam Guard Key provided")
		steam_guard_key = self.textbox.text()
		steam_guard_key_file = open(recultis_dir + "steam_guard_key.txt", "w")
		steam_guard_key_file.write(steam_guard_key)
		steam_guard_key_file.close()
		self.result = "ok"
		self.close()
	
	def on_click_launcher(self):
		result = 0
		for r_button in self.r_button_list:
			if r_button.isChecked() == False:
				result += 1
			else:
				break
		print("Launcher choosen")
		self.result = result
		self.close()
		
	def on_click_autoupdate(self):
		result = 0
		for r_button in self.r_button_list:
			if r_button.isChecked() == False:
				result += 1
			else:
				update_link = self.patch_link_list[result]
		print("Recultis update version choosen")
		update_do.recultis_update_do(self_dir, update_link)
		self.result = "ok"
		self.close()

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())

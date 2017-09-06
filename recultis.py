#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import sys, os, _thread, time, urllib
from subprocess import check_output, call

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from tools import update_check, status

recultis_version = "1.2.0pre"

self_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
recultis_dir = os.getenv("HOME") + "/.recultis/"

from games import installer
#This is the list of lists. It is sorted in alphabetic order. Every position is list wich contains game name (as game directory name) and game status.
game_list = installer.get_game_list()

class Window(QWidget):
	
	radio_list = []
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
		self.game_r_list = []
		for game_position in game_list:
			self.game_r_list.append(QRadioButton(get_game_desc(game_position)))
			self.game_r_list[0].toggled.connect(self.game_radiobutton_effect)
		choose_data_box = QGroupBox("Choose digital distribution platform to download game data:")
		self.r0a = QRadioButton("Only engine update")
		self.r0a.setEnabled(False)
		self.r0a.toggled.connect(self.r0a_clicked)
		self.r1a = QRadioButton("Steam")
		self.r1a.setChecked(True)
		self.r1a.toggled.connect(self.r1a_clicked)
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
		self.installButton = QPushButton("Install")
		self.uninstallButton = QPushButton("Uninstall")
		self.exitButton = QPushButton("Exit")
		choose_game_Label = QLabel("Choose the game to install:")
		
		#Default game selection
		self.description_image = QLabel() 
		self.description_label = QLabel()
		self.description_steam_link = QLabel()
		self.description_steam_link.setOpenExternalLinks(True)
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
		hbox2.addWidget(self.installButton)
		hbox2.addWidget(self.uninstallButton)
		hbox2.addWidget(self.exitButton)
		vbox1.addLayout(hbox2)
		vbox2.addWidget(self.description_image)
		vbox2.addWidget(self.description_label)
		vbox2.addWidget(self.description_steam_link)
		hbox0.addLayout(vbox1)
		hbox0.addLayout(vbox2)
		
		self.app_updateButton.clicked.connect(self.autoupdate)
		self.app_create_launcher.clicked.connect(self.add_launcher)
		self.playButton.clicked.connect(self.play_game)
		self.installButton.clicked.connect(self.install_game)
		self.uninstallButton.clicked.connect(self.uninstall_game)
		self.exitButton.clicked.connect(self.close)
 
		self.setLayout(hbox0)
		self.setWindowTitle("Recultis " + recultis_version)
		
		#After Windows is drawn, lets check status of the games
		self.second_thread_list = [self.app_staus_label, self.app_updateButton, self.playButton, self.installButton, self.uninstallButton, self.game_r_list, self.r0a, self.installing_game]
		self.update_game_app = SecondThread(1, self.second_thread_list)
		self.update_game_app.start()
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
		sys.path.insert(0, self_dir + "games/" + self.playing_game)
		from game import launcher_cmd_list
		sys.path.remove(self_dir + "games/" + self.clicked_game)
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
	
	def install_game(self):
		print("Game to be installed:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				self.installing_game = game_list[r_list_nr][0]
				print(self.installing_game)
				rbutton = game_fname
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
		self.app_staus_label.setText("Recultis status is: Updating. Please wait.")
		patch_link_file = open(self_dir + "patch_link.txt", "r")
		patch_link = patch_link_file.read()
		from tools import update_tool
		update_tool.autoupdate(self_dir, patch_link)
		QMessageBox.information(self, "Message", "Update complete. Recultis will now turn off. Please start it again to apply patch.")
		self.close()
	
	def add_launcher(self):
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
	
	def game_radiobutton_effect(self):
		print("Game selected:")
		r_list_nr = 0
		for game_fname in self.game_r_list:
			if game_fname.isChecked() == True:
				self.clicked_game = game_list[r_list_nr][0]
				print(self.clicked_game)
				rbutton = game_fname
			r_list_nr += 1
		sys.path.insert(0, self_dir + "games/" + self.clicked_game)
		from game import description, screenshot_path, steam_link
		sys.path.remove(self_dir + "games/" + self.clicked_game)
		description_pixmap = QPixmap(screenshot_path)
		self.description_image.setPixmap(description_pixmap)
		self.description_label.setText(description)
		self.description_steam_link.setText("<a href='" + steam_link + "'>Link to the game on Steam.</a>")
		if "Update available" in rbutton.text():
			self.r0a.setEnabled(True)
			self.playButton.setEnabled(True)
			self.installButton.setEnabled(True)
			self.installButton.setText("Update")
			self.uninstallButton.setEnabled(True)
		elif self.r0a.isChecked() == True:
			self.r1a.setChecked(True)
			self.r0a.setEnabled(False)
		else:
			self.r0a.setEnabled(False)
		if "Not installed" in rbutton.text() or "Checking for update" in rbutton.text():
			self.playButton.setEnabled(False)
			self.installButton.setEnabled(True)
			self.installButton.setText("Install")
			self.uninstallButton.setEnabled(False)
		if "Installed" in rbutton.text():
			self.playButton.setEnabled(True)
			self.installButton.setEnabled(True)
			self.installButton.setText("Install")
			self.uninstallButton.setEnabled(True)
		for game_button in self.radio_list:
			if "Installing..." in game_button.text():
				self.playButton.setEnabled(False)
				self.uninstallButton.setEnabled(False)
				self.installButton.setEnabled(False)
	
	def r0a_clicked(self, enabled):
		if enabled:
			self.loginText.setEnabled(False)
			self.passwordText.setEnabled(False)
	
	def r1a_clicked(self, enabled):
		if enabled:
			self.loginText.setEnabled(True)
			self.passwordText.setEnabled(True)

	def ask_window_start(self, wr_nr):
		nw = AskWindow(wr_nr, self)
		nw.show()
		while nw.isVisible() == True:
			app.processEvents()
		return nw.result

class SecondThread(QThread):
	
	result_text = pyqtSignal(str)
	percent_num = pyqtSignal(int)
	steam_warning = pyqtSignal(int)

	def __init__(self, task_nr, widget_list):
		QThread.__init__(self)
		len_widget_list = 8
		if len(widget_list) != len_widget_list:
			print("SecondThread error: widget list for has wrong size. Should be: " + str(len_widget_list) + " ,but is: " + str(len(widget_list)))
			return 0
		self.status_label = widget_list[0]
		self.update_button = widget_list[1]
		self.play_button = widget_list[2]
		self.install_button = widget_list[3]
		self.uninstall_button = widget_list[4]
		self.radio_list = widget_list[5]
		self.only_engine_radio = widget_list[6]
		self.installing_game = widget_list[7]
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
					
	def check_net_connection(self):
		try:
			urllib.request.urlopen("https://github.com", timeout=3)
			self.connection = 1
		except urllib.request.URLError:
			self.connection = 0
			self.status_label.setText("Recultis status is: No internet connection")
			self.install_button.setEnabled(False)
	
	def check_app_update(self):
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
			
	def check_games_update(self):
		global game_list
		game_nr = 0
		for radio_button in self.radio_list:
			game_status_description = update_check.start(game_list[game_nr][0], self_dir)
			game_list[game_nr] = [game_list[game_nr][0], game_status_description]
			print("Game list looks like:")
			print(game_list)
			radio_button.setText(get_game_desc(game_list[game_nr]))
			game_nr += 1
			if radio_button.isChecked() == True:
				if "Installed" in radio_button.text():
					self.play_button.setEnabled(True)
					self.install_button.setEnabled(True)
					self.install_button.setText("Install")
					self.uninstall_button.setEnabled(True)
					self.only_engine_radio.setEnabled(False)
				elif "Update available" in radio_button.text():
					self.play_button.setEnabled(True)
					self.install_button.setEnabled(True)
					self.install_button.setText("Update")
					self.uninstall_button.setEnabled(True)
					self.only_engine_radio.setEnabled(True)
				elif "Not installed" in radio_button.text():
					self.play_button.setEnabled(False)
					self.install_button.setEnabled(True)
					self.install_button.setText("Install")
					self.uninstall_button.setEnabled(False)
					self.only_engine_radio.setEnabled(False)
	
	def update_progress_bar(self):
		global game_list
		game_nr = 0
		for radio_button in self.radio_list:
			if radio_button.isChecked() == True:
				game_list[game_nr] = [game_list[game_nr][0], 3]
				game = game_list[game_nr][0]				
				radio_button.setText(get_game_desc(game_list[game_nr]))
			game_nr += 1
		print("Game list looks like:")
		print(game_list)
		self.play_button.setEnabled(False)
		self.install_button.setEnabled(False)
		self.uninstall_button.setEnabled(False)
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

class AskWindow(QMainWindow):
	#Available reasons: 1 - Steam Guard, 2 - Choose game launcher
	
	reason = 0
	game = ""
	result = "no"
	
	def __init__(self, reason, parent=None):
		super(AskWindow, self).__init__(parent)
		self.reason = reason
		move_offset = 27
		if self.reason == 1:
			self.game = parent.installing_game
			self.title = 'Steam Guard authentication.'
			self.MessageLabel = QLabel("Please provide Steam Guard code, which was just send via email.", self)
			self.textbox = QLineEdit(self)
			self.button = QPushButton('OK', self)
			self.button.clicked.connect(self.on_click_steam_guard)
			self.textbox.move(0,move_offset)
			self.textbox.resize(400, 30)
		elif self.reason == 2:
			self.game = parent.playing_game
			self.title = 'Choose game launcher.'
			self.MessageLabel = QLabel("Please choose game launcher.", self)
			sys.path.insert(0, self_dir + "games/" + self.game)
			from game import launcher_cmd_list
			sys.path.remove(self_dir + "games/" + self.game)
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
		else:
			print("Error, wrong reason nr: " + str(self.reason))
			return 0
		print("Warning reason nr: " + str(self.reason))
		self.setWindowTitle(self.title)
		self.MessageLabel.move(0,0)
		self.MessageLabel.resize(self.MessageLabel.minimumSizeHint())
		self.button.move(150,move_offset + 40)
		self.setGeometry(250, 250, 400, move_offset + 90)
		
	def on_click_steam_guard(self):
		print("Steam Guard Ley provided")
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

#Status: -1 - Checking for update...; 0 - Not installed; 1 - Installed; 2 - Update available; 3 - Installing...	
def get_game_desc(info_list):
	game_fname = info_list[0]
	status = info_list[1]
	sys.path.insert(0, self_dir + "games/" + game_fname)
	from game import full_name
	sys.path.remove(self_dir + "games/" + game_fname)
	rest_name = ""
	if status == -1:
		rest_name = " (Checking for update...)"
	elif status == 0:
		rest_name = " (Not installed)"
	elif status == 1:
		rest_name = " (Installed)"
	elif status == 2:
		rest_name = " (Update available)"
	elif status == 3:
		rest_name = " (Installing...)"
	return full_name + rest_name

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())

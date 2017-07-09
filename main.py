#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

##This file will move icon to proper directory, check dependencies and handle autoupdate.

#Copy icon
import os, shutil
if os.path.isdir(os.getenv("HOME") + "/.icons") == False:
	os.makedirs(os.getenv("HOME") + "/.icons")
if os.path.isfile(os.getenv("HOME") + "/.icons/recultis.png") == False:
	print("Prepare Recultis launcher icon.")
	shutil.copy(os.path.dirname(os.path.abspath(__file__)) + "/assets/icon.png", os.getenv("HOME") + "/.icons/recultis.png")
del os, shutil

#Check for dependencies
print("Checking dependencies")
try:
	import PyQt5
	del PyQt5
	dep_pyqt = True
	print("PyQt5 found")
except:
	dep_pyqt = False
	print("PyQt5 not found")
from tools import unpack_deb
dep_dpkg = unpack_deb.check_dpkg()
dep_ar = unpack_deb.check_ar()
del unpack_deb
dep_error = ""
if dep_pyqt == False:
	dep_error = dep_error + "Error: Python3 PyQt5 is missing. Please install it from the repository and start the program again. "
if dep_dpkg == False and dep_ar == False:
	dep_error = dep_error + "Error: both 'ar' and 'dpkg' are missing in the system. Please install one of them and start the program again. "
if dep_error != "":
	print(dep_error)
	import os
	error_file = open("error_file.txt", "w")
	error_file.write(dep_error + "\n")
	del error_file
	os.system("xterm -e 'bash -c \"cat error_file.txt ; sleep 20\"'")
	os.remove("error_file.txt")
	import sys
	sys.exit(2)

#Start main program
print("Every dependencie met. Starting Recultis.")
import recultis.py

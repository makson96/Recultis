#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

##This file will move icon to proper directory, check dependencies and handle autoupdate.

#Copy icon
import os, shutil, sys
if os.path.isdir(os.getenv("HOME") + "/.local/share/icons") == False:
	os.makedirs(os.getenv("HOME") + "/.local/share/icons")
if os.path.isfile(os.getenv("HOME") + "/.local/share/icons/recultis.png") == False:
	print("Prepare Recultis launcher icon.")
	shutil.copy(os.path.dirname(os.path.abspath(__file__)) + "/assets/icon.png", os.getenv("HOME") + "/.local/share/icons/recultis.png")

#Check for dependencies
#Python3 PyQt5
print("Checking dependencies")
try:
	import PyQt5
	del PyQt5
	dep_pyqt = True
	print("PyQt5 found")
except:
	dep_pyqt = False
	print("PyQt5 not found")
#DPKG or AR
from tools import unpack_deb
dep_dpkg = unpack_deb.check_dpkg()
if dep_dpkg == True:
	print("dpkg found")
else:
	print("dpkg not found")
dep_ar = unpack_deb.check_ar()
if dep_ar == True:
	print("ar found")
else:
	print("ar not found")
del unpack_deb
#32 bit libc and stdlic++
os.system("ldconfig -p | grep libc.so > error_file.txt")
if sum(1 for line in open('error_file.txt')) >= 2:
	print("32 bit libc found")
	dep_32bit_libc = True
else:
	print("32 bit libc not found")
	dep_32bit_libc = False
os.system("ldconfig -p | grep libstdc++.so > error_file.txt")
if sum(1 for line in open('error_file.txt')) >= 2:
	print("32 bit libstdc++ found")
	dep_32bit_libstd = True
else:
	print("32 bit libstdc++ not found")
	dep_32bit_libstd = False
os.system("ldconfig -p | grep libgcc_s.so > error_file.txt")
if sum(1 for line in open('error_file.txt')) >= 2:
	print("32 bit libgcc_s found")
	dep_32bit_libgcc = True
else:
	print("32 bit libgcc_s not found")
	dep_32bit_libgcc = False

dep_error = ""
if dep_pyqt == False:
	dep_error = dep_error + "Error: Python3 PyQt5 is missing. Please install it from the repository and start the program again.\n"
if dep_dpkg == False and dep_ar == False:
	dep_error = dep_error + "Error: both 'ar' and 'dpkg' are missing in the system. Please install one of them and start the program again.\n"
if dep_32bit_libc == False or dep_32bit_libstd == False or dep_32bit_libgcc == False::
	dep_error = dep_error + "Error: 32 bit libc required for steam is missing. Try to install lib32gcc1 on Ubuntu/Debian or glibc.i686 and libstdc++.i686 on Fedora.\n"
if dep_error != "":
	print(dep_error)
	error_file = open("error_file.txt", "w")
	error_file.write(dep_error + "\n")
	del error_file
	os.system("xterm -e 'bash -c \"cat error_file.txt ; sleep 20\"'")
	sys.exit(2)

if os.path.isfile("error_file.txt"):
	os.remove("error_file.txt")
#Start main program
print("Every dependencie met. Starting Recultis.")
import recultis.py

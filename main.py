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
if os.path.isfile(os.getenv("HOME") + "/.icons/free-engineer.png") == False:
	shutil.copy(os.path.dirname(os.path.abspath(__file__)) + "/data/icon.png", os.getenv("HOME") + "/.icons/free-engineer.png")

#Check for dependencies
print("TODO: Check dependencies")

#Check for update
print("TODO: Check for update")

#Start main program
import free_engineer.py

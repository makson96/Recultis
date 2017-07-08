#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, shutil, subprocess

def check_dpkg():
	try:
		subprocess.check_call(['dpkg'], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	except subprocess.CalledProcessError:
		dpkg_present = True
		print("dpkg is present")
	except OSError:
		dpkg_present = False
		print("dpkg is not present")
	return dpkg_present

def check_ar():
	try:
		subprocess.check_call(['ar'], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	except subprocess.CalledProcessError:
		ar_present = True
		print("ar is present")
	except OSError:
		ar_present = False
		print("ar is not present")
	return ar_present

def ar(deb_file, tmp_dir):
	print("ar command: " + "cd " + tmp_dir + "; ar x " + deb_file)
	s_ar = subprocess.call("cd " + tmp_dir + "; ar x " + deb_file, shell=True)

def dpkg(deb_file, tmp_dir):
	print("dpkg command: " + "dpkg -x " + deb_file + " " + tmp_dir)
	s_dpkg = subprocess.call("dpkg -x " + deb_file + " " + tmp_dir, shell=True)

def untar_data(tmp_dir):
	print("extract file: " + tmp_dir + "data.tar.xz")
	tar = tarfile.open(tmp_dir + "data.tar.xz")
	tar.extractall(path=tmp_dir)
	tar.close()

def move_data(tmp_dir):
	for directory in next(os.walk(tmp_dir + "opt/"))[1]:
		print("move from: " + tmp_dir + "opt/" + directory + "to: " + tmp_dir + directory
		shutil.move(tmp_dir + "opt/" + directory, tmp_dir + directory)

def clean_data(tmp_dir, deb_name):
	try:
		shutil.rmtree(tmp_dir + "opt")
		print("remove: " + tmp_dir + "opt")
	except:
		pass
	clean_files = ["control.tar.gz", "data.tar.xz", "debian-binary", deb_name]
	for clean_file in clean_files:
		try:
			os.remove(tmp_dir + clean_file)
			print("remove: " + tmp_dir + clean_file)
		except:
			pass

def unpack_deb(tmp_dir, deb_name):
	dpkg_present = check_dpkg()
	if dpkg_present == True:
		dpkg(tmp_dir+deb_name, tmp_dir)
	else:
		ar(tmp_dir+deb_name, tmp_dir)
		untar_data(tmp_dir)
	move_data(tmp_dir)
	clean_data(tmp_dir, deb_name)

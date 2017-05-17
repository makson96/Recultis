#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, shutil, pickle
from subprocess import call, check_call
from free_engineer import engineer_dir

def check_dpkg():
	try:
		subprocess.check_call(['dpkg'], stdout=open(os.devnull, 'wb'))
	except subprocess.CalledProcessError:
		dpkg_present = True
	except OSError:
		dpkg_present = False
	return dpkg_present

def ar(deb_file, tmp_dir):
	s_ar = call("cd " + tmp_dir + "; ar x " + deb_file, shell=True)

def dpkg(deb_file, tmp_dir):
	s_dpkg = call("dpkg -x " + deb_file + " " + tmp_dir, shell=True)

def untar_data(tmp_dir):
	os.chdir(tmp_dir)
	tar = tarfile.open(tmp_dir + "data.tar.xz")
	tar.extractall()
	tar.close()

def move_data(tmp_dir, deb_name):
	shutil.move(tmp_dir + "opt/" + deb_name[:-4], tmp_dir + deb_name[:-4])

def clean_data(tmp_dir, deb_name):
	shutil.rmtree(tmp_dir + "opt")
	os.remove(tmp_dir + "control.tar.gz")
	os.remove(tmp_dir + "data.tar.xz")
	os.remove(tmp_dir + "debian-binary")
	os.remove(tmp_dir+deb_name)

def unpack_deb(tmp_dir, deb_name):
	status = "Installing engine"
	percent = 25
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
	dpkg_present = check_dpkg()
	if dpkg_present == True:
		dpkg(tmp_dir+deb_name, tmp_dir)
	else:
		ar(tmp_dir+deb_name, tmp_dir)
		untar_data(tmp_dir)
	move_data(tmp_dir, deb_name)
	clean_data(tmp_dir, deb_name)

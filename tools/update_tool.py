#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, urllib.request, tarfile, shutil

def autoupdate(self_dir, patch_link):
	print("Starting autoupdate.")
	#download patch
	patch_file = "patch.tar.gz"
	urllib.request.urlretrieve(patch_link, self_dir + patch_file)
	#remove old files
	for the_file in os.listdir(self_dir):
		file_path = os.path.join(self_dir, the_file)
		if os.path.isfile(file_path) and the_file != patch_file:
			os.remove(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)
	#unpack patch
	tar = tarfile.open(self_dir + patch_file)
	tar.extractall()
	tar.close()
	#remove patch file
	os.remove(self_dir + patch_file)
	#copy everything one directory backs
	patch_dir = os.listdir(self_dir)[0]
	for the_file_or_dir in os.listdir(patch_dir):
		shutil.move(os.path.join(patch_dir, the_file_or_dir), os.path.join(self_dir, the_file_or_dir))
	shutil.rmtree(patch_dir)
	print("Autoupdate complete.")

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import pickle

from tools import download_engine

def read_status(engineer_dir):
	status_list = pickle.load(open(engineer_dir+"status_list.p", "rb"))
	return status_list

def write_status(engineer_dir, file_path, link_path):
	#Downloading engine is 20%
	status = "Downloading engine"
	disk_s = download_engine.check_disk_size(file_path)
	url_s = download_engine.check_url_size(link_path)
	percent = 20 * disk_s / url_s
	print(disk_s)
	print(url_s)
	print(percent)
	if disk_s != url_s:
		pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
		return
	#Installing engine is 5%
	status = "Installing engine"
	percent = 25
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
	return

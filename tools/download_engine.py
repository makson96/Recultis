#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import urllib.request, os, time

def download(link, file_path):
	urllib.request.urlretrieve(link, file_path)
	return 1

def status(link, file_path):
	status = "Downloading engine"
	disk_s = 0
	url_s = 1
	if disk_s != url_s:
		try:
			f = open(file_path, "rb")
			disk_s = int(len(f.read()))
			f.close()
		except:
			time.sleep(4)
			if os.path.isfile(file_path) == False:
				percent = 21
				statatus = "Engine downloaded"
				return status, percent
		d = urllib.request.urlopen(link)
		url_s = int(d.getheaders()[2][1])
		percent = 20 * disk_s / url_s
	else:
		percent = 21
		statatus = "Engine downloaded"
	return status, percent

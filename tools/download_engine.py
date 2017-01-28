#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import urllib.request

def check_url_size(link):
	d = urllib.request.urlopen(link)
	meta = d.info()
	u_size = meta.getheaders("Content-Length")[0]
	return 1, int(u_size)

def check_disk_size(file_path):
	f = open(file_path, "rb")
	f_size = len(f.read())
	f.close()
	return 1, int(f_size)

def download(link, file_path):
	urllib.request.urlretrieve(link, file_path)
	return 1

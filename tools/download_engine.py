#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import urllib.request, pickle, _thread

def download(link, file_path):
	_thread.start_new_thread(urllib.request.urlretrieve, (link, file_path))
	status = "Downloading engine"
	f = open(file_path, "rb")
	disk_s = int(len(f.read()))
	f.close()
	d = urllib.request.urlopen(link)
	url_s = int(d.getheaders()[2][1])
	percent = 20 * disk_s / url_s
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
	return 1

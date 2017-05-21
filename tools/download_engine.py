#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import urllib.request, pickle, _thread, time

def download(link, file_path):
	_thread.start_new_thread(urllib.request.urlretrieve, (link, file_path))
	status = "Downloading engine"
	disk_s = 0
	url_s = 1
	while disk_s != url_s:
		time.sleep(2)
		try:
			f = open(file_path, "rb")
			disk_s = int(len(f.read()))
			f.close()
		except:
			pass
		d = urllib.request.urlopen(link)
		url_s = int(d.getheaders()[2][1])
		percent = 20 * disk_s / url_s
		pickle.dump([status, percent], open(os.getenv("HOME") + "/.free-engineer/status_list.p", "wb"))
	return 1

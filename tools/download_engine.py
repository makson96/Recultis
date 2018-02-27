#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import urllib.request

def download(link, file_path):
	link = link.rstrip()
	print("Downloading game engine from: " + link + " to: " + file_path)
	try:
		urllib.request.urlretrieve(link, file_path)
	except urllib.error.HTTPError:
		return 0
	print("Game engine download finished successfully")
	return 1

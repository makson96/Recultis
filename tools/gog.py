#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, time, shutil
from subprocess import Popen, PIPE

def start(login, password, recultis_dir, s_appid, game_dir):
	shop_install_dir = recultis_dir + "shops/gog/"
	print("Download lgogdownloader")
	from tools import update_do, download_engine, unpack_deb
	lgog_link = update_do.get_link_string("lgogdownloader", "recultis2")
	result = download_engine.download(lgog_link, recultis_dir + "tmp/lgogdownloader.deb")		
	unpack_deb.unpack_deb(recultis_dir + "tmp/", "lgogdownloader.deb")
	if os.path.isdir(shop_install_dir) == False:
		os.makedirs(shop_install_dir)
	else:
		shutil.rmtree(shop_install_dir)
		os.makedirs(shop_install_dir)
	shutil.move(recultis_dir + "tmp/lgogdownloader/bin/lgogdownloader", shop_install_dir)
	print("Download innoextract")
	print("Download game using lgogdownloader")
	print("Extract game using innoextract")
	return True

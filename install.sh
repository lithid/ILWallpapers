#!/bin/bash
# Install this app

chk=$(which dpkg-buildpackage |wc -l)
type=$(dpkg-architecture |grep "DEB_BUILD_ARCH=" |cut -d"=" -f2)

if  [ $chk -eq 0 ]; then
	sudo apt-get install debhelper
fi

dpkg-buildpackage -rfakeroot
sudo dpkg -i ../ilwallpapers_0.1_$type.deb

./clean

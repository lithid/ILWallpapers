InterfaceLiftGUI
================

InterfaceLift front end for setting wallpapers in gnome desktops

How to build:

Install dependacy:

    sudo apt-get install debhelper
    
Build:

    dpkg-buildpackage -rfakeroot
    
Install:

    sudo dpkg -i ../ilwallpapers-daily_0.1_$(dpkg-architecture |grep "DEB_BUILD_ARCH=" |cut -d"=" -f2).deb
    
    
You can also install using my PPA:
================
located: https://launchpad.net/~lithid/+archive/ppa

    sudo apt-add-repository ppa:lithid/ppa
    sudo apt-get update
    
Install:

    sudo apt-get install ilwallpapers-daily
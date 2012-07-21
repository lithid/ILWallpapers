#!/usr/bin/env python

#   ILWallpapers is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

import gtk, pygtk
import commands
import os
import shutil
import urllib
import urllib2
import re
import time
import threading

gtk.threads_init()

myHome = os.environ['HOME']
WallStore = "%s/Pictures/InterfaceLift" % myHome
Url = "http://interfacelift.com/wallpaper/downloads/date"
UserAgent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)"
DownloadUrl = "http://interfacelift.com"
PreviewUrl = "%s/wallpaper/previews" % DownloadUrl
Icon = "/usr/share/ilwallpapers/images/Icon.png"
SplashImg = "/usr/share/ilwallpapers/images/Interfacelift.jpg"

placeIcon = gtk.gdk.pixbuf_new_from_file(Icon)

myMainWallList = []
myMainWallList2 = []
WallSet = None
FinName = None
Spanned = None
Clean = None

SplashW = gtk.Window(gtk.WINDOW_TOPLEVEL)
label = gtk.Label()

try:
	os.makedirs(WallStore)
except:
	pass

class SplashScreenThread(threading.Thread):
	stopthread = threading.Event()

	def run(self):

		while not self.stopthread.isSet():
			gtk.threads_enter()

			SplashScreen().main()

			gtk.threads_leave()
			self.stop()

	def stop(self):
		global SplashW
		SplashW.hide()
		global SST
		SST._Thread__stop()
		self.stopthread.set()

class MainThread(threading.Thread):
	stopthread = threading.Event()

	def run(self):

		while not self.stopthread.isSet() :
			gtk.threads_enter()

			InterfaceWallpapers().main()

			gtk.threads_leave()
			self.stop()

	def stop(self):
		self.stopthread.set()

class SplashScreen():

	def main(self):

		global SplashW

		SplashW.set_position(gtk.WIN_POS_CENTER)
		SplashW.set_size_request(280, 280)
		SplashW.set_icon(placeIcon)
		SplashW.set_resizable(False)
		SplashW.set_decorated(False)
		vbox = gtk.VBox(False, 0)
		event = gtk.EventBox()
		image = gtk.Image()
		event.add(image)
		image.set_from_file(SplashImg)
		image.show()
		event.show()
		vbox.add(event)
		SplashW.add(vbox)
		SplashW.show_all()

		gtk.main()

class InterfaceWallpapers():

	def GetImages(self, version, dem, mon):
		print mon
		FinUrl = "%s/%s/%s/" % (Url, version, dem,)
		try:
			htmlpage = urllib2.urlopen(FinUrl).read()
		except:
			print "Error reaching the interfacelift.com website. Exiting."
			exit()
		alllinks = re.findall("<a href=\".*?_%s.jpg\">.*?</a>" % dem,htmlpage)

		for links in alllinks:
			x = links.split("\"")
			x = x[1]
			if mon == "one":
				myMainWallList.append(x)
			elif mon == "two":
				myMainWallList2.append(x)
			else:
				print "Don't know what you are doing, please just stop it"

		return

	def GetVersion(self, version):
		final = None
		print version

		if version == "3840x1080":
			version = "3360x1050"
			
		if version == "2560x720":
			version == "2880x900"
			
		print version

		netbook = ["1366x768", "1280x800", "1024x600", "800x400"]
		fullscreen = ["1600x1200", "1400x1050", "1280x1024", "1280x960", "1024x768"]
		widescreen = ["2880x1800", "2560x1600", "2560x1440", "1920x1200", "1680x1050", "1440x900", "1280x800"]
		HDTV = ["1920x1080", "1280x720"]
		screens2 = ["2560x1024", "2880x900", "3200x1200", "3360x1050", "2840x1200", "5120x1600"]
		
		if final == None:
			for x in netbook:
				if version == x:
					final = "netbook"
		if final == None:
			for x in fullscreen:
				if version == x:
					final = "fullscreen"
		if final == None:
			for x in widescreen:
				if version == x:
					final = "widescreen"
		if final == None:
			for x in HDTV:
				if version == x:
					final = "HDTV"
		if final == None:
			for x in screens2:
				if version == x:
					final = "2_screens"

		print final
		return final

	def GetMonitors(self):
		chk = commands.getoutput("xrandr --current |grep \" connected [0-9][0-9]\" |wc -l")
		return chk

	def GetWidth(self):
		window = gtk.Window()
		screen = window.get_screen()
		width = screen.get_width()
		return width

	def GetHeight(self):
		window = gtk.Window()
		screen = window.get_screen()
		height = str(screen.get_height())
		return height

	def WallpaperSet(self, widget):
		global label

		if Clean == True:
			try:
				shutil.rmtree(WallStore)
				os.makedirs(WallStore)
			except:
				os.makedirs(WallStore)

		location = "%s/%s" % (WallStore, FinName)
		urllib.urlretrieve(WallSet, location)
		cmd = "gsettings set org.gnome.desktop.background picture-uri file://%s" % location
		commands.getoutput(cmd)
		if Spanned == True:
			cmd = "gsettings set org.gnome.desktop.background picture-options spanned"
			commands.getoutput(cmd)
		else:
			cmd = "gsettings set org.gnome.desktop.background picture-options stretched"
			commands.getoutput(cmd)
		label.set_markup("%s is set!" % FinName)

	def CheckSpanned(self, widget):
		global Spanned
		if widget.get_active() == True:
			Spanned = True
			print "Spanned is now True"
		else:
			Spanned = False
			print "Spanned is now False"

	def CheckClean(self, widget):
		global Clean
		if widget.get_active() == True:
			Clean = True
			print "Clean will take place next download"
		else:
			Clean = False
			print "Clean is disabled"

	def WallpaperCallback(self, widget, event, data, prename, n):
		global WallSet
		global label
		global FinName
		label.set_markup("You choose image <b>%s</b>" % prename)
		WallSet = data
		f = n.split("/")
		FinName = f[-1]

	def main_quit():
		global SS
		SS.stop()
		gtk.main_quit()

	def main(self):
	
		s = None
		sv = None

		dialog = gtk.Dialog("Download InterfaceLift Wallpapers", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_resizable(False)
		dialog.set_icon(placeIcon)

		monitors = self.GetMonitors()
		w = self.GetWidth()
		h = self.GetHeight()
		if monitors == "2":
		        single = str(w / 2)
		        
		w = str(w)

		wh = "%sx%s" % (w, h)
		
		if monitors == "2":
			swh = "%sx%s" % (single, h)

		v = self.GetVersion(wh)
		
		if monitors == "2":
			sv = self.GetVersion(swh)

		self.GetImages(v, wh, "one")
		
		if monitors == "2":
			self.GetImages(sv, swh, "two")

		label.set_markup("Choose your wallpaper from below...")
		label.show()
		dialog.vbox.pack_start(label, True, True, 15)

		if v is not None:
			mainLabel = gtk.Label()
			if monitors == "2":
				head = "Dual Screen"
			else:
				head = "Single Screen"
			mainLabel.set_markup("%s: <b>%s x %s</b>" % (head, w, h))
			mainLabel.show()
			dialog.vbox.pack_start(mainLabel, True, True, 0)
			mainScroll = gtk.ScrolledWindow()
			mainScroll.set_size_request(600, 180)
			mainScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
			mainScroll.show()
			dialog.vbox.pack_start(mainScroll, True, True, 0)

			mainTable = gtk.Table(10, 1, False)

			mainScroll.add_with_viewport(mainTable)
			mainTable.show()

			count = 0
			for x in myMainWallList:
				count+=1

				event = "event%s" % (count)
				image = "image%s" % (count)

				event = gtk.EventBox()
				image = gtk.Image()
				preview = x.replace("_%s" % wh, "")
				preview = preview.split("/")
				preview = preview[-1]
				PreWall = "%s/%s" % (PreviewUrl, preview)
				FinWall = "%s%s" % (DownloadUrl, x)
				imgurl = urllib2.urlopen(PreWall)
				loader = gtk.gdk.PixbufLoader()
				loader.write(imgurl.read())
				loader.close() 
				image.set_from_pixbuf(loader.get_pixbuf())
				event.connect("button_press_event", self.WallpaperCallback, FinWall, preview, x)
				event.add(image)
				mainTable.attach(event, count-1, count, 0, 1, xpadding=5, ypadding=5)
				image.show()
				event.show()
			
			
		if monitors == "2" and sv is not None:
			Label2 = gtk.Label()
			head2 = "Single Screen"
			Label2.set_markup("%s: <b>%s x %s</b>" % (head2, single, h))
			Label2.show()
			dialog.vbox.pack_start(Label2, True, True, 0)
			Scroll2 = gtk.ScrolledWindow()
			Scroll2.set_size_request(600, 180)
			Scroll2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
			Scroll2.show()
			dialog.vbox.pack_start(Scroll2, True, True, 0)

			Table2 = gtk.Table(10, 1, False)

			Scroll2.add_with_viewport(Table2)
			Table2.show()

			count = 0
			for x in myMainWallList2:
				count+=1

				event = "event%s" % (count)
				image = "image%s" % (count)

				event = gtk.EventBox()
				image = gtk.Image()
				preview = x.replace("_%s" % swh, "")
				preview = preview.split("/")
				preview = preview[-1]
				PreWall = "%s/%s" % (PreviewUrl, preview)
				FinWall = "%s%s" % (DownloadUrl, x)
				imgurl = urllib2.urlopen(PreWall)
				loader = gtk.gdk.PixbufLoader()
				loader.write(imgurl.read())
				loader.close() 
				image.set_from_pixbuf(loader.get_pixbuf())
				event.connect("button_press_event", self.WallpaperCallback, FinWall, preview, x)
				event.add(image)
				Table2.attach(event, count-1, count, 0, 1, xpadding=5, ypadding=5)
				image.show()
				event.show()
				
		if sv == None and v == None:
			LabelBad = gtk.Label()
			LabelBad.set_markup("Sorry, Couldn't find monitors attached. This is bad, report it.")
			LabelBad.show()
			dialog.vbox.pack_start(LabelBad, True, True, 0)
			
			
		secondTable = gtk.Table(3, 1, False)
		secondTable.show()

		button = gtk.Button("Set")
		button.connect("clicked", self.WallpaperSet)
		button.show()

		checkSpan = gtk.CheckButton("Spanned")
		checkSpan.set_active(False)
		checkSpan.connect("clicked", self.CheckSpanned)
		checkSpan.show()

		checkClean = gtk.CheckButton("Clean folder")
		checkClean.set_active(False)
		checkClean.connect("clicked", self.CheckClean)
		checkClean.show()

		secondTable.attach(button, 0, 1, 0, 1, xpadding=20)
		secondTable.attach(checkSpan, 1, 2, 0, 1, xoptions=gtk.SHRINK,  yoptions=gtk.SHRINK)
		secondTable.attach(checkClean, 2, 3, 0, 1, xoptions=gtk.SHRINK,  yoptions=gtk.SHRINK)

		dialog.vbox.pack_start(secondTable, True, True, 15)

		global SST
		SST.stop()

		dialog.run()
		dialog.destroy()

if __name__ == "__main__":
	SST = SplashScreenThread()
	SST.start()
	time.sleep(1)
	MainThread().start()

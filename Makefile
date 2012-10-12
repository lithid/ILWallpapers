# Makefile for aoscompiler
# By: lithid
SHELL := /bin/bash
NAME := ilwallpapers
VERSION := $(shell head -n1 debian/changelog |cut -d" " -f2 |tr -d "()")
TYPE := $(shell dpkg-architecture |grep "DEB_BUILD_ARCH=" |cut -d"=" -f2)

# Help
help:
	@echo
	@echo "//* $(NAME): $(VERSION)-$(TYPE) *\\"
	@echo
	@echo "Usage: make"
	@echo "debian or [deb-pack|deb-build|deb-clean]"
	@echo

# Definitions
debian: deb-pack deb-install deb-clean

#
# Start debian setup
#
deb-pack:
ifeq ($(wildcard /etc/debian_version),)
	@echo "Not debian, leaving"
	exit 1
else
	@echo "Building $(NAME): $(VERSION)-$(TYPE)"
	-dpkg-buildpackage -rfakeroot
endif

deb-install:
ifeq ($(wildcard /etc/debian_version),)
	@echo "Not debian, leaving"
	exit 1
else
	@echo "Installing $(NAME): $(VERSION)-$(TYPE)"
	-sudo dpkg -i ../${NAME}_${VERSION}_${TYPE}.deb
endif

deb-clean:
ifeq ($(wildcard /etc/debian_version),)
	@echo "Not debian, leaving"
	exit 1
else
	@echo "Cleaning up $(NAME): $(VERSION)-$(TYPE)"
	-rm -rf debian/$(NAME)
	-rm -rf debian/$(NAME).substvars
	-rm -rf debian/*.log
	-rm -rf debian/files
	-rm -rf debian/*debhelper
	-rm -rf ../$(NAME)_*
endif


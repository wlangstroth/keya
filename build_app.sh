#!/usr/bin/env bash

py2applet --make-setup times_table.py
python setup.py py2app
cp -r dist/times_table.app ~/Desktop/

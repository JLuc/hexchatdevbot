#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
          
__module_name__ = "Scribus bugs and commits tracker"
__module_version__ = "0.3 (12/12/2017)"
__module_description__ = "Turns a short bug #1234 into a real url http://bugs.scribus.net/view.php?id=1234 and a 'revision 1234' into a real url http://scribus.net/websvn/comp.php?repname=Scribus&compare[]=%2F@1233&compare[]=%2F@1234"
__author__ = "JLuc - "

from html.parser import HTMLParser
import os
import re
import requests
import threading
import urllib3
import hexchat

events = ("Channel Message", 
# "Channel Action",
#        "Channel Msg Hilight", "Channel Action Hilight",
          "Private Message", "Private Message to Dialog",
#          "Private Action", "Private Action to Dialog",
          "Message send", "Your Message")

url_regex = re.compile("(#[0-9]+)")
 
# including private messages
watched_channels = ("#scribus", "#scribus-test", "#scribus-dev", "#jluc")

def explain_scribus(word, word_eol, userdata, attr=""):
	chan = hexchat.get_info("channel")
	if chan in watched_channels:

		found = re.search(".*r.vision\s*([0-9]+)($|[^0-9].*)", word[1], re.IGNORECASE)
		if found:
			revnum = int(found.group(1))
			hexchat.command ("say * yeah ! http://scribus.net/websvn/comp.php?repname=Scribus&compare[]=%2F@"+str(revnum-1)+"&compare[]=%2F@"+str(revnum)+" (wait a bit when baking page)")

		found = re.search(".*#([0-9]+)($|[^0-9].*)", word[1], re.IGNORECASE)
		if found:
			if int(found.group(1)) > 20:
				hexchat.command("say * hop ! http://bugs.scribus.net/view.php?id="+ found.group(1))

	# treat event as usual after callback
	return hexchat.EAT_NONE

for event in events:
    # hexchat.command("say hook "+event) 
    hexchat.hook_print(event, explain_scribus)

# prnt : que moi voit / say : tout le monde voit comme si je parlais
hexchat.prnt("===")
hexchat.prnt(__module_name__ + " version " + __module_version__ + " loaded")

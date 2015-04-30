#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hexchat
import random
import time

__module_name__ = "BangTheDuck"
__module_version__ = "0.1"
__module_description__ = "Kill the evil duck that resides at #mnfh"


class Duck:
    EVIL = 1
    GOOD = 2

""" Configurations """
min_delay = 1.5
max_delay = 8.0
botname = "CookieBot"
kill_commands = [".bang"]
free_commands = [".befree", ".pokeball"]
all_ducks = {
	"\_.o<" : Duck.EVIL
	,"\_.<" : Duck.EVIL 
	,"\_o<" : Duck.GOOD
	}


def check_duck(word, word_eol, userdata):
	""" Check the messages to see if it actually contains the duck, if yes, fire away """
	#nick, message = word
	nick = word[0]
	message = word[1]
	if nick == botname:
		for duck in all_ducks:
			if duck in message:
				if all_ducks[duck] == Duck.EVIL:
					completeMessage = "say %s" % random.choice(kill_commands)
					simulate_humanism()
					print "\002Killing the evil duck.."
					hexchat.command(completeMessage)
				elif all_ducks[duck] == Duck.GOOD:
					print "\002Freeing the good duck.. "
					completeMessage = "say %s" % random.choice(free_commands)
					simulate_humanism()
					hexchat.command(completeMessage)
	return hexchat.EAT_NONE

def simulate_humanism():
	delay = random.uniform(min_delay, max_delay)
	print "\002Delaying for %d seconds" % delay
	time.sleep(delay)


print "\002%s is loading up it's machine gun." % __module_name__
hexchat.hook_print("Channel Message", check_duck)

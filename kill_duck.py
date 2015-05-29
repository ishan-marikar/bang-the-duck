#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hexchat
import random
import time
import threading

__module_name__ = "BangTheDuck"
__module_version__ = "0.1"
__module_description__ = "Kill the evil duck that resides at #mnfh"


class Duck:
    EVIL = 1
    GOOD = 2
    NEUTRAL = 3

""" Configurations """
min_delay = 2.0
max_delay = 3.0

botnames = {
    "#mnfh": "CookieBot",
    "##duckhunt": "reddit-bot",
    "#test-channel-duck-hunt": "testduck"
    }

kill_commands = {
    "#mnfh": [".bang", ".pewpew"],
    "##duckhunt": [".bang"],
    "#test-channel-duck-hunt": [".bang"]
    }

free_commands = {
    "#mnfh": [".befree", ".pokeball"],
    "##duckhunt": [".befriend", ".bef"],
    "#test-channel-duck-hunt": [".befriend"]
    }

all_ducks = {
    "#mnfh": {
        "\_.o<": Duck.EVIL,
        "\_.<": Duck.EVIL,
        "\_o<": Duck.GOOD
    },

    "##duckhunt": {
        "QUACK": Duck.NEUTRAL,
        "FLAP FLAP": Duck.NEUTRAL,
        "quack": Duck.NEUTRAL
    },

    "#test-channel-duck-hunt": {
        "QUACK": Duck.NEUTRAL,
        "\_.<": Duck.EVIL,
        "\_o<": Duck.GOOD}
    }


def check_duck(word, word_eol, userdata):
    """ Check the messages to see if it actually contains the duck """
    # nick, message = word
    try:
        nick = word[0]
        message = word[1].decode('unicode_escape').encode('ascii', 'ignore')
        current_channel = hexchat.get_info('channel')
        for channel_bots in botnames:
            if channel_bots == current_channel:
                if nick == botnames[channel_bots]:
                    for duck in all_ducks[current_channel]:

                        if duck in message:

                            if all_ducks[current_channel][duck] == Duck.EVIL:
                                completeMessage = "say %s" % random.choice(kill_commands[current_channel])
                                simulate_humanism()
                                print "\002Killing the evil duck on %s" % current_channel
                                hexchat.command(completeMessage)

                            elif all_ducks[current_channel][duck] == Duck.GOOD:
                                print "\002Freeing the good duck on %s" % current_channel
                                completeMessage = "say %s" % random.choice(free_commands[current_channel])
                                simulate_humanism()
                                hexchat.command(completeMessage)

                            elif all_ducks[current_channel][duck] == Duck.NEUTRAL:
                                print "\002Found neutral duck on %s" % current_channel
                                all_commands = []
                                from pprint import pprint
                                all_commands.extend(free_commands[current_channel])
                                all_commands.extend(kill_commands[current_channel])
                                pprint(all_commands)
                                completeMessage = "say %s" % random.choice(all_commands)
                                simulate_humanism()
                                print completeMessage, current_channel
                                hexchat.command(completeMessage)
    except:
        pass

    return hexchat.EAT_NONE


def simulate_humanism():
    delay = random.uniform(min_delay, max_delay)
    print "\002Delaying for %d seconds" % delay
    time.sleep(delay)


def thread(word, word_eol, userdata):
    threading.Thread(
        target=check_duck,
        args=(word, word_eol, userdata)
    ).start()

print "\002%s has loaded it's machine gun. Ready to shoot me some duck." % __module_name__
hexchat.hook_print("Channel Message", thread)

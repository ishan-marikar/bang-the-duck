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
        # Get the current channel
        current_channel = hexchat.get_info('channel')
        # For each bot in the existing bots
        for channel_bots in botnames:
            # check if the existing bot list has entry for the current channel
            if channel_bots == current_channel:
                # .. and if the nick of the sender matches the botname
                if nick == botnames[channel_bots]:
                    # Iterate through all the probable bots for the channel
                    for duck in all_ducks[current_channel]:
                        # If the bot in the list exists in the message
                        if duck in message:
                            # Check what kind of duck it is.
                            # If the duck is EVIL:
                            if all_ducks[current_channel][duck] == Duck.EVIL:
                                # Pick a random kill command
                                completeMessage = "say %s" % random.choice(kill_commands[current_channel])
                                # Delay it for a few seconds so we make it seem more human like
                                simulate_humanism()
                                print "\002Killing the evil duck on %s" % current_channel
                                # Send the command
                                hexchat.command(completeMessage)
                            # If the duck is GOOD:
                            elif all_ducks[current_channel][duck] == Duck.GOOD:
                                completeMessage = "say %s" % random.choice(free_commands[current_channel])
                                print "\002Freeing the good duck on %s" % current_channel
                                simulate_humanism()
                                hexchat.command(completeMessage)
                            # .. or if the duck is neither EVIL or GOOD
                            elif all_ducks[current_channel][duck] == Duck.NEUTRAL:
                                print "\002Found neutral duck on %s" % current_channel
                                # Make an empty list to store the commands
                                all_commands = []
                                # Add both the kill and free commands to our list
                                all_commands.extend(free_commands[current_channel])
                                all_commands.extend(kill_commands[current_channel])
                                completeMessage = "say %s" % random.choice(all_commands)
                                simulate_humanism()
                                hexchat.command(completeMessage)
    # Silently ignore any errors we come across, not really good practice, but meh.
    except:
        pass
    # Let hexchat know that it shouldn't do anything with the existing text event
    return hexchat.EAT_NONE


# The method we call to "humanise"
def simulate_humanism():
    delay = random.uniform(min_delay, max_delay)
    print "\002Delaying for %d seconds" % delay
    time.sleep(delay)


# This is the method that first gets called when the it detects a channel message
# It creates a new thread for every message, so it doesn't freeze hexchat.
def thread(word, word_eol, userdata):
    threading.Thread(
        target=check_duck,
        args=(word, word_eol, userdata)
    ).start()

print "\002%s has loaded it's machine gun. Ready to shoot me some duck." % __module_name__
# Hook on to the "Channel Message" text event
hexchat.hook_print("Channel Message", thread)

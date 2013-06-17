#!/usr/bin/env python

#####################################################################################
#
#    Pipe something to Pidgin.
#    Copyright (C) 2013  Max Rosin  git@hackrid.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#####################################################################################

import dbus
import sys
import os.path

PURPLE_CONV_TYPE_IM = 1

if len(sys.argv) == 1 :
    print("Usage example:")
    print(" echo 'Hello World' | ./pipe2pidgin.py 'yourpidgincontact@example.com'")
    print(" ./pipe2pidgin.py filename 'yourpidgincontact@example.com'")
    sys.exit(-1)

filepath = None
if len(sys.argv) == 3:
    filepath = os.path.realpath(sys.argv[1])
    contact = sys.argv[2]
else:
    contact = sys.argv[1]
    message = sys.stdin.read()


bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

accounts = purple.PurpleAccountsGetAllActive()

for account in accounts:
    buddies = purple.PurpleFindBuddies(account, '')
    for buddy in buddies:
        if (buddy != 0 and purple.PurpleBuddyIsOnline(buddy) and 
                ( purple.PurpleBuddyGetAlias(buddy) == contact or 
                    purple.PurpleBuddyGetName(buddy) == contact )
                ):
            contact = purple.PurpleBuddyGetName(buddy)
            if filepath is None:
                conversation = purple.PurpleConversationNew(PURPLE_CONV_TYPE_IM, account, contact)
                purple.PurpleConvImSend(purple.PurpleConvIm(conversation), message)
            else:
                connection = purple.PurpleAccountGetConnection(account)
                purple.ServSendFile(connection, contact, filepath)
                break

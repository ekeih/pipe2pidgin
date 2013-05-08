#! /usr/bin/python2

import dbus
import sys

if len(sys.argv) != 2:
    print  "Usage example: echo 'Hello World' | ./pipe2pidgin.py '<yourpidgincontact@example.com'"
    sys.exit(-1)

contact = sys.argv[1]
PURPLE_CONV_TYPE_IM = 1

message = sys.stdin.read()

bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

accounts = purple.PurpleAccountsGetAllActive()

for account in accounts:
    buddy = purple.PurpleFindBuddy(account, contact)
    if buddy != 0 and purple.PurpleBuddyIsOnline(buddy):
        conversation = purple.PurpleConversationNew(PURPLE_CONV_TYPE_IM, account, contact)
        purple.PurpleConvImSend(purple.PurpleConvIm(conversation), message)

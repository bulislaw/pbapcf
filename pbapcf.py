#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
#    PBAPcf -- Frontend for PBAP client in obex-client (obexd)    
#
#    Copyright (C) 2011 Bartosz Szatkowski <bulislaw@linux.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


"""Frontend for PBAP client in obexd"""

import sys
import dbus
from dbus.mainloop.glib import DBusGMainLoop

OBEXC_IF = "org.openobex.Client"
PBAP_IF = "org.openobex.PhonebookAccess"

VCARD21 = "vcard21"
VCARD30 = "vcard30"

class PBAPcf(object):

    __bus = None
    __path = None
    __obexc = None
    __pbap = None

    def __init__(self, bt_addr):

        self.__bus = dbus.SessionBus(mainloop = DBusGMainLoop())
        self.__obexc = self.__bus.get_object("org.openobex.client", "/")
        resp = self.__obexc.CreateSession({"Destination" : bt_addr,
                "Target" : "PBAP"}, dbus_interface = OBEXC_IF)

        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        self.__path = resp
        self.__pbap = self.__bus.get_object("org.openobex.client", self.__path)

    def close(self):
        self.__obexc.RemoveSession(self.__path, dbus_interface = OBEXC_IF)

    def select(self, location, folder):
        resp = self.__pbap.Select(location, folder, dbus_interface = PBAP_IF)
        return resp

    def list(self):
        resp = self.__pbap.List(dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return [(unicode(x[0]), unicode(x[1])) for x in resp]

    def pullAll(self):
        resp = self.__pbap.PullAll(dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return resp

    def pull(self, contact):
        resp = self.__pbap.Pull(contact, dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return resp

    def search(self, field, value):
        resp = self.__pbap.Search(field, value, dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return [(unicode(x[0]), unicode(x[1])) for x in resp]

    def getSize(self):
        resp = self.__pbap.GetSize(dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return resp

    def setFormat(self, version):
        resp = self.__pbap.SetFormat(version, dbus_interface = PBAP_IF)

    def setFilter(self, filters):
        resp = self.__pbap.SetFilter(filters, dbus_interface = PBAP_IF)

    def getFilter(self):
        resp = self.__pbap.GetFilter(dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return resp

    def listFilterFields(self):
        resp = self.__pbap.ListFilterFields(dbus_interface = PBAP_IF)
        if not resp:
            print >> sys.stderr, "Error: ", resp
            exit(1)

        return resp

    def setOrder(self, order):
        """'indexed', 'alphanumeric', 'phonetic'"""

        resp = self.__pbap.SetOrder(order, dbus_interface = PBAP_IF)

if __name__ == "__main__":
    con = PBAPcf("00:22:A5:2E:1B:41")
    print con.select("INT", "pb")
    con.setFilter(['TEL',])
    print con.getFilter()
    con.setOrder("indexed")
    print con.pullAll()
    con.close()


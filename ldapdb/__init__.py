# -*- coding: utf-8 -*-
# 
# django-ldapdb
# Copyright (C) 2009-2010 Bolloré telecom
# See AUTHORS file for a full list of contributors.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import ldap

from django.conf import settings
from django.db.backends import BaseDatabaseFeatures, BaseDatabaseOperations

def escape_ldap_filter(value):
    value = str(value)
    return value.replace('\\', '\\5c') \
                .replace('*', '\\2a') \
                .replace('(', '\\28') \
                .replace(')', '\\29') \
                .replace('\0', '\\00')

class DatabaseCursor(object):
    def __init__(self, ldap_connection):
        self.connection = ldap_connection

class DatabaseFeatures(BaseDatabaseFeatures):
    pass

class DatabaseOperations(BaseDatabaseOperations):
    def quote_name(self, name):
        return name

class LdapConnection(object):
    def __init__(self):
        self.connection = None
        self.charset = "utf-8"
        self.features = DatabaseFeatures()
        self.ops = DatabaseOperations()

    def _cursor(self):
        if self.connection is None:
            self.connection = ldap.initialize(settings.LDAPDB_SERVER_URI)
            self.connection.simple_bind_s(
                settings.LDAPDB_BIND_DN,
                settings.LDAPDB_BIND_PASSWORD)
        return DatabaseCursor(self.connection)

    def add_s(self, dn, modlist):
        cursor = self._cursor()
        return cursor.connection.add_s(dn.encode(self.charset), modlist)

    def delete_s(self, dn):
        cursor = self._cursor()
        return cursor.connection.delete_s(dn.encode(self.charset))

    def modify_s(self, dn, modlist):
        cursor = self._cursor()
        return cursor.connection.modify_s(dn.encode(self.charset), modlist)

    def rename_s(self, dn, newrdn):
        cursor = self._cursor()
        return cursor.connection.rename_s(dn.encode(self.charset), newrdn.encode(self.charset))

    def search_s(self, base, scope, filterstr, attrlist):
        cursor = self._cursor()
        results = cursor.connection.search_s(base, scope, filterstr.encode(self.charset), attrlist)
        output = []
        for dn, attrs in results:
            output.append((dn.decode(self.charset), attrs))
        return output

# FIXME: is this the right place to initialize the LDAP connection?
connection = LdapConnection()


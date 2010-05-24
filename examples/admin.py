# -*- coding: utf-8 -*-
# 
# django-granadilla
# Copyright (C) 2009 Bolloré telecom
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

from django.contrib import admin
from examples.models import LdapGroup, LdapUser

class LdapGroupAdmin(admin.ModelAdmin):
    exclude = ['dn', 'usernames']

class LdapUserAdmin(admin.ModelAdmin):
    exclude = ['dn', 'password', 'photo']
    search_fields = ['first_name', 'last_name', 'full_name', 'username']

admin.site.register(LdapGroup, LdapGroupAdmin)
admin.site.register(LdapUser, LdapUserAdmin)

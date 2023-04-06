

from decimal import ROUND_UP, Decimal
from gettext import find
from itertools import zip_longest
import os
from pprint import pprint
from pyexpat import model
import re
import shutil
from statistics import mode
from turtle import backward
from django.views.generic import TemplateView
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
import xmlrpc.client
import ssl


import time



#!/usr/bin/env python3


from asyncore import read
import xmlrpc.client
import ssl






# Begin Login to Odoo#
import requests


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

db='demo'
url='http://localhost:8069'
username='fabiananguiano@gmail.com'
password='214&dallaS'


models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

print(uid)

read_purchase_order_line = models.execute_kw(db, uid, password, 'purchase.order', 'search_read', [[['state', '=', 'draft']]], {'fields': ['name', 'partner_id','date_order']})
print(read_purchase_order_line)

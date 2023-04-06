import ast
from django.views.generic import TemplateView
from asyncore import read
import xmlrpc.client
import ssl
from django.shortcuts import render,redirect
import xmlrpc.client
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
##import variables from .env file
from .odoo_utils import process_po  # Import the process_po function

import os

db = os.environ.get('db')
username = os.environ.get('user')
password = os.environ.get('password')
url = os.environ.get('url')

from django.http import HttpResponse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),allow_none=True,verbose=False, use_datetime=True,context=ssl._create_unverified_context())
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url),allow_none=True,verbose=False, use_datetime=True,context=ssl._create_unverified_context())

uid = common.authenticate(db, username, password, {})



try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def po_loading(request):
    
    read_purchase_order_line = models.execute_kw(db, uid, password, 'purchase.order', 'search_read', [[['state', '=', 'draft']]], {'fields': ['name', 'partner_id','date_order']})
    print(read_purchase_order_line)
    
    
    return render(request, 'po_processing/checkin.html', {'read_purchase_order_line': read_purchase_order_line})

def qc_check(request):
   
    import json

    post_data = request.POST
    print(post_data)

    # Access the 'po' key in the QueryDict
    po_data = post_data.get('po')
    print(po_data)

    # Replace single quotes with double quotes
    po_data = po_data.replace("'", '"')

    # Parse the JSON string
    po_dict = json.loads(po_data)

    # Get the value of the 'name' key
    po_name = po_dict.get('name')
    print(po_name)
    
    read_purchase_order_line = models.execute_kw(db, uid, password, 'purchase.order.line', 'search_read', [[['order_id', '=', po_name]]])
        
    
    return render(request, 'po_processing/qc.html', {'read_purchase_order_line': read_purchase_order_line, 'po_name': po_name})
        
def update(request):
    if request.method == 'POST':
        post_data = request.POST
        po_id = str(post_data.get('name_of_po'))

        for product, original, updatedqty in zip(
                post_data.getlist('product'), post_data.getlist('original'),
                post_data.getlist('updatedqty')):

            purchase_order_line_ids = models.execute_kw(db, uid, password, 'purchase.order.line', 'search_read',
                                                        [[['order_id', '=', po_id], ['product_id', '=', int(product)],
                                                        ['product_qty', '=', float(original)]]])

            # If nothing has changed, do nothing
            if float(original) == float(updatedqty):
                continue

            # If anything has changed, update the purchase order line
            for line in purchase_order_line_ids:
                models.execute_kw(db, uid, password, 'purchase.order.line', 'write', [line['id'], {
                    'product_qty': float(updatedqty)
                }])

        return render(request, 'po_processing/qc.html', {'po_id': po_id})
    else:
        return JsonResponse({'status': 'failed', 'reason': 'Invalid request method'})
    


def process(request):
    get_data = request.GET
    po_name = get_data.get('po_name')  # Get the PO name from the query parameter
   
    # Find the Purchase Order based on the PO name
    po_ids = models.execute_kw(db, uid, password, 'purchase.order', 'search', [[('name', '=', po_name)]])

    # Process the PO (assuming a single PO is found)
    if po_ids:
        po_id = po_ids[0]
        # Perform necessary operations to process the PO
        models.execute_kw(db, uid, password, 'purchase.order', 'button_confirm', [po_id])
        # Additional operations can be added here
        return JsonResponse({'status': 'Success', 'message': 'PO processed successfully'})
    else:
        return JsonResponse({'status': 'Error', 'message': 'PO not found'})

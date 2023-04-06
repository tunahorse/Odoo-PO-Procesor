# odoo_handler.py
import odoorpc
from decouple import config

def process_po(po_name):
    # Get the Odoo login information from the .env file
    odoo_host = config('url').replace('http://', '')  # Remove 'http://' from the URL to get the host
    odoo_port = 8069  # Use the default Odoo port (8069)
    odoo_db = config('db')
    odoo_user = config('user')
    odoo_password = config('password')

    # Establish a connection to the Odoo server
    odoo = odoorpc.ODOO(odoo_host, port=odoo_port)

    # Authenticate
    odoo.login(odoo_db, odoo_user, odoo_password)

    # Find the Purchase Order based on the PO name
    po_model = odoo.env['purchase.order']
    po_ids = po_model.search([('name', '=', po_name)])

    # Process the PO (assuming a single PO is found)
    if po_ids:
        po_id = po_ids[0]
        # Perform necessary operations to process the PO
        po_model.button_confirm([po_id])  # Confirm the PO
        # Additional operations can be added here
        return {'status': 'Success', 'message': 'PO processed successfully'}
    else:
        return {'status': 'Error', 'message': 'PO not found'}

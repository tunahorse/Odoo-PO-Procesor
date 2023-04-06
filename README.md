## Project: Purchase Order Processing (Django Web Application)

This is a Django web application for processing purchase orders (POs). The application provides views and functionalities to handle purchase order loading, quality control checks, updating order quantities, and processing orders. It communicates with an external Odoo ERP system using XML-RPC.

## Features
List draft purchase orders with details such as name, partner, and order date.
Perform quality control checks on purchase order lines.
Update purchase order line quantities.
Process purchase orders and update their state in the Odoo ERP system.

## Dependencies

```python
Python
Django
xmlrpc.client
ssl
ast
asyncore
os
Configuration
The application reads configuration values for the Odoo ERP system from environment variables:

db: The database name of the Odoo ERP system.
user: The username to authenticate with the Odoo ERP system.
password: The password to authenticate with the Odoo ERP system.
url: The base URL of the Odoo ERP system.
```


# Purchase Order Processing Form Application

## Key Functions

### `po_loading(request)`
![alt text](https://github.com/thetrebelcc/Odoo-PO-Procesor/blob/master/screenshots/select_po.png)

 
- Loads draft purchase orders from the Odoo ERP system.
- Renders the `checkin.html` template with the purchase orders.

### `qc_check(request)`
- Receives purchase order information from a POST request.
- Retrieves purchase order lines from the Odoo ERP system for quality control checks.
- Renders the `qc.html` template with the purchase order lines and PO name.
![alt text](https://github.com/thetrebelcc/Odoo-PO-Procesor/blob/master/screenshots/update_po.png)

### `update(request)`

- Handles the form submission for updating purchase order line quantities.
- Updates purchase order lines in the Odoo ERP system.
- Renders the `qc.html` template with the updated PO or returns a JSON response if the request method is invalid.

### `process(request)`
![alt_text](https://github.com/thetrebelcc/Odoo-PO-Procesor/blob/master/screenshots/submit_form.png)

- Receives the purchase order name from a GET request query parameter.
- Processes the purchase order in the Odoo ERP system.
- Returns a JSON response indicating the success or failure of processing the PO.

## Usage

1. Set the required environment variables (`db`, `user`, `password`, `url`) for connecting to the Odoo ERP system.
2. Run the Django application and access the provided URLs to perform the various purchase order processing functionalities.

## Note

This README is a brief overview of the project. For detailed usage and understanding of the code, refer to the project's codebase and comments.

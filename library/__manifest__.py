# -*- coding: utf-8 -*-
{
    'name':        "Library Management",

    'summary':
                   """
                   Library management
                   """,

    'description': """
        Manage a Library: customers, books, etc.... 
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'Library',
    'version':     '0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base', 'product', 'mail', 'contacts'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        "views/books.xml",
        "views/partners.xml",
        "views/rentals.xml",
        "views/copies.xml",
        "views/price.xml",
        "wizard/wizard.xml",
        "views/menuitems.xml",
        "data/price_data.xml",
        "data/partner_data.xml",
        "templates/payment_notification.xml"
    ],
    # only loaded in demonstration mode
    'demo':        [],
    'license': 'AGPL-3',
}

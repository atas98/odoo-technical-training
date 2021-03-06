# -*- coding: utf-8 -*-
{
    'name':
    "openacademy",
    'summary':
    """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description':
    """
        Long description of module's purpose
    """,
    'author':
    "My Company",
    'website':
    "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':
    'Uncategorized',
    'version':
    '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'mail', 'product', 'account', 'website'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/openacademy_data.xml',
        'wizard/wizard.xml',
        'views/courses.xml',
        'views/sessions.xml',
        'views/partners.xml',
        'views/reports.xml',
        'views/templates.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/data.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "Football Module",
    'description': "This module is designed to test the functionality related to describing football players.",
    'author': "Minh Nguyen Binh _ Intern BAP",
    'website': 'https://bap.bemo-cloud.com/',  # Optional website
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Custom',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': ['security/player_security.xml',
             'security/ir.model.access.csv',
             'views/player_views.xml'
             ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,          # Specify if the module is installable
    'application': True,         # Specify if it's an application
    'auto_install': False,
    'test': [],
}

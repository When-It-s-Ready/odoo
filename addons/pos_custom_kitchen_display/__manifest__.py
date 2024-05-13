# -*- coding: utf-8 -*-
{
    'name': 'POS Kitchen Screen',
    'description': 'POS Kitchen Screen generates a panel for the kitchen to be able '
                    'to see and handle the preparation of the POS orders.',
    'summary': 'POS Kitchen Screen generates a panel for the kitchen to be able '
               'to see and handle the preparation of the POS orders.',
    'category': 'Point Of Sale',
    'version': '17.0.1.0.1',
    'depends': ['point_of_sale', 'pos_restaurant'],
    'data': [
        "security/ir.model.access.csv",
        "views/pos_custom_kitchen_display_views.xml",
        "views/pos_custom_kitchen_display_menus.xml",
        
    ],
    'assets': {
        'web.assets_backend': [
            'pos_custom_kitchen_display/static/src/app/kitchen_display_dashboard/kitchen_display_dashboard.js',
            'pos_custom_kitchen_display/static/src/app/kitchen_display_dashboard/kitchen_display_dashboard.xml',
        ],
    },
    'images': [
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
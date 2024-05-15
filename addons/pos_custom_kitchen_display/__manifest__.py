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
        "views/templates.xml"
    ],
    'assets': {
        'pos_custom_kitchen_display.assets_display': [
            # bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap_backend'),

            # required for fa icons
            'web/static/src/libs/fontawesome/css/font-awesome.css',
            
            # include base files from framework
            ('include', 'web._assets_core'),

            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',
            # add the kitchen display files
            # 'pos_custom_kitchen_display/static/src/app/services/*',
            'pos_custom_kitchen_display/static/src/app/*',
            'pos_custom_kitchen_display/static/src/app/kitchen_display_dashboard/*'
        ],
    },
    'images': [
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
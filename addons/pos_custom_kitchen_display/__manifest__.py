# -*- coding: utf-8 -*-
{
    'name': 'POS Custom Kitchen Display',
    'description': 'POS Custom Kitchen Display allows kitchen panels to be able to see tickets that correspond to orders accepted through the point of Sale System.',
    'summary': 'POS Custom Kitchen Display allows kitchen panels to be able to see tickets that correspond to orders accepted through the point of Sale System.',
    'category': 'Point Of Sale',
    'version': '17.0.1.0.1',
    'depends': ['point_of_sale', 'pos_restaurant'],
    'data': [
        "data/ir_cron_data.xml",
        "security/ir.model.access.csv",
        "views/pos_custom_kitchen_display_views.xml",
        "views/pos_custom_kitchen_display_menus.xml",
        "views/product_view.xml",
        "views/templates.xml"
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_custom_kitchen_display/static/src/overrides/*'
        ],
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
            # sound origin https://pixabay.com/sound-effects/livechat-129007/
            'pos_custom_kitchen_display/static/src/sound/*',
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
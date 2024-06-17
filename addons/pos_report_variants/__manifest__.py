# -*- coding: utf-8 -*-
{
    'name': 'POS Report Variants',
    'description': 'POS Report addon to allow generating a products sales report that takes into account the product variants, if those are on never create mode.',
    'summary': 'POS Report addon to allow generating a products sales report that takes into account the product variants, if those are on never create mode. This is based on the code of the Point of sale reports.',
    'category': 'Point Of Sale',
    'version': '17.0.1.0.1',
    'depends': ['point_of_sale', 'pos_restaurant'],
    'data': [
        "security/ir.model.access.csv",
        "views/report_variantsdetails.xml",
        "views/details_report_variants.xml",
        "views/pos_report_variants.xml",
        "views/pos_report_variants_menu.xml",
        "views/pos_category_view.xml"
    ],
    'assets': {
    },
    'images': [
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
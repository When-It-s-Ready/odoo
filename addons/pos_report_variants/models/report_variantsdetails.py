# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta

import pytz

from odoo import api, fields, models, _
from odoo.osv.expression import AND

class ReportVariantsDetails(models.AbstractModel):

    _name = 'report.pos_report_variants.report_variantsdetails'
    _description = 'Pos product Report with variants details'


    @api.model
    def get_sale_details(self, session_ids=False):
        """ Serialise the orders of the requested time period.
        :type session_ids: list of numbers.
        :returns: dict -- Serialised sales.
        """
        domain = [('state', 'in', ['paid', 'invoiced', 'done'])]
        if (session_ids):
            domain = AND([domain, [('session_id', 'in', session_ids)]])

        orders = self.env['pos.order'].search(domain)

        config_currencies = self.env['pos.session'].search([('id', 'in', session_ids)]).mapped('config_id.currency_id')
        # If all the pos.config have the same currency, we can use it, else we use the company currency
        if config_currencies and all(i == config_currencies.ids[0] for i in config_currencies.ids):
            user_currency = config_currencies[0]
        else:
            user_currency = self.env.company.currency_id

        total = 0.0
        products_sold = {}
        refund_done = {}
        all_total = 0
        all_qty = 0
        ref_total = 0
        ref_qty = 0
        for order in orders:
            if user_currency != order.pricelist_id.currency_id:
                total += order.pricelist_id.currency_id._convert(
                    order.amount_total, user_currency, order.company_id, order.date_order or fields.Date.today())
            else:
                total += order.amount_total
            currency = order.session_id.currency_id

            for line in order.lines:
                variant = '-'
                if line.attribute_value_ids:
                    variant = ", ".join([attr.name for attr in line.attribute_value_ids])
                
                if line.qty >= 0:
                    products_sold, all_total, all_qty = self._get_products_dict(line, variant, products_sold, all_total, all_qty)
                else:
                    refund_done, ref_total, ref_qty = self._get_products_dict(line, variant, refund_done, ref_total, ref_qty)

        sessions = self.env['pos.session'].search([('id', 'in', session_ids)])

        products = []
        refund_products = []
        for category_name, product_list in products_sold.items():
            category_dictionnary = {
                'name': category_name,
                'products': sorted([{
                    'product_id': product.id,
                    'product_name': product.name,
                    'code': product.default_code,
                    'variants': [{
                        'name': var,
                        'quantity': qty,
                        'price_unit': price_unit,
                        'discount': discount,
                        'uom': product.uom_id.name,
                        'total_paid': product_total,
                        'base_amount': base_amount,
                    } for (var, price_unit, discount), (qty, product_total, base_amount) in variants.items()]
                } for product, variants in product_list.items()], key=lambda l: l['product_name']),
            }
            products.append(category_dictionnary)
        products = sorted(products, key=lambda l: str(l['name']))

        for category_name, product_list in refund_done.items():
            category_dictionnary = {
                'name': category_name,
                'products': sorted([{
                    'product_id': product.id,
                    'product_name': product.name,
                    'code': product.default_code,
                    'variants': [{
                        'name': var,
                        'quantity': qty,
                        'price_unit': price_unit,
                        'discount': discount,
                        'uom': product.uom_id.name,
                        'total_paid': product_total,
                        'base_amount': base_amount,
                    } for (var, price_unit, discount), (qty, product_total, base_amount) in variants.items()]
                } for product, variants in product_list.items()], key=lambda l: l['product_name']),
            }
            refund_products.append(category_dictionnary)
        refund_products = sorted(refund_products, key=lambda l: str(l['name']))

        products = self._get_total_and_qty_per_category(products)
        refund_products = self._get_total_and_qty_per_category(refund_products)

        currency = {
            'symbol': user_currency.symbol,
            'position': True if user_currency.position == 'after' else False,
            'total_paid': user_currency.round(total),
            'precision': user_currency.decimal_places,
        }

        session_name = False
        if len(sessions) == 1:
            state = sessions[0].state
            date_start = sessions[0].start_at
            date_stop = sessions[0].stop_at
            session_name = sessions[0].name
        else:
            state = "multiple"

        return {
            'opening_note': sessions[0].opening_notes if len(sessions) == 1 else False,
            'closing_note': sessions[0].closing_notes if len(sessions) == 1 else False,
            'state': state,
            'currency': currency,
            'nbr_orders': len(orders),
            'date_start': date_start,
            'date_stop': date_stop,
            'session_name': session_name if session_name else False,
            'company_name': self.env.company.name,
            'products': products,
            'products_info': {'total' : all_total, 'qty': all_qty},
            'refund_info': {'total' : ref_total, 'qty': ref_qty},
            'refund_products': refund_products,
        }

    def _get_products_dict(self, line, variant, products, total, qty):
        key2 = line.product_id
        key3 = (variant, line.price_unit, line.discount)
        keys1 = []
        for cat in line.product_id.product_tmpl_id.pos_categ_ids:
            print(cat, cat.toReport)
            if cat.toReport == True:
                keys1.append(cat.name)
        if keys1 == []:
            keys1 = ['Not Categorized']

        for key1 in keys1:
            products.setdefault(key1, {})
            products[key1].setdefault(key2, {})
            products[key1][key2].setdefault(key3, [0.0, 0.0, 0.0])
            products[key1][key2]
            products[key1][key2][key3][0] += line.qty
            products[key1][key2][key3][1] += line.currency_id.round(line.price_unit * line.qty * (100 - line.discount) / 100.0)
            products[key1][key2][key3][2] += line.price_subtotal
        
        total += line.price_subtotal
        qty += line.qty

        return products, total, qty

    def _get_total_and_qty_per_category(self, categories):
        all_qty = 0
        all_total = 0
        for category_dict in categories:
            qty_cat = 0
            total_cat = 0
            for product in category_dict['products']:
                for var in product['variants']:
                    qty_cat += var['quantity']
                    total_cat += var['base_amount']
            category_dict['total'] = total_cat
            category_dict['qty'] = qty_cat
        # IMPROVEMENT: It would be better if the `products` are grouped by pos.order.line.id.
        return categories

    @api.model
    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        # # initialize data keys with their value if provided, else None
        data.update({
        #     #If no data is provided it means that the report is called from the PoS, and docids represent the session_id
            'session_ids': data.get('session_ids') ,
        #     'config_ids': data.get('config_ids'),
        #     'date_start': data.get('date_start'),
        #     'date_stop': data.get('date_stop')
        })
        # configs = self.env['pos.config'].browse(data['config_ids'])
        if 'session_ids' in data:
            data.update(self.get_sale_details(data['session_ids']))
        return data

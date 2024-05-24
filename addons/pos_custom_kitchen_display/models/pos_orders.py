# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json
import logging
_logger = logging.getLogger(__name__)



class PosOrder(models.Model):
    _inherit = "pos.order"
    
    # line_satus = fields.Selection(string="Line Status",
    #                                 selection=[("pending", "Pending"),
    #                                            ("done", "Done"),
    #                                            ("cancel", "Cancel")],
    #                                 help='To know the status of the ticket')
    kitchen_tickets = fields.One2many("kitchen.ticket", "order_ref", string = "List of tickets")
    ticket_count = fields.Integer(string="Ticket counter", help="Keeps the number of kitchen tickets created for this order", default = 0)

    @api.model
    def _process_order(self, order, draft, existing_order):
        if existing_order:
            last  = existing_order.last_order_preparation_change
        else:
            last = '{}'

        oid = super(PosOrder, self)._process_order(order, draft, existing_order)
        ord =  self.env['pos.order'].search([('id', '=', oid)], limit=1)
        diffs = ord.order_difference(json.loads(last))

        diff = diffs['new']
        if diff !={}:
            ord.ticket_count = ord.ticket_count + 1
            ticket = self.env['kitchen.ticket'].create(
                {
                    'order_ref': oid,
                    'table': ord.table_id.id,
                }
            )

            for item in diff:
                # TODO check that item should really go to kitchen
                self.env['kitchen.ticket.line'].create(
                    {
                        'ticket_id' : ticket.id,
                        'product_id' : int(diff[item]['product_id']),
                        'name' : diff[item]['name'],
                        'qty' : diff[item]['quantity'],
                        'note' : diff[item]['note']
                    }
                )
            
        cancels = diffs['canceled']
        if cancels:
            for item in cancels:
                tickets = self.env['kitchen.ticket'].search(
                    [
                        ("order_ref","=",ord.id), 
                        ("ticket_status", '!=', "done"),
                        ("lines", "any", [('product_id', "=", cancels[item]['product_id'])]),
                    ], order="create_date desc")
                if tickets:
                    for ticket in tickets:
                        for line in ticket.lines:
                            if(line.product_id.id == cancels[item]['product_id'] and (line.line_status =="pending" or line.line_status =="attention")):
                                line.change_to_cancel()
                                cancels[item]['to_delete'] -= line.qty
                                break
                        if(cancels[item]['to_delete'] <= 0):
                            break
                    if(cancels[item]['quantity'] > 0 and cancels[item]['to_delete'] <= 0):
                        self.env['kitchen.ticket.line'].create(
                            {
                                'ticket_id' : tickets[0].id,
                                'product_id' : int(cancels[item]['product_id']),
                                'name' : cancels[item]['name'],
                                'qty' : cancels[item]['quantity'],
                                'note' : cancels[item]['note'],
                                'line_status': 'attention'
                            }
                        )
        return oid

        
    def order_difference(self, old):
        curr = json.loads(self.last_order_preparation_change)
        print(curr)
        diff = {
            'new': {},
            'canceled': {}
        }
        for item in list(curr.keys())+list(old.keys()):
            if item in curr and item in old:
                if curr[item]['quantity'] > old[item]['quantity']:
                    diff['new'][curr[item]['line_uuid']] = curr[item].copy()
                    diff['new'][curr[item]['line_uuid']]['quantity'] -= old[item]['quantity']
                elif curr[item]['quantity'] < old[item]['quantity']:
                    # DELETION
                    diff['canceled'][curr[item]['line_uuid']] = curr[item].copy()
                    diff['canceled'][curr[item]['line_uuid']]['to_delete'] = old[item]['quantity']-curr[item]['quantity']

            elif item in curr and item not in old:
                if(curr[item]['quantity'] > 0):
                    diff['new'][curr[item]['line_uuid']] = curr[item].copy()
            else:
                if(old[item]['quantity'] > 0):
                    diff['canceled'][old[item]['line_uuid']] = old[item].copy()
                    diff['canceled'][old[item]['line_uuid']]['quantity'] = 0
                    diff['canceled'][old[item]['line_uuid']]['to_delete'] = old[item]['quantity']

        return diff
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
        diff = ord.order_difference(json.loads(last))
        
        if diff !={}:
            ord.ticket_count = ord.ticket_count + 1
            ticket = self.env['kitchen.ticket'].create(
                {
                    'order_ref': oid,
                    'table': ord.table_id.id,
                    'items': json.dumps(diff)
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

            
        return oid

        
    def order_difference(self, old):
        curr = json.loads(self.last_order_preparation_change)
        diff = {}
        for item in list(curr.keys())+list(old.keys()):
            if item in curr and item in old:
                if curr[item]['quantity'] != old[item]['quantity']:
                    diff[curr[item]['line_uuid']] = curr[item].copy()
                    diff[curr[item]['line_uuid']]['quantity'] -= old[item]['quantity']
            elif item in curr and item not in old:
                diff[curr[item]['line_uuid']] = curr[item].copy()
            else:
                diff[old[item]['line_uuid']] = old[item].copy()
                diff[old[item]['line_uuid']]['quantity'] = -old[item]['quantity']
        return diff
    
class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    
    ticket_id = fields.Many2one("kitchen.ticket")
    ticket_selection = fields.Selection(
        selection = [('empty', 'Unassigned'), ('assigned', 'Assigned')], default = 'empty'
    )
# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json


# alter the PosOrder model from the point_of_sale addon to support ticket generation
class PosOrder(models.Model):
    _inherit = "pos.order"
    
    # references possibly multiple tickets that are part of the order
    kitchen_tickets = fields.One2many("kitchen.ticket", "order_ref", string = "List of tickets")
    # the number of those tickets
    ticket_count = fields.Integer(string="Ticket counter", help="Keeps the number of kitchen tickets created for this order", default = 0)

    # extends _process_order in order to generate tickets based on the differences between the previous order 
    # during changes in an order, the PosOrder model deletes all PosOrderLines and creates new ones
    # therefore since we want to find the differences between the previous status of the order and the new one,
    # we use the field last_order_preparation_change, that fully describes the order as json string
    @api.model
    def _process_order(self, order, draft, existing_order):
        # if an existing order is to be altered, we store the previous status of the order to calculate the differences
        if existing_order:
            last  = existing_order.last_order_preparation_change
        else:
            last = '{}'

        # call the original function to not break anything
        oid = super(PosOrder, self)._process_order(order, draft, existing_order)

        # get the updated order and find differences with the previous one
        # order_difference returns a dictionary with products that need to be added and possibly cancelations
        ord =  self.env['pos.order'].search([('id', '=', oid)], limit=1)
        diffs = ord.order_difference(json.loads(last))

        # for products that need to be added, we create a new ticket to send to the kitchen displays
        diff = diffs['new']
        if diff !={}:
            ord.ticket_count = ord.ticket_count + 1
            ticket = self.env['kitchen.ticket'].create(
                {
                    # link it to the specific order
                    'order_ref': oid,
                    'table': ord.table_id.id,
                }
            )

            for item in diff:

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
                # for canceled products we need to pull up the tickets that are part of this order and contain the canceled product
                # we only look for unfinished tickets, since it does not make any sense to alter an already completed ticket
                # this returns the tickets sorted from the latest to the earliest, since it is more probable that lines in newer tickets have not been completed yet
                tickets = self.env['kitchen.ticket'].search(
                    [
                        ("order_ref","=",ord.id), 
                        ("ticket_status", '!=', "done"),
                        ("lines", "any", [('product_id', "=", cancels[item]['product_id'])]),
                    ], order="create_date desc")
                if tickets:
                    # for each product, we keep the quantity that needs to be removed in the 'to_delete' field. 
                    # and the new quantity that we need in the 'quantity' field
                    # we are looking through the tickets we got, in order to find unfinished lines of that product and cancel them, up to the specified qty
                    for ticket in tickets:
                        for line in ticket.lines:
                            # any line that is found this way is canceled
                            if(line.product_id.id == cancels[item]['product_id'] and (line.line_status =="pending" or line.line_status =="attention")):
                                line.change_to_cancel()
                                cancels[item]['to_delete'] -= line.qty
                                break
                        if(cancels[item]['to_delete'] <= 0):
                            break
                    
                    # if we managed to delete enough items and the new required quantity is more than 0, then we have to generate a new ticket line for that product
                    # we do that in the latest ticket (ticket[0]) for that order
                    # since this comes from a cancelation, it gets the attention status
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

        
    # calculates the differences during an order change
    def order_difference(self, old):
        curr = json.loads(self.last_order_preparation_change)
        print(curr)
        diff = {
            'new': {},
            'canceled': {}
        }
        for item in list(curr.keys())+list(old.keys()):

            # if an item exists both in the previous and current status of the order, 
            # the quantity will show us if extra needs to be added, or removed
            if item in curr and item in old:
                if curr[item]['quantity'] > old[item]['quantity']:
                    diff['new'][curr[item]['line_uuid']] = curr[item].copy()
                    diff['new'][curr[item]['line_uuid']]['quantity'] -= old[item]['quantity']
                elif curr[item]['quantity'] < old[item]['quantity']:
                    # Cancelation
                    diff['canceled'][curr[item]['line_uuid']] = curr[item].copy()
                    diff['canceled'][curr[item]['line_uuid']]['to_delete'] = old[item]['quantity']-curr[item]['quantity']

            # if an item only exists in the current order, then it is addition for sure
            elif item in curr and item not in old:
                if(curr[item]['quantity'] > 0):
                    diff['new'][curr[item]['line_uuid']] = curr[item].copy()

            # similarly if an item only exists in the old order, then it is cancelation
            else:
                if(old[item]['quantity'] > 0):
                    diff['canceled'][old[item]['line_uuid']] = old[item].copy()
                    diff['canceled'][old[item]['line_uuid']]['quantity'] = 0
                    diff['canceled'][old[item]['line_uuid']]['to_delete'] = old[item]['quantity']

        return diff
# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime, timedelta


# Entity of Kitchen Tickets in the database
class KitchenTicket(models.Model):
    _name = "kitchen.ticket"
    _description ="POS Kitchen Tickets for orders"
    _rec_name = 'order_ref'

    # references the order that created the ticket
    order_ref = fields.Many2one("pos.order", string="Order Id") 
    # represents the current status of the ticket
    ticket_status = fields.Selection(string="Ticket Status",
                                    selection=[("pending", "Received"),
                                               ("ack", "In progress"),
                                               ("done", "Ready"),
                                               ("cancel", "Cancel")],
                                    help='To know the status of the ticket', default = 'pending')
    # references each product that is part of the ticket (kitchen ticket line)
    lines = fields.One2many("kitchen.ticket.line", "ticket_id", string = "Ticket lines")
    # references the table that each ticket comes from
    table = fields.Many2one("restaurant.table", string="Table")

    
    # function to check if all ticket lines within this ticket are completed or canceled
    # used to transition the ticket in the done state
    def check_all_lines_done(self):
        for line in self.lines:
            if line.line_status == 'pending' or line.line_status =='attention':
                return False
        return True
    
    # function to check if all ticket lines are canceled
    # used to transition ticket in cancel state
    def check_all_lines_cancel(self):
        for line in self.lines:
            if line.line_status != 'cancel':
                return False
        return True

    # function to change the ticket status
    # a ticket normally goes ack -> pending -> done
    # to transition to done, all ticket lines must be completed
    # a ticket that has all lines canceled will transition to cancel
    def change_ticket_status(self):
        if self.check_all_lines_cancel():
            self.ticket_status = 'cancel'
            return 'cancel'
        if self.ticket_status == 'pending':
            self.ticket_status = "ack"
        elif self.ticket_status == 'ack':
            if self.check_all_lines_done():
                self.ticket_status = 'done'
        return self.ticket_status

    # called from the kitchen display clients to update the status of a ticket
    # returns the status that the ticket should now have
    def update_status_ui(self, ticket_id):
        ticket = self.env['kitchen.ticket'].search([("id", "=", ticket_id)])
        if ticket:
            res = { "status": ticket.change_ticket_status()}
        else:
            res = { "status": "error" }
        return res

                
    # called from the ticket_polling function in Kitchen_Display in order to generate the required fields for the ui
    def export_for_ui(self):
        return {
            'id': self.id,
            'order_ref': self.order_ref.id,
            'ticket_status': self.ticket_status,
            'lines': [line.export_for_ui() for line in self.lines],
            'table': self.table.name,
            'time': self.create_date.strftime("%H:%M"),
        }

    # cron job to delete day-old tickets
    # called from data/ir_cron_data.xml
    def delete_old_tickets(self, days = 5):
        del_time = datetime.now() - timedelta(days=days)
        tickets = self.env['kitchen.ticket'].search([('create_date', '<', del_time)])
        for ticket in tickets:
            for line in ticket.lines:
                line.unlink()
            ticket.unlink()

    

# represents the product line for each ticket
class KitchenTicketLine(models.Model):
    _name = "kitchen.ticket.line"
    _description = "Entry line for a Kitchen Ticket"
    _rec_name = "product_id"
    
    # references the ticket that is part of
    ticket_id = fields.Many2one('kitchen.ticket', string= "Ticket Id")

    # references the product that it describes
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], required=True)

    # the name of the product
    name = fields.Char(string=" Product Name")

    # the quantity of the product for this ticket
    qty = fields.Float('Quantity', digits='Product Unit of Measure', default = 1)

    # any internal note that may be present for this product
    note = fields.Char(string= 'Note', help="Internal note for the kitchen")

    # the preparation status of this product in the ticket
    # attention and att_done are used for products that have been altered by cancelations
    line_status = fields.Selection(string="Line Status",
                                   selection=[("pending", "Pending"), ("done","Ready"), ('cancel', "Cancel"), ('attention', "Attention"), ('att_done', "Attention Ready")], help="Status of the ticket line", default = 'pending')

    # move ticket line to ready status
    def change_line_status(self):
        if self.line_status == 'pending':
            self.line_status = 'done'
        elif self.line_status == 'attention':
            self.line_status = 'att_done'
        return self.line_status
    

    # called from the kitchen display clients, to update the status of a ticket line
    def update_line_status_ui(self, line_id):
        line = self.env['kitchen.ticket.line'].search([("id", "=", line_id)])
        if line:
            res = { "status": line.change_line_status()}
        else:
            res = { "status": "error" }
        return res
        
    
    # cancels the ticket line
    def change_to_cancel(self):
        self.line_status = 'cancel'

    # called during ticket_polling, to generate the required line data for the ui
    def export_for_ui(self):
        return {
            'id': self.id,
            'product_id': self.product_id.id,
            'name': self.name,
            'qty': self.qty,
            'note': self.note,
            'line_status': self.line_status
        }
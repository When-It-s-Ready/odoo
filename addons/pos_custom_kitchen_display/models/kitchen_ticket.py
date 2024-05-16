# -*- coding: utf-8 -*-
from odoo import fields, models

class KitchenTicket(models.Model):
    _name = "kitchen.ticket"
    _description ="POS Kitchen Tickets for orders"
    _rec_name = 'order_ref'

    order_ref = fields.Many2one("pos.order", string="Order Id") 
    ticket_status = fields.Selection(string="Ticket Status",
                                    selection=[("pending", "Received"),
                                               ("ack", "In progress"),
                                               ("done", "Ready"),
                                               ("cancel", "Cancel")],
                                    help='To know the status of the ticket', default = 'pending')
    lines = fields.One2many("kitchen.ticket.line", "ticket_id", string = "Ticket lines")
    table = fields.Many2one("restaurant.table", string="Table")
    # TODO not needed as well create_date exists 
    create_time = fields.Datetime('Creation date', required=True, readonly=False,
                                  default=lambda self: fields.datetime.now())
    # TODO delete this
    items = fields.Char(string = "Items")


    def check_all_lines_done(self):
        for line in self.lines:
            if line.line_status == 'pending':
                return False
        return True

    
    def change_ticket_status(self):
        if self.ticket_status == 'pending':
            self.ticket_status = "ack"
        elif self.ticket_status == 'ack':
            if self.check_all_lines_done():
                self.ticket_status = 'done'
        return self.ticket_status

                
    def export_for_ui(self):
        return {
            'id': self.id,
            'order_ref': self.order_ref.id,
            'ticket_status': self.ticket_status,
            'lines': [line.export_for_ui() for line in self.lines],
            'table': self.table.name,
            'create_time': self.create_date.strftime("%H:%M")
        }
    

    def sendIfActive(self):
        actives = self.env['kitchen.display'].search_count([('active','=','true')])
        if actives != 0:
            tickets = self.export_for_ui()
            self.env['bus.bus']._sendone("new_ticket", "new_ticket", {"tickets": tickets})

    

class KitchenTicketLine(models.Model):
    _name = "kitchen.ticket.line"
    _description = "Entry line for a Kitchen Ticket"
    _rec_name = "product_id"
    
    ticket_id = fields.Many2one('kitchen.ticket', string= "Ticket Id")
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], required=True)
    name = fields.Char(string=" Product Name")
    qty = fields.Float('Quantity', digits='Product Unit of Measure', default = 1)
    note = fields.Char(string= 'Note', help="Internal note for the kitchen")
    line_status = fields.Selection(string="Line Status",
                                   selection=[("pending", "Pending"), ("done","Ready"), ('cancel', "Cancel")], help="Status of the ticket line", default = 'pending')

    def change_line_status(self):
        if self.line_status == 'pending':
            self.line_status = 'done'
        return self.line_status
    
    def change_to_cancel(self):
        self.line_status = 'cancel'

    def export_for_ui(self):
        return {
            'product_id': self.product_id.id,
            'name': self.name,
            'qty': self.qty,
            'note': self.note,
            'line_status': self.line_status
        }
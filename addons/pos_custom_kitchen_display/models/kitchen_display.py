# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime, date

# Object for the Kitchen display, multiple can be created to allow for extra customization (e.g. restrict types of products for each screen)
class KitchenDisplay(models.Model):
    _name = "kitchen.display"
    _description ="POS Kitchen Screen"

    # time to track which tickets to poll. 
    # will poll tickets that are newer than init_time
    init_time = fields.Datetime('Initial time value for ticket gathering', required=True, readonly=False,
                                  default=lambda self: fields.datetime.now())
    
    # Display name for each object
    name = fields.Char(help="Display Name", required=True, default="Kitchen Display")

    # references the ticket categories that this screen accepts
    ticket_category = fields.Many2many("kitchen.ticket.category", string= "Ticket categories")
    # ticket_polling time from the frontend
    success_polling = fields.Integer(string="Polling time (seconds)", help="Set the polling time in seconds for successful polling requests", default = 5)
    # error polling time for missed requests from frontend
    error_polling = fields.Integer(string="Error Polling time (seconds)", help="Set the polling time in seconds for missed polling requests", default = 10)
    # threshold for missed requests upon which frontend will have to check server status
    missed_thresh = fields.Integer(string="Error Threshold", help="Set up the limit of failed requests from frontend to notify the client", default = 6)


    # function to open the kitchen display
    # called from the backend screen
    def open_ui(self):
        return {
            'type': 'ir.actions.act_url',
            'url': "/kdisplay" + '?disp_id=%d&ps=%d&eps=%d&thr=%d' % (self.id, self.success_polling, self.error_polling, self.missed_thresh) ,
            'target': 'self',
        }

    # resets the init_time to today-midnight
    # called from the backend screen
    def reset(self):
        self.init_time = datetime.combine(date.today(), datetime.min.time())
        return

    # polls and returns the tickets to be displayed
    # called from the display screen clients
    def ticket_polling(self, disp_id):
        disp = self.env['kitchen.display'].search([("id", "=", disp_id)])
        tickets = self.env['kitchen.ticket'].search([
            ("create_date", ">", disp.init_time), ("ticket_category", "in", disp.ticket_category.ids)], order="create_date desc")
        res = { "tickets": [ticket.export_for_ui() for ticket in tickets]}
        return res
        
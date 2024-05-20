# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime, date


class KitchenDisplay(models.Model):
    _name = "kitchen.display"
    _description ="POS Kitchen Screen"


    # maybe not needed
    pos_id = fields.Char(help="Id of the corresponding pos system")
    active = fields.Boolean(help="Check if display is currently connected", default = "false")
    last_ticket = fields.Datetime('Last polled time')


    def open_ui(self):
        return {
            'type': 'ir.actions.act_url',
            'url': "/kdisplay" + '?disp_id=%d' % self.id,
            'target': 'self',
        }
                


    def start_ticket_polling(self, disp_id):
        disp = self.env['kitchen.display'].search([("id", "=", disp_id)])
        dt = datetime.combine(date.today(), datetime.min.time())
        tickets = self.env['kitchen.ticket'].search([("create_date", ">", dt)], order="create_date desc")
        res = { "tickets": [ticket.export_for_ui() for ticket in tickets]}
        if tickets:
            disp.last_ticket = tickets[0].create_date
        
        return res

    def get_next_tickets(self, disp_id):
        disp = self.env['kitchen.display'].search([("id", "=", disp_id)])
        tickets = self.env['kitchen.ticket'].search([("create_date",">",disp.last_ticket)], order="create_date desc")
        if tickets:
            disp.last_ticket = tickets[0].create_date
        res = { "tickets": [ticket.export_for_ui() for ticket in tickets]}
        return res

        
    # TODO: kitchen screen filter tickes by today

    def setActive(self):
        self.active = True

    def setInactive(self):
        self.active = False
        
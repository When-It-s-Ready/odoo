# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime, date


class KitchenDisplay(models.Model):
    _name = "kitchen.display"
    _description ="POS Kitchen Screen"


    init_time = fields.Datetime('Initial time value for ticket gathering', required=True, readonly=False,
                                  default=lambda self: fields.datetime.now())
    

    name = fields.Char(help="Display Name", required=True, default="Kitchen Display")


    def open_ui(self):
        return {
            'type': 'ir.actions.act_url',
            'url': "/kdisplay" + '?disp_id=%d' % self.id,
            'target': 'self',
        }

    def reset(self):
        self.init_time = datetime.combine(date.today(), datetime.min.time())
        return


    def ticket_polling(self, disp_id):
        disp = self.env['kitchen.display'].search([("id", "=", disp_id)])
        tickets = self.env['kitchen.ticket'].search([("create_date", ">", disp.init_time)], order="create_date desc")
        res = { "tickets": [ticket.export_for_ui() for ticket in tickets]}
        return res
        
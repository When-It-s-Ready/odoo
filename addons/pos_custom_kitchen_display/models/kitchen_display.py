# -*- coding: utf-8 -*-
from odoo import fields, models


class KitchenDisplay(models.Model):
    _name = "kitchen.display"
    _description ="POS Kitchen Screen"

    pos_id = fields.Char(help="Id of the corresponding pos system")

    def get_tickets(self):
        tickets = self.env['kitchen.ticket'].search([])
        res = { "tickets": tickets.read()}
        return res
        
        
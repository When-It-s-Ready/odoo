# -*- coding: utf-8 -*-
from odoo import fields, models


class KitchenDisplay(models.Model):
    _name = "kitchen.display"
    _description ="POS Kitchen Screen"


    # maybe not needed
    pos_id = fields.Char(help="Id of the corresponding pos system")
    active = fields.Boolean(help="Check if display is currently connected", default = "false")

    def get_tickets(self):
        tickets = self.env['kitchen.ticket'].search([])
        res = { "tickets": tickets.read()}
        return res

    def setActive(self):
        self.active = True

    def setInactive(self):
        self.active = False
        
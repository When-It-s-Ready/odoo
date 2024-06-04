# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    ticket_category = fields.Many2many("kitchen.ticket.category", string="Ticket Categories")

    

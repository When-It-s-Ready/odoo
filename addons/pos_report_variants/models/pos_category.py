# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json

class PosCategory(models.Model):
    _inherit = "pos.category"

    toReport = fields.Boolean(string ="Printable in variants report?", default=True)
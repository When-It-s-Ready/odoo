# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PosReportVariants(models.TransientModel):
    _name = 'pos.report.variants.wizard'
    _description = 'POS Report with variants'

    pos_session_id = fields.Many2one('pos.session', required=True)

    def generate_report(self):
        data = {'session_ids': self.pos_session_id.ids}
        return self.env.ref('pos_report_variants.details_report_variants').report_action([], data=data)

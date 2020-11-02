# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    available_in_pos = fields.Boolean(
        string="Available for POS",
        default=False,
    )

    def create_from_ui(self,partner):
        if not partner.get('available_in_pos'):
            partner['available_in_pos'] = True
        return super(ResPartner, self).create_from_ui(partner)

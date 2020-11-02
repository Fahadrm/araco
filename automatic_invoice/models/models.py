# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def auto_pos_order_invoice(self):
        pos_orders = self.env['pos.order'].search([('state', '=', 'paid'),('operating_unit_id','in',self.env.user.operating_unit_ids.ids)], limit=10)

        # pos_orders = self.env['pos.order'].search([('state','=','paid')]).
        for order in pos_orders:
            order.action_pos_order_invoice()
        return
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"
    order_type = fields.Char(string='Order Type')
    update_status = fields.Char(string='Update Status')
    ref_number = fields.Char(string='Ref Number')

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)

        order_fields['partner_id']=ui_order['partner_id']

        partner = order_fields['partner_id']

        if partner:

            if self.env['res.partner'].browse(ui_order['partner_id']).ref:
                order_fields.update({
                    'ref_number': self.env['res.partner'].browse(ui_order['partner_id']).ref,
                    'order_type': 'Opencart',
                    'update_status': 'Pending'
                })
            else:
                order_fields.update({
                    'ref_number': False,
                    'order_type': 'Odoo',
                    'update_status': 'Pending'
                })
        else:
            order_fields.update({
                'ref_number': False,
                'order_type': 'Odoo',
                'update_status': 'Pending'
            })
        return order_fields

    # self.env['connector.product.mapping'].browse('id').ecomm_id

    # @api.model
    # def create_from_ui(self, orders,draft=False):
    #
    #     _logger.info('begin invoice create_from_ui')
    #
    #     order_ids = super(PosOrder, self).create_from_ui(orders,draft)
    #
    #     orders_object = self.browse(order_ids)
    #
    #     for o in orders:
    #         data = o['data']
    #         lines = data.get('lines')
    #         for line_val in lines:
    #             line = line_val[2]
    #             ec_id = self.env['connector.product.mapping'].search([('odoo_id','=',line['product_id'])]).ecomm_id
    #
    #             line['ecommerce_id'] = 2
    #
    #         # if not order.lines:
    #         #     continue

        # _logger.info('end invoice create_from_ui')
        # return order_ids


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    ecommerce_id = fields.Integer(string='Ecommerce ID',compute='opencart_ecomm_id')

    @api.depends('product_id')
    def opencart_ecomm_id(self):
        for i in self:
            if i.product_id:
                ec_id = self.env['connector.product.mapping'].search([('odoo_id','=',i.product_id.id)]).ecomm_id
                i.ecommerce_id = ec_id




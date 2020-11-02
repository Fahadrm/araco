# -*- coding: utf-8 -*-

from odoo import models, fields, api

#
class product_bv(models.Model):
    _inherit = 'product.product'

    bv_value = fields.Float("BV", store=True)

# class product_tempbv(models.Model):
#     _inherit = 'product.template'
#
#     bv_value = fields.Float("BV", store=True)



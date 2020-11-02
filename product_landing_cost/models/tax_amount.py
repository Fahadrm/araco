# -*- coding: utf-8 -*-

from odoo import models, fields, api



class ACcount_tax(models.Model):
    _inherit='account.tax'


    tax_amount = fields.Float(string='Tax Amount', store=True,default=0.00)

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Stock_picking(models.Model):
    _inherit = 'stock.picking'

    sms_state = fields.Selection([('default','Pending'),('completed', 'Completed')],default='default')




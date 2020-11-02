# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class phygireport_delivery_name(models.Model):
#     _name = 'phygireport_delivery_name.phygireport_delivery_name'
#     _description = 'phygireport_delivery_name.phygireport_delivery_name'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

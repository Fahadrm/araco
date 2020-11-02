# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
class smsChangeupdateState(models.TransientModel):
    _name = 'sms.completed.status'
    _description = 'SMS sending'


    sms_state = fields.Selection([
        ('default','Default'),('completed', 'Completed')
    ], string = 'Status')
    def sms_update_state(self):
        active_ids = self._context.get('active_ids', []) or []
        work = self.env['stock.picking'].browse(active_ids)
        # work = self.env['hr.work.entry'].search([('state', '!=', 'validated')])
        for record in work.search([]).browse(active_ids):
            record.sms_state = 'completed'
            # if record.picking_type_code =='outgoing' and record.sms_state=='completed':
            if record.sms_state=='completed':
                record.send_picking_done_message()

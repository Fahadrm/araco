# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Own_productsales(models.TransientModel):
    _name = "commission.report"
    _description = "Commission Report"


    operating_unit= fields.Many2one('operating.unit', string='Branch',required=True,
                                 default=lambda self: self.env.user.default_operating_unit_id)
    company_id = fields.Many2one('res.company',required=True, string='Company',default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date',required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='End Date',required=True, default=fields.Date.context_today)
    own_target_move = fields.Boolean("Own Product",default=False)
    not_own_target_move = fields.Boolean("Not Own Product", default=False)


    def check_report(self):

        self.ensure_one()
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'pos.order'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('commission_report.action_report_commission_report').report_action(self, data=datas)


    def export_xls(self):


        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'pos.order'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('commission_report.action_commission_report_xls').report_action(self, data=datas)

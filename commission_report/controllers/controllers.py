# -*- coding: utf-8 -*-
# from odoo import http


# class CommisionReport(http.Controller):
#     @http.route('/commission_report/commission_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/commission_report/commission_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('commission_report.listing', {
#             'root': '/commission_report/commission_report',
#             'objects': http.request.env['commission_report.commission_report'].search([]),
#         })

#     @http.route('/commission_report/commission_report/objects/<model("commission_report.commission_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('commission_report.object', {
#             'object': obj
#         })

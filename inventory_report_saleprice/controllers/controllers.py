# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryReportSaleprice(http.Controller):
#     @http.route('/inventory_report_saleprice/inventory_report_saleprice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_report_saleprice/inventory_report_saleprice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_report_saleprice.listing', {
#             'root': '/inventory_report_saleprice/inventory_report_saleprice',
#             'objects': http.request.env['inventory_report_saleprice.inventory_report_saleprice'].search([]),
#         })

#     @http.route('/inventory_report_saleprice/inventory_report_saleprice/objects/<model("inventory_report_saleprice.inventory_report_saleprice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_report_saleprice.object', {
#             'object': obj
#         })

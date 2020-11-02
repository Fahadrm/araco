# -*- coding: utf-8 -*-
# from odoo import http


# class PosCustomerList(http.Controller):
#     @http.route('/pos_customer_list/pos_customer_list/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_customer_list/pos_customer_list/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_customer_list.listing', {
#             'root': '/pos_customer_list/pos_customer_list',
#             'objects': http.request.env['pos_customer_list.pos_customer_list'].search([]),
#         })

#     @http.route('/pos_customer_list/pos_customer_list/objects/<model("pos_customer_list.pos_customer_list"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_customer_list.object', {
#             'object': obj
#         })

# -*- coding: utf-8 -*-
# from odoo import http


# class PosCustomerRefSearch(http.Controller):
#     @http.route('/pos_customer_ref_search/pos_customer_ref_search/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_customer_ref_search/pos_customer_ref_search/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_customer_ref_search.listing', {
#             'root': '/pos_customer_ref_search/pos_customer_ref_search',
#             'objects': http.request.env['pos_customer_ref_search.pos_customer_ref_search'].search([]),
#         })

#     @http.route('/pos_customer_ref_search/pos_customer_ref_search/objects/<model("pos_customer_ref_search.pos_customer_ref_search"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_customer_ref_search.object', {
#             'object': obj
#         })

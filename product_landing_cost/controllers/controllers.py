# -*- coding: utf-8 -*-
# from odoo import http


# class ProductLandingCost(http.Controller):
#     @http.route('/product_landing_cost/product_landing_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_landing_cost/product_landing_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_landing_cost.listing', {
#             'root': '/product_landing_cost/product_landing_cost',
#             'objects': http.request.env['product_landing_cost.product_landing_cost'].search([]),
#         })

#     @http.route('/product_landing_cost/product_landing_cost/objects/<model("product_landing_cost.product_landing_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_landing_cost.object', {
#             'object': obj
#         })

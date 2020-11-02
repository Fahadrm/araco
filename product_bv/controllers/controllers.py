# -*- coding: utf-8 -*-
# from odoo import http


# class ProductBv(http.Controller):
#     @http.route('/product_bv/product_bv/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_bv/product_bv/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_bv.listing', {
#             'root': '/product_bv/product_bv',
#             'objects': http.request.env['product_bv.product_bv'].search([]),
#         })

#     @http.route('/product_bv/product_bv/objects/<model("product_bv.product_bv"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_bv.object', {
#             'object': obj
#         })

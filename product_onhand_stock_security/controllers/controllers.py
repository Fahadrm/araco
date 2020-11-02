# -*- coding: utf-8 -*-
# from odoo import http


# class ProductOnhandStockSecurity(http.Controller):
#     @http.route('/product_onhand_stock_security/product_onhand_stock_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_onhand_stock_security/product_onhand_stock_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_onhand_stock_security.listing', {
#             'root': '/product_onhand_stock_security/product_onhand_stock_security',
#             'objects': http.request.env['product_onhand_stock_security.product_onhand_stock_security'].search([]),
#         })

#     @http.route('/product_onhand_stock_security/product_onhand_stock_security/objects/<model("product_onhand_stock_security.product_onhand_stock_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_onhand_stock_security.object', {
#             'object': obj
#         })

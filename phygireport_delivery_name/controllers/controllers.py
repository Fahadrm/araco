# -*- coding: utf-8 -*-
# from odoo import http


# class PhygireportDeliveryName(http.Controller):
#     @http.route('/phygireport_delivery_name/phygireport_delivery_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phygireport_delivery_name/phygireport_delivery_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('phygireport_delivery_name.listing', {
#             'root': '/phygireport_delivery_name/phygireport_delivery_name',
#             'objects': http.request.env['phygireport_delivery_name.phygireport_delivery_name'].search([]),
#         })

#     @http.route('/phygireport_delivery_name/phygireport_delivery_name/objects/<model("phygireport_delivery_name.phygireport_delivery_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phygireport_delivery_name.object', {
#             'object': obj
#         })

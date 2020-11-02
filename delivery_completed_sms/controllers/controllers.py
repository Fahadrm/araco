# -*- coding: utf-8 -*-
# from odoo import http


# class DeliveryCompletedSms(http.Controller):
#     @http.route('/delivery_completed_sms/delivery_completed_sms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_completed_sms/delivery_completed_sms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_completed_sms.listing', {
#             'root': '/delivery_completed_sms/delivery_completed_sms',
#             'objects': http.request.env['delivery_completed_sms.delivery_completed_sms'].search([]),
#         })

#     @http.route('/delivery_completed_sms/delivery_completed_sms/objects/<model("delivery_completed_sms.delivery_completed_sms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_completed_sms.object', {
#             'object': obj
#         })

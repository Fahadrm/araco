# # -*- coding: utf-8 -*-
# from odoo import models, fields, api, _
# from datetime import datetime, timedelta
# import logging
#
# _logger = logging.getLogger(__name__)
#
#
#
# class pos_customer_reference(models.Model):
#     _name = "pos.mlm.orders"
#
#     _description = "Pos Customer Reference"
#
#     customer_id = fields.Many2one('res.partner', string='Customer')
#     order_number = fields.Char('Order No.')
#     ref_number = fields.Char('Ref No.')
#     start_date = fields.Datetime('Order date')
#
#     total_amount = fields.Float('Total amount')
#
#     state = fields.Selection([('waiting','Waiting')])
#
#     pos_order_id = fields.Many2one('pos.order', 'Pos order', readonly=1)
#     pos_order_line_id = fields.Many2one('pos.order.line', 'Pos order line', readonly=1)
#     pos_mlm_line_ids = fields.One2many('pos.mlm.orders.line','pos_mlm_order_id',string="Orders")
#
#     user_id = fields.Many2one('res.users', 'Create user', readonly=1)
#
#     value =fields.Float("Amount Total")
#
#
#     def create_phygi_orders(self, order):
#         today = datetime.today()
#         # end_date = today
#
#         order = self[0]['id']['data']
#         self.create(
#             {
#                 'customer_id': order['partner_id'] if order['partner_id'] else None,
#                 'start_date': fields.Datetime.now(),
#                 'state': 'waiting',
#                 'value': - order['amount_total'],
#                 'order_number': order['name'],
#                 # 'pos_order_id': self[0]['id']['id'],
#                 'user_id': order['user_id'],
#             }
#
#         )
#         return True
#
#     # @api.multi
#     # def get_vouchers_by_order_ids(self, order_ids):
#     #     _logger.info('begin get_vouchers_by_order_ids')
#     #     vouchers_data = []
#     #     product=[]
#     #     discount=0
#     #     subtotal=0
#     #     result=[]
#     #     t=[]
#     #     orders = self.env['pos.order'].sudo().browse(order_ids)
#     #     for order in orders:
#     #         line_ids = [line.id for line in order.lines]
#     #         pos_order_line_ids = self.env['pos.order'].sudo().search(
#     #             [('company_id', '=', self.env.user.company_id.id),
#     #              ('state', 'not in', ['cancel'])], limit=10)
#     #         vouchers = self.sudo().search([('pos_order_line_id', 'in', line_ids)])
#     #         for voucher in vouchers:
#     #             vouchers_data.append({
#     #                 'number': voucher.number,
#     #                 'code': voucher.code,
#     #                 'partner_name': voucher.customer_id.name if voucher.customer_id else '',
#     #                 'method': voucher.method,
#     #                 'apply_type': voucher.apply_type,
#     #                 'value': voucher.value,
#     #                 'start_date': voucher.end_date,
#     #                 'end_date': voucher.end_date,
#     #                 'id': voucher.id,
#     #                 'pos_order_id': voucher.pos_order_id.id,
#     #                 'pos_order_line_id':"",
#     #                 'user_name':voucher.user_id.name if voucher.user_id else '',
#     #             })
#     #         if order.create_voucher:
#     #             vouchers = self.sudo().search([('pos_order_id', '=', order.id)])
#     #             for voucher in vouchers:
#     #                 s={
#     #                     'number': voucher.number,
#     #                     'code': voucher.code,
#     #                     'partner_name': voucher.customer_id.name if voucher.customer_id else '',
#     #                     'method': voucher.method,
#     #                     'apply_type': voucher.apply_type,
#     #                     'value': voucher.value,
#     #                     'start_date': voucher.end_date,
#     #                     'end_date': voucher.end_date,
#     #                     'id': voucher.id,
#     #                     'pos_order_id': voucher.pos_order_id.id,
#     #                     'pos_order_line_id':"",
#     #                     'user_name': voucher.user_id.name if voucher.user_id else '',
#     #                 }
#     #                 # vouchers_data.append({
#     #                 #     'number': voucher.number,
#     #                 #     'code': voucher.code,
#     #                 #     'partner_name': voucher.customer_id.name if voucher.customer_id else '',
#     #                 #     'method': voucher.method,
#     #                 #     'apply_type': voucher.apply_type,
#     #                 #     'value': voucher.value,
#     #                 #     'start_date': voucher.end_date,
#     #                 #     'end_date': voucher.end_date,
#     #                 #     'id': voucher.id,
#     #                 # })
#     #                 for line in voucher.pos_order_id.lines:
#     #                     tax_name = self.env["account.tax"].browse(line.tax_ids.ids).name if line.tax_ids else "None"
#     #
#     #                     new_vals = {
#     #                         'product_id': line.product_id.name,
#     #                         'product_mrp': line.product_mrp,
#     #                         'unit': line.product_id.uom_id.name,
#     #                         'qty': line.qty*-1,
#     #                         'price_unit': '%.2f' % line.price_unit,
#     #                         'tax_name': tax_name,
#     #                         'discount': '%.2f' % line.discount,
#     #                         'price_subtotal': line.price_subtotal*-1,
#     #                         'tax': (line.price_subtotal_incl - line.price_subtotal)*-1 if line.price_subtotal_incl != 0 else 0,
#     #                         'price_subtotal_incl': line.price_subtotal_incl*-1,
#     #                         'tax_ids': line.tax_ids.ids if line.tax_ids else False,
#     #                     }
#     #                     discount += (line.price_unit * line.qty *-1* line.discount) / 100
#     #                     subtotal += (line.price_subtotal_incl*-1)
#     #                     v1=(0,0,new_vals)
#     #                     t.append(v1)
#     #                     result.append(new_vals)
#     #                 s.update({'pos_order_line_id':result})
#     #                     # hrp_re = (0, 0, new_vals)
#     #                     # result.append(hrp_re)
#     #             vouchers_data.append(s)
#     #     return vouchers_data
#     #
#     #
#     #
#     #
#     # @api.model
#     # def get_voucher_by_code(self, code):
#     #     s = []
#     #
#     #     # pos_vouchers = self.env['pos.order'].search([])
#     #
#     #     vouchers = self.env['pos.voucher'].search(
#     #         # ['|', ('code', '=', code), ('number', '=', code), ('state', '=', 'active')])
#     #     ['|', ('code', '=', code), ('number', '=', code), ('end_date', '>=', fields.Datetime.now()), ('state', '=', 'active')])
#     #
#     #
#     #
#     #     if not vouchers:
#     #         return -1
#     #     else:
#     #         for voucher in vouchers:
#     #             pos_order = self.env['pos.order'].search([('voucher_id', '=', voucher.id)])
#     #             s.append(pos_order.voucher_id.number)
#     #         if code in s:
#     #             return ""
#     #         else:
#     #             return vouchers.read([])[0]
#     #     # for i in pos_vouchers:
#     #     #     s.append(i.voucher_id.number)
#     #     # if code in s:
#     #     #     return ""
#     #     # # elif code not in s:
#     #     # #     return code
#     #     #
#     #     #     # ['|', ('code', '=', code), ('number', '=', code), ('end_date', '>=', fields.Datetime.now()), ('state', '=', 'active')])
#     #     # elif not vouchers:
#     #     #     return -1
#     #     # else:
#     #     #     return vouchers.read([])[0]
#     #
#     # @api.model
#     # def get_last_voucher(self, ref):
#     #     vouchers_data = []
#     #     discount = 0
#     #     subtotal = 0
#     #     result = []
#     #     t = []
#     #     s={}
#     #     if ref == None or ref == u'':
#     #         vouchers = self.search([('state', 'in', ['active'])], limit=1,order='id desc')
#     #
#     #     else:
#     #         vouchers = self.search([('state', 'in', ['active']),('pos_order_id.session_id','=',ref)], limit=1, order='id desc')
#     #
#     #
#     #     if vouchers:
#     #         for voucher in vouchers:
#     #             s = {js_create_voucher
#     #                 'number': voucher.number,
#     #                 'code': voucher.code,
#     #                 'partner_name': voucher.customer_id.name if voucher.customer_id else '',
#     #                 'method': voucher.method,
#     #                 'apply_type': voucher.apply_type,
#     #                 'value': voucher.value,
#     #                 'start_date': voucher.end_date,
#     #                 'end_date': voucher.end_date,
#     #                 'id': voucher.id,
#     #                 'pos_order_id': voucher.pos_order_id.id,
#     #                 'pos_order_line_id': "",
#     #                 'user_name': voucher.user_id.name if voucher.user_id else '',
#     #             }
#     #
#     #             for line in voucher.pos_order_id.lines:
#     #                 tax_name = self.env["account.tax"].browse(line.tax_ids.ids).name if line.tax_ids else "None"
#     #
#     #                 new_vals = {
#     #                     'product_id': line.product_id.name,
#     #                     'product_mrp': line.product_mrp,
#     #                     'unit': line.product_id.uom_id.name,
#     #                     'qty': line.qty*-1,
#     #                     'price_unit': '%.2f' % line.price_unit,
#     #                     'tax_name': tax_name,
#     #                     'discount': '%.2f' % line.discount,
#     #                     'price_subtotal': line.price_subtotal*-1,
#     #                     'tax': (line.price_subtotal_incl - line.price_subtotal)*-1 if line.price_subtotal_incl != 0 else 0,
#     #                     'price_subtotal_incl': line.price_subtotal_incl*-1,
#     #                     'tax_ids': line.tax_ids.ids if line.tax_ids else False,
#     #                 }
#     #                 discount += (line.price_unit * line.qty *-1* line.discount) / 100
#     #                 subtotal += (line.price_subtotal_incl*-1)
#     #                 v1 = (0, 0, new_vals)
#     #                 t.append(v1)
#     #                 result.append(new_vals)
#     #             s.update({'pos_order_line_id': result})
#     #
#     #         vouchers_data.append(s)
#     #     return vouchers_data
#
#
# class pos_mlm_orders_line_reference(models.Model):
#     _name = "pos.mlm.orders.line"
#
#     product_id = fields.Many2one('product.product', string="Product", store=True)
#
#     product_subtotal = fields.Float('Subtotal', store=True)
#     product_qty = fields.Float('Qty', store=True)
#     pos_mlm_order_id = fields.Many2one('pos.mlm.orders', string='Pos mlm order', store=True)
#

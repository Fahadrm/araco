# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MassConfirmPicking(models.TransientModel):
    _name = 'mass.confirm.picking'
    _description = 'Mass Confirm Picking'

    message = fields.Text(string='Message', readonly=True)
    compute_message = fields.Text(string='Message', readonly=True)
    picking_validate_process = fields.Selection([('full','Fully Available'),('partial','Partial Available'),('force','Force Available')],default='full',string='Picking Available',required=True)
    backorder = fields.Boolean(string='Is Backorder ?')

    @api.model
    def default_get(self, fields):
        res = super(MassConfirmPicking, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        sale_orders = self.env['sale.order'].browse(active_ids)
        order_list = []
        draft_orders = []
        for order in sale_orders:
            if order.state in ['sale']:
                order_list.append(order.name)
            elif order.state not in ['sale']:
                draft_orders.append(order.name)
        msg = ','.join(order_list)
        message = ','.join(draft_orders)
        res.update({
            'message': "Validate The Following Sale Orders" + " " + msg,
            })
        if len(draft_orders) > 0:
            res.update({
                'compute_message': "Following Orders are not Confirmed" + " " + message
                })
        return res

    def action_confirm_picking(self):
        if self.env.context.get('active_ids', False):
            done_picking = []
            not_done_picking = []
            msg = ""
            message = ""
            backorder_message = ""
            backorder = []
            if self.picking_validate_process == 'full':
                for order in self.env['sale.order'].search([('id', 'in', self.env.context.get('active_ids', False))]):
                    if order.state in ['sale']:
                        if order.picking_ids:
                            for picking in order.picking_ids:
                                if picking.state in ['done']:
                                    not_done_picking.append(picking.name)
                                else:
                                    is_partial = False
                                    for check_move in picking.move_ids_without_package:
                                        if check_move.state in ['partially_available']:
                                            is_partial = True
                                    if is_partial == True:
                                        not_done_picking.append(picking.name)
                                    else:
                                        done_picking.append(picking.name)
                                        if picking.state in ['draft']:
                                            picking.action_confirm()
                                        if picking.state in ['confirmed']:
                                            picking.action_assign()
                                        if picking.state in ['assigned']:
                                            picking.button_validate()
                                        wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                                        wiz.process()
            elif self.picking_validate_process == 'partial':
                for order in self.env['sale.order'].search([('id', 'in', self.env.context.get('active_ids', False))]):
                    if order.state in ['sale']:
                        if order.picking_ids:
                            for picking in order.picking_ids:
                                if picking.state in ['done']:
                                    not_done_picking.append(picking.name)
                                else:
                                    if self.backorder == True:
                                        is_partial = False
                                        for move in picking.move_ids_without_package:
                                            if move.state in ['partially_available']:
                                                is_partial = True
                                        if is_partial == True:
                                            if picking.state in ['draft']:
                                                picking.action_confirm()
                                            if picking.state in ['confirmed']:
                                                picking.action_assign()
                                            if picking.state in ['assigned']:
                                                picking.button_validate()
                                            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                                            wiz.process()
                                            wizard = self.env['stock.backorder.confirmation'].create({'pick_ids': [(4, picking.id)]})
                                            wizard.process()
                                            done_picking.append(picking.name)
                                            backorder_id = self.env['stock.picking'].sudo().search([('backorder_id','=',picking.id)],limit=1)
                                            if backorder_id:
                                                backorder.append(backorder_id.name)
                                        else:
                                            if picking.state in ['draft']:
                                                picking.action_confirm()
                                            if picking.state in ['confirmed']:
                                                picking.action_assign()
                                            if picking.state in ['assigned']:
                                                picking.button_validate()
                                            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                                            wiz.process()
                                    else:
                                        is_partial = False
                                        for move in picking.move_ids_without_package:
                                            if move.state in ['partially_available']:
                                                is_partial = True
                                        if is_partial == True:
                                            if picking.state in ['draft']:
                                                picking.action_confirm()
                                            if picking.state in ['confirmed']:
                                                picking.action_assign()
                                            if picking.state in ['assigned']:
                                                picking.button_validate()
                                            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                                            wiz.process()
                                            wizard = self.env['stock.backorder.confirmation'].create({'pick_ids': [(4, picking.id)]})
                                            wizard.process_cancel_backorder()
                                            done_picking.append(picking.name)
                                        else:
                                            if picking.state in ['draft']:
                                                picking.action_confirm()
                                            if picking.state in ['confirmed']:
                                                picking.action_assign()
                                            if picking.state in ['assigned']:
                                                picking.button_validate()
                                            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                                            wiz.process()
            elif self.picking_validate_process == 'force':
                for order in self.env['sale.order'].search([('id', 'in', self.env.context.get('active_ids', False))]):
                    if order.state in ['sale']:
                        if order.picking_ids:
                            for picking in order.picking_ids:
                                if picking.state in ['done']:
                                    not_done_picking.append(picking.name)
                                else:
                                    for move in picking.move_ids_without_package:
                                        move.sudo().write({
                                            'quantity_done':move.product_uom_qty
                                            })
                                    picking.button_validate()
                                    wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                                    wiz.process()
                                    done_picking.append(picking.name)
            
            if len(done_picking) > 0:
                msg = "Following Picking Validated Successfully" + " " + ','.join(done_picking)
            if len(not_done_picking) > 0:
                message = "There is some issue to validate following Picking" + " " + ','.join(not_done_picking)
            if len(backorder)>0:
                backorder_message = "Backorders :" + " " + ','.join(backorder)
            return {
                'name': _('Picking Validate Success'),
                'type': 'ir.actions.act_window',
                'res_model': 'picking.warning.message',
                'view_type': 'form',
                'view_mode': 'form',
                'context': {'default_message': msg, 'default_compute_message': message,'default_backorder_message':backorder_message},
                'target': 'new'
            }

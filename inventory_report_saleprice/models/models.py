# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_is_zero



class StockQuant(models.Model):
    _inherit = 'stock.quant'

    sale_value = fields.Monetary('Sale Value', compute='_compute_sale_value', groups='stock.group_stock_manager')

    @api.depends('company_id', 'location_id', 'owner_id', 'product_id', 'quantity')
    def _compute_sale_value(self):
        """ For standard and AVCO valuation, compute the current accounting
        valuation of the quants by multiplying the quantity by
        the standard price. Instead for FIFO, use the quantity times the
        average cost (valuation layers are not manage by location so the
        average cost is the same for all location and the valuation field is
        a estimation more than a real value).
        """
        for quant in self:
            # If the user didn't enter a location yet while enconding a quant.
            if not quant.location_id:
                quant.sale_value = 0
                return

            if not quant.location_id._should_be_valued() or\
                    (quant.owner_id and quant.owner_id != quant.company_id.partner_id):
                quant.sale_value = 0
                continue
            # if quant.product_id.cost_method == 'fifo':
            #     quantity = quant.product_id.quantity_svl
            #     if float_is_zero(quantity, precision_rounding=quant.product_id.uom_id.rounding):
            #         quant.value = 0.0
            #         continue
            #     average_cost = quant.product_id.value_svl / quantity
            #     quant.value = quant.quantity * average_cost
            # else:
            quant.sale_value = quant.quantity * quant.product_id.list_price


    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ This override is done in order for the grouped list view to display the total value of
        the quants inside a location. This doesn't work out of the box because `value` is a computed
        field.
        """
        if 'sale_value' not in fields:
            return super(StockQuant, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        res = super(StockQuant, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        for group in res:
            if group.get('__domain'):
                quants = self.search(group['__domain'])
                group['sale_value'] = sum(quant.sale_value for quant in quants)
        return res

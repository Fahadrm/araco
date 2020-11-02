# -*- coding: utf-8 -*-

from odoo import models, fields, api



class onproduct_checking(models.Model):
    _inherit='product.template'


    landing_cost = fields.Float(string="Landing Cost",compute='get_landing_cost_value',store = True)

    @api.depends('standard_price', 'taxes_id','taxes_id.tax_amount')
    def get_landing_cost_value(self):
        for i in self:
            currency = i.currency_id or None
            prec = currency.decimal_places
            price = i.standard_price
            q = 1
            unit_taxes = False
            taxes = False
            total_cost = 0
            if i.taxes_id:
                unit_taxes = i.taxes_id.compute_all(price)
                for j in i.taxes_id:
                    total_cost += i.standard_price*j.tax_amount/100


            i.landing_cost = i.standard_price + total_cost if unit_taxes else price

            # i.landing_cost = i.standard_price + (i.standard_price*i.taxes_id.tax_amount/100) if unit_taxes else price

            # i.landing_cost = i.standard_price + (unit_taxes['total_included']-unit_taxes['total_excluded']) if unit_taxes else price
            if i.taxes_id:
                i.landing_cost = i.currency_id.round(i.landing_cost)
            else:
                i.landing_cost = i.currency_id.round(i.standard_price)

            # line.landing_cost = line.uom_id._compute_price(landing_cost, line.uom_id)


    # @api.depends('standard_price', 'taxes_id')
    # def _compute_price_tax(self):
    #     for i in self:
    #         currency = i.currency_id or None
    #         prec = currency.decimal_places
    #         price = i.standard_price
    #         q = 1
    #         unit_taxes = False
    #         taxes = False
    #         if i.taxes_id:
    #
    #                 unit_taxes = i.taxes_id.compute_all(price)
    #         i.landing_cost = unit_taxes['total_included'] if unit_taxes else price
    #         if i.taxes_id:
    #             i.landing_cost = i.currency_id.round(i.landing_cost)
    #
    #     return


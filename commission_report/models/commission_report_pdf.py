# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime
from datetime import datetime


class commsionPDF(models.AbstractModel):
    _name = 'report.commission_report.report_commission_report'

    def get_sale(self, data):

        lines = []

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        operating_unit = data['form']['operating_unit']
        company_id = data['form']['company_id']
        own_target_move = data['form']['own_target_move']
        not_own_target_move = data['form']['not_own_target_move']

        sl = 0
        if own_target_move == False and not_own_target_move == True:

            query = '''


    SELECT 
    product_template.name as product,
    sum(account_move_line.quantity) as qty,
    account_move_line.price_unit as price_unit,
    product_product.id as product_id,
                sum((((account_move_line.price_unit-product_template.landing_cost)*account_move_line.quantity)*56)/100)  as phygi_store

    			FROM 
                    public.account_move_line
                    left join public.account_move   on (account_move.id = account_move_line.move_id)
                left join public.product_product   on (account_move_line.product_id = product_product.id)
                    left join public.product_template   on (product_template.id = product_product.product_tmpl_id)

                    where product_template.own_product=false and
                    account_move.state in ('posted') and account_move.type = 'out_invoice'
                    and exclude_from_invoice_tab = false
                    AND to_char(date_trunc('day',account_move.invoice_date),'YYYY-MM-DD')::date between %s and %s
                    AND account_move.company_id= %s
    				AND account_move.operating_unit_id= %s
                    group by 
                    account_move_line.price_unit,product_template.id,product_product.id order by product

                           '''

            self.env.cr.execute(query, (
                date_from, date_to, company_id, operating_unit
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                if row['product']:
                    product_name = row['product'] if row['product'] else " "
                else:
                    product_name = row['product'] if row['product'] else " "
                if row['price_unit']:
                    list_price = row['price_unit'] if row['price_unit'] else 0.0
                else:
                    list_price = row['price_unit'] if row['price_unit'] else 0.0
                if row['qty']:
                    qty = row['qty'] if row['qty'] else 0.0
                else:
                    qty = row['qty'] if row['qty'] else 0.
                if row['product_id']:
                    product_id = row['product_id'] if row['product_id'] else " "
                else:
                    product_id = row['product_id'] if row['product_id'] else " "
                if row['phygi_store']:
                    phygi_store_commission = row['phygi_store'] if row['phygi_store'] else 0
                else:
                    phygi_store_commission = row['phygi_store'] if row['phygi_store'] else 0


                res = {
                    'sl_no': sl,
                    'product_name': product_name if product_name else " ",
                    'list_price': list_price if list_price else 0.0,
                    'qty': qty if qty else 0.0,
                    'phygi_store_commission': round(phygi_store_commission,2) if phygi_store_commission else 0.0

                }

                lines.append(res)
            if lines:
                return lines
            else:
                return []
        elif own_target_move == True and not_own_target_move ==False :

            query = '''

    SELECT 
    product_template.name as product,
    sum(account_move_line.quantity) as qty,
    account_move_line.price_unit as price_unit,
    product_product.id as product_id,
    round(sum((account_move_line.quantity*account_move_line.price_unit*3)/100),2) as phygi_store

    			FROM 
                    public.account_move_line
                    left join public.account_move   on (account_move.id = account_move_line.move_id)
                left join public.product_product   on (account_move_line.product_id = product_product.id)
                    left join public.product_template   on (product_template.id = product_product.product_tmpl_id)

                    where product_template.own_product=true and
                    account_move.state in ('posted') and account_move.type = 'out_invoice'
                    and exclude_from_invoice_tab = false
                    AND to_char(date_trunc('day',account_move.invoice_date),'YYYY-MM-DD')::date between %s and %s
                    AND account_move.company_id= %s
    				AND account_move.operating_unit_id= %s
                    group by 
                    account_move_line.price_unit,product_template.id,product_product.id order by product

                                                               '''

            self.env.cr.execute(query, (
                date_from, date_to, company_id, operating_unit
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                if row['product']:
                    product_name = row['product'] if row['product'] else " "
                else:
                    product_name = row['product'] if row['product'] else " "
                if row['price_unit']:
                    list_price = row['price_unit'] if row['price_unit'] else 0.0
                else:
                    list_price = row['price_unit'] if row['price_unit'] else 0.0
                if row['qty']:
                    qty = row['qty'] if row['qty'] else 0.0
                else:
                    qty = row['qty'] if row['qty'] else 0.
                if row['product_id']:
                    product_id = row['product_id'] if row['product_id'] else " "
                else:
                    product_id = row['product_id'] if row['product_id'] else " "

                if row['phygi_store']:
                    phygi_store = row['phygi_store'] if row['phygi_store'] else 0
                else:
                    phygi_store = row['phygi_store'] if row['phygi_store'] else 0

                res = {
                    'sl_no': sl,
                    'product_name': product_name if product_name else " ",
                    'list_price': list_price if list_price else 0.0,
                    'qty': qty if qty else 0.0,
                    'phygi_store_commission': phygi_store if phygi_store else 0.0,

                }

                lines.append(res)

            if lines:
                return lines
            else:
                return []

        elif own_target_move == False and not_own_target_move == False or own_target_move == True and not_own_target_move == True:

            query = '''
 SELECT 
    product_template.name as product,
    sum(account_move_line.quantity) as qty,
    account_move_line.price_unit as price_unit,
    product_product.id as product_id,
     (case
                   when product_template.own_product=true
                  then  round(sum((account_move_line.quantity*account_move_line.price_unit*3)/100),2)
                 else sum((((account_move_line.price_unit-product_template.landing_cost)*account_move_line.quantity)*56)/100) end ) as phygi_store
               


    			FROM 
                    public.account_move_line
                    left join public.account_move   on (account_move.id = account_move_line.move_id)
                left join public.product_product   on (account_move_line.product_id = product_product.id)
                    left join public.product_template   on (product_template.id = product_product.product_tmpl_id)

                    where 
                    account_move.state in ('posted') and account_move.type = 'out_invoice'  
                    and exclude_from_invoice_tab = false
                    AND to_char(date_trunc('day',account_move.invoice_date),'YYYY-MM-DD')::date between %s and %s
                    AND account_move.company_id= %s
    				AND account_move.operating_unit_id= %s
                    group by 
                    account_move_line.price_unit,product_template.id,product_product.id order by product
                                                               '''

            self.env.cr.execute(query, (
                date_from, date_to, company_id,operating_unit
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                if row['product']:
                    product_name = row['product'] if row['product'] else " "
                else:
                    product_name = row['product'] if row['product'] else " "
                if row['price_unit']:
                    list_price = row['price_unit'] if row['price_unit'] else 0.0
                else:
                    list_price = row['price_unit'] if row['price_unit'] else 0.0
                if row['qty']:
                    qty = row['qty'] if row['qty'] else 0.0
                else:
                    qty = row['qty'] if row['qty'] else 0.
                if row['product_id']:
                    product_id = row['product_id'] if row['product_id'] else " "
                else:
                    product_id = row['product_id'] if row['product_id'] else " "


                if row['phygi_store']:
                    phygi_store_commission = row['phygi_store'] if row['phygi_store'] else 0
                else:
                    phygi_store_commission = row['phygi_store'] if row['phygi_store'] else 0



                res = {
                    'sl_no': sl,
                    'product_name': product_name if product_name else " ",
                    'list_price': list_price if list_price else 0.0,
                    'qty': qty if qty else 0.0,
                    'phygi_store_commission': round(phygi_store_commission,2) if phygi_store_commission else 0.0

                }

                lines.append(res)

            if lines:
                return lines
            else:
                return []

    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        operating_unit = data['form']['operating_unit']
        company_id = data['form']['company_id']
        own_target_move = data['form']['own_target_move']
        not_own_target_move = data['form']['not_own_target_move']

        operating_unit_name = self.env['operating.unit'].browse(operating_unit).name

        company_name = self.env['res.company'].browse(company_id).name
        company_logo = self.env['res.company'].browse(company_id).logo
        company_street = self.env['res.company'].browse(company_id).street
        company_street2 = self.env['res.company'].browse(company_id).street2
        company_city = self.env['res.company'].browse(company_id).city
        company_country = self.env['res.company'].browse(company_id).country_id.name
        company_email = self.env['res.company'].browse(company_id).email
        company_state = self.env['res.company'].browse(company_id).state_id.name



        get_sale = self.get_sale(data)

        date_object_startdate = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_object_enddate = datetime.strptime(date_to, '%Y-%m-%d').date()

        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'date_start': date_object_startdate.strftime('%d-%m-%Y'),
            'date_end': date_object_enddate.strftime('%d-%m-%Y'),
            'docs': docs,
            'time': time,
            'get_sale': get_sale,
            'own_target_move':own_target_move,
            'not_own_target_move': not_own_target_move,
            'operating_unit':operating_unit_name,

           'company_name' :company_name ,
        'company_logo':company_logo,
        'company_street': company_street ,
        'company_street2':company_street2 ,
        'company_city':company_city ,
        'company_country':company_country ,
        'company_email':company_email,
            'company_state': company_state,
        }
        return docargs

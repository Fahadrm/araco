import datetime
from odoo.exceptions import UserError
from datetime import datetime, date
import time
from odoo import api, models, _
from odoo.exceptions import UserError
from xlsxwriter.utility import xl_range, xl_rowcol_to_cell
from collections import defaultdict



class commissionXls(models.AbstractModel):
    _name = 'report.commission_report.action_commission_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_sale(self, data):

        lines = []

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        operating_unit = data['form']['operating_unit']
        company_id = data['form']['company_id']
        own_target_move = data['form']['own_target_move']
        not_own_target_move = data['form']['not_own_target_move']

        sl = 0
        if own_target_move==False and not_own_target_move == True:


            query = '''

             
SELECT 
product_template.name as product,
sum(account_move_line.quantity) as qty,
account_move_line.price_unit as price_unit,
product_product.id as product_id,
            sum((((account_move_line.price_unit-product_template.landing_cost)*account_move_line.quantity)*56)/100)  as phygi_store

 
			FROM 
                public.account_move_line
                left join public.account_move  on (account_move.id = account_move_line.move_id)
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
                date_from, date_to, company_id,operating_unit
            ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                product_name = row['product'] if row['product'] else " "
                list_price = row['price_unit'] if row['price_unit'] else 0.0
                qty = row['qty'] if row['qty'] else 0.0

                product_id = row['product_id'] if row['product_id'] else 0


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
        elif own_target_move== True and not_own_target_move ==False:


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
                    date_from, date_to,company_id, operating_unit
                ))
            for row in self.env.cr.dictfetchall():
                sl += 1

                product_name = row['product'] if row['product'] else " "
                list_price = row['price_unit'] if row['price_unit'] else 0.0
                qty = row['qty'] if row['qty'] else 0.0

                product_id = row['product_id'] if row['product_id'] else 0
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

        elif own_target_move==False and not_own_target_move == False or own_target_move==True and not_own_target_move == True:

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
                               and exclude_from_invoice_tab =false
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

                product_name = row['product'] if row['product'] else " "
                list_price = row['price_unit'] if row['price_unit'] else 0.0
                qty = row['qty'] if row['qty'] else 0.0

                product_id = row['product_id'] if row['product_id'] else 0
                phygi_store_commission = row['phygi_store'] if row['phygi_store'] else 0

                res = {
                    'sl_no': sl,
                    'product_name': product_name if product_name else " ",
                    'list_price': list_price if list_price else 0.0,
                    'qty': qty if qty else 0.0,
                    # 'tax': tax if tax else 0.0,
                    'phygi_store_commission': round(phygi_store_commission,2) if phygi_store_commission else 0.0

                }

                lines.append(res)

            if lines:
                return lines
            else:
                return []
    def generate_xlsx_report(self, workbook, data, lines):

        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        sheet = workbook.add_worksheet(_('Commission Report'))
        sheet.set_landscape()
        sheet.set_default_row(25)
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        # sheet.set_column(0, 0, 14)
        # sheet.set_column(1, 1, 45)
        # sheet.set_column(2, 2, 22)
        # sheet.set_column(3, 5, 18)
        # sheet.set_column(4, 5, 20)


        # sheet.set_column(1, 1, 20)
        # sheet.set_column(2, 2, 25)
        # sheet.set_column(3, 3, 25)
        # sheet.set_column(4, 4, 20)
        # sheet.set_column(5, 5, 25)
        # sheet.set_column(6, 6, 20)
        # sheet.set_column(7, 7, 20)
        # sheet.set_column(8, 8, 20)
        # sheet.set_column(9, 9, 20)
        # sheet.set_column(10, 10, 20)
        # sheet.set_column(11, 11, 20)
        # sheet.set_column(12, 12, 20)
        # sheet.set_column(13, 13, 20)
        # sheet.set_column(14, 14, 20)
        # sheet.set_column(15, 15, 20)
        # sheet.set_column(16, 16, 20)
        # sheet.set_column(17, 17, 20)
        # sheet.set_column(18, 18, 20)
        # sheet.set_column(19, 19, 20)
        # sheet.set_column(20, 20, 20)
        # sheet.set_column(21, 21, 30)
        # sheet.set_column(22, 22, 20)
        # sheet.set_column(23, 23, 20)
        # sheet.set_column(24, 24, 20)

        company = self.env['res.company'].browse(data['form']['company_id'])

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        operating_unit = data['form']['operating_unit']
        company_id = data['form']['company_id']
        own_target_move = data['form']['own_target_move']
        not_own_target_move = data['form']['not_own_target_move']
        if company.street:
            res = company.street
        else:
            res=""
        if company.street2:
            res2 = company.street2
        else:
            res2 = ""


        date_start = data['form']['date_from']
        date_end = data['form']['date_to']
        if date_start:

            date_object_date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
        if date_end:
            date_object_date_end = datetime.strptime(date_end, '%Y-%m-%d').date()


        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14})
        font_size_8_center = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'center'})
        font_size_8_right = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'right'})
        font_size_8_left = workbook.add_format(
            {'bottom': True, 'top': True, 'left': True, 'font_size': 14, 'align': 'left'})

        formattotal = workbook.add_format(
            {'bg_color': 'e2e8e8', 'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
             'align': 'right', 'bold': True})


        blue_mark2 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True,
             'color': 'ffffff', 'bg_color': '7b0b5b', 'align': 'center'})
        font_size_8blod = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 14, 'bold': True, })

        blue_mark3 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 18, 'bold': True,
             'color': 'ffffff', 'bg_color': '7b0b5b', 'align': 'center'})

        title_style = workbook.add_format({'font_size': 14, 'bold': True,
                                           'bg_color': '000000', 'color': 'ffffff',
                                           'bottom': 1, 'align': 'center'})
        account_style = workbook.add_format({'font_size': 14, 'bold': True,
                                           'bg_color': '929393', 'color': 'ffffff',
                                           'bottom': 1, 'align': 'left'})


        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 35)
        sheet.set_column(3, 3, 25)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 25)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)
        sheet.set_column(8, 8, 20)
        sheet.set_column(9, 9, 20)
        sheet.set_column(10, 10, 20)
        sheet.set_column(11, 11, 20)
        sheet.set_column(12, 12, 20)
        sheet.set_column(13, 13, 20)
        sheet.set_column(14, 14, 20)
        sheet.set_column(15, 15, 20)
        sheet.set_column(16, 16, 20)
        sheet.set_column(17, 17, 20)
        sheet.set_column(18, 18, 20)
        sheet.set_column(19, 19, 20)
        sheet.set_column(20, 20, 20)
        sheet.set_column(21, 21, 30)
        sheet.set_column(22, 22, 20)
        sheet.set_column(23, 23, 20)
        sheet.set_column(24, 24, 20)

        sheet.merge_range('A1:E1', company.name, blue_mark3)
        sheet.merge_range('A2:E2', res + " ," + res2, blue_mark2)
        sheet.merge_range('A3:E3', "Commission Report", blue_mark2)

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        if date_start and date_end:

            sheet.merge_range('A5:E5',
                              "Date : " + date_object_date_start.strftime('%d-%m-%Y') + " to " + date_object_date_end.strftime(
                                  '%d-%m-%Y'), font_size_8blod)
        elif date_start:
            sheet.merge_range('A5:E5', "Date : " + date_object_date_start.strftime('%d-%m-%Y'),
                              font_size_8blod)

        sheet.write('A6', "Sl No.", title_style)
        sheet.write('B6', "Product Name", title_style)
        sheet.write('C6', "Sale Qty", title_style)
        sheet.write('D6', "Selling Price", title_style)
        sheet.write('E6', "Phygi store Commission", title_style)

        linw_row = 6
        line_column = 0

        for line in self.get_sale(data):
            sheet.write(linw_row, line_column, line['sl_no'], font_size_8_center)
            sheet.write(linw_row, line_column + 1, line['product_name'], font_size_8_left)
            sheet.write(linw_row, line_column + 2, '{0:,.2f}'.format(float(line['qty'])), font_size_8_center)

            sheet.write(linw_row, line_column + 3, line['list_price'], font_size_8_center)
            sheet.write(linw_row, line_column + 4, '{0:,.2f}'.format(float(line['phygi_store_commission'])), font_size_8_center)
            # sheet.write(linw_row, line_column + 5, '{0:,.2f}'.format(float(line['tax'])), font_size_8_center)

            # sheet.write(linw_row, line_column + 6, '{0:,.2f}'.format(float(line['untax_amount'])), font_size_8_center)
            # sheet.write(linw_row, line_column + 7, '{0:,.2f}'.format(float(line['total_amount'])), font_size_8_center)

            linw_row = linw_row + 1
            line_column = 0

        line_column = 0

        sheet.merge_range(linw_row, 0, linw_row, 1, "TOTAL", font_size_8_left)

        total_cell_range12 = xl_range(8, 2, linw_row - 1, 2)

        total_cell_range11 = xl_range(8, 3, linw_row - 1, 3)
        total_cell_range = xl_range(8, 4, linw_row - 1, 4)

        sheet.write_formula(linw_row, 2, '=SUM(' + total_cell_range12 + ')', font_size_8_center)
        sheet.write_formula(linw_row, 3, '=SUM(' + total_cell_range11 + ')', font_size_8_center)
        sheet.write_formula(linw_row, 4, '=SUM(' + total_cell_range + ')', font_size_8_center)


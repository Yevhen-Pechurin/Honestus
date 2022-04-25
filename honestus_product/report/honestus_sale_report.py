# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class HonestusSaleReport(models.Model):
    _name = "honestus.sale.report"
    _description = "Honestus Sales Analysis Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    name = fields.Char('Order Reference', readonly=True)
    product_code = fields.Char()
    honestus_code = fields.Char()
    unit_price = fields.Float()
    honestus_price = fields.Float()
    margin = fields.Float(digits=(10, 2))
    date = fields.Datetime('Order Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product Variant', readonly=True)
    order_id = fields.Many2one('sale.order', 'Order #', readonly=True)

    def _select_sale(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            coalesce(l.id, -s.id) as id,
            l.product_id as product_id,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.partner_id as partner_id,
            s.id as order_id,
            (CASE WHEN p.honestus_price != 0.0 
                THEN p.honestus_price 
                ELSE l.price_unit END - ip.value_float) / 
                CASE WHEN p.honestus_price != 0.0 
                THEN p.honestus_price 
                ELSE l.price_unit END as margin,
            p.default_code as product_code,
            p.honestus_code as honestus_code,
            l.price_unit as unit_price,
            p.honestus_price as honestus_price
        """

        for field in fields.values():
            select_ += field
        return select_

    def _from_sale(self, from_clause=''):
        from_ = """
                sale_order_line l
                    right outer join sale_order s on (s.id=l.order_id)
                    join res_partner partner on s.partner_id = partner.id
                    left join product_product p on (l.product_id=p.id)
                    left join product_template t on (p.product_tmpl_id=t.id)
                    JOIN ir_property ip ON ip.res_id = CONCAT('product.product,', p.id) AND ip.name = 'standard_price'
                %s
        """ % from_clause
        return from_

    def _query(self, with_clause='', fields=None, groupby='', from_clause=''):
        if not fields:
            fields = {}
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        return '%s (SELECT %s FROM %s WHERE l.display_type IS NULL)' % \
               (with_, self._select_sale(fields), self._from_sale(from_clause))

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

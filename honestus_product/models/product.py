from odoo import models, fields


class Product(models.Model):
    _inherit = 'product.product'

    honestus_code = fields.Char()
    honestus_price = fields.Float()


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    honestus_code = fields.Char()
    honestus_price = fields.Monetary()

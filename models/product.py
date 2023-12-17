from odoo import models, fields


class Product(models.Model):
    _name = 'product_labeling.product'
    _description = 'Product records'
    _order = 'name'

    name = fields.Char(string='Product Name', required=True)
    description = fields.Text(string="Description")

    def confirm_create(self):
        return True

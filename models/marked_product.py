from odoo import models, fields


class MarkedProduct(models.Model):
    _name = 'product_labeling.marked_product'

    last_destination = fields.Text(string='Last destination', required=True)
    status = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('internal_movement', 'Internal movement')],
        string='Assigned status', required=True)
    product = fields.Many2one('product_labeling.product', required=True)

from odoo import models, fields, api
from odoo.custom_addons.utils.mark_generate import generate_random_mark


class MarkedProduct(models.Model):
    _name = 'product_labeling.marked_product'

    product = fields.Many2one('product_labeling.product', required=True)
    name = fields.Char(name='Name', readonly=True, required=True)
    last_destination = fields.Text(string='Last destination', required=True)
    state = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('internal_movement', 'Internal movement')],
        string='Assigned status', required=True)

    @api.model
    @api.depends('product')
    def create(self, vals):
        if vals.get('state') == 'purchase':
            product_record = self.env['product_labeling.product'].browse(vals['product'])
            vals['name'] = f'{product_record.name} #{generate_random_mark()}'
        return super(MarkedProduct, self).create(vals)

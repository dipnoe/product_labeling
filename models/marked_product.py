from odoo import models, fields, api
import random
import string


def generate_random_mark():
    # Generating mark
    mark = [''.join(random.choices(string.ascii_lowercase, k=5)) for i in range(3)]
    return '-'.join(mark)



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
    acts = fields.Many2many('product_labeling.act')
    expense_incomes = fields.Many2many('product_labeling.expense_income', "ei_mp_rel")

    final_profit = fields.Integer(string='Final profit')

    @api.model
    @api.depends('product')
    def create(self, vals):
        if vals.get('state') == 'purchase':
            product_record = self.env['product_labeling.product'].browse(vals['product'])
            vals['name'] = f'{product_record.name} #{generate_random_mark()}'
        return super(MarkedProduct, self).create(vals)

    def action_show_expense_income(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expenses/Incomes',
            'view_mode': 'tree,form',
            'res_model': 'product_labeling.expense_income',
            'domain': [('id', 'in', self.expense_incomes.ids)],
            'context': {'default_marked_product_id': self.id},
        }

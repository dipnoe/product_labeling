from odoo import models, fields, api


class ExpenseIncome(models.Model):
    _name = 'product_labeling.expense_income'
    _description = 'Expense/Income'

    act_id = fields.Many2one('product_labeling.act', string='Act', readonly=True)
    operation = fields.Selection([
        ('purchase_cost', 'Purchase'),
        ('promotion', 'Promotion'),
        ('logistics_cost', 'Logistics'),
        ('agency_commission', 'Agency Commission'),
        ('sale', 'Sale')
        ])
    operation_costs = fields.Integer(string='Operation Costs')
    marked_products = fields.Many2many('product_labeling.marked_product', "ei_mp_rel")

    def confirm_create(self):
        return True

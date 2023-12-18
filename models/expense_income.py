from odoo import models, fields


class ExpenseIncome(models.Model):
    _name = 'product_labeling.expense_income'
    _description = 'Expense/Income'

    act_id = fields.Many2one('product_labeling.act', string='Act')
    promotion = fields.Integer('Product promotion')
    logistics_cost = fields.Integer('Logistics')
    purchase_cost = fields.Integer('Purchase cost')
    agency_commission = fields.Integer('Agency commission')
    sale = fields.Integer('Sale')
    sum = fields.Integer(string='Sum')

    def confirm_create(self):
        return True

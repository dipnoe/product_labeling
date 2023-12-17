from odoo import models, fields


class DirectCostItem(models.Model):
    _name = 'product_labeling.direct_cost_item'

    promotion = fields.Integer('Product promotion')
    logistics_cost = fields.Integer('Logistics')
    purchase_cost = fields.Integer('Purchase cost')
    agency_commission = fields.Integer('Agency commission')
    sale = fields.Integer('Sale')


class ExpenseIncome(models.Model):
    _name = 'product_labeling.expense_income'
    _description = 'Expense/Income'

    act_id = fields.Many2one('product_labeling.act', string='Act')
    direct_cost_item = fields.Many2one('product_labeling.direct_cost_item', string='Direct Cost Item')
    sum = fields.Integer(string='Sum')

    def confirm_create(self):
        return True
